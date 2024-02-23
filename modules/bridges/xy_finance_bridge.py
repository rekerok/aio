import pprint
import random
import config
import utils
import settings
from loguru import logger
from modules.account import Account
from modules.web3Bridger import Web3Bridger
from modules.web3Client import Web3Client
from settings import Client_Networks
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class XY_finance_bridge(Web3Bridger):
    NAME = "XY_FINANCE_BRIDGE"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[int | float] = None,
        min_balance: float = 0,
        slippage: float = 1,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            type_transfer=type_transfer,
            value=value,
            min_balance=min_balance,
            slippage=slippage,
        )

    async def _get_quote(
        self,
        from_chain_id: int,
        to_chain_id: int,
        from_token: Token_Info,
        to_token: Token_Info,
        amount_to_send: Token_Amount,
    ):
        url = config.XY_FINANCE.QUOTE_BRIDGE
        # url = "https://open-api.xy.finance/v1/quote?srcChainId=1&fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amount=500000000000000000&destChainId=56&toTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        params = {
            "srcChainId": str(from_chain_id),
            "fromTokenAddress": from_token.address,
            "amount": str(amount_to_send.WEI),
            "destChainId": str(to_chain_id),
            "toTokenAddress": to_token.address,
            # "slippage": self.slippage,
        }

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            params=params,
        )
        if response is None or not response["isSuccess"]:
            logger.error(response["msg"])
            return None
        # pprint.pprint(response)
        return response

    async def _build_tx(
        self,
        from_chain_id: int,
        to_chain_id: int,
        from_token: Token_Info,
        to_token: Token_Info,
        amount_to_send: Token_Amount,
    ):
        url = config.XY_FINANCE.BIULD_TRANSACTION_BRIDGE
        params = {
            "srcChainId": str(from_chain_id),
            "fromTokenAddress": from_token.address,
            "amount": str(amount_to_send.WEI),
            "destChainId": str(to_chain_id),
            "toTokenAddress": to_token.address,
            "slippage": str(self.slippage),
            "receiveAddress": self.acc.address,
        }

        # if settings.USE_REF:
        #     params.update({"reffer": "0x9f6cf6852b7aacf8377083b7a5d52862d0f312c7"})

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            params=params,
        )
        if response is None or not response["isSuccess"]:
            return None
        return response

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token_address: str = "",
    ):
        from_chain_id: int = int(await self.acc.w3.eth.chain_id)
        to_chain_id: int = int(config.GENERAL.CHAIN_IDS.get(to_chain))
        to_token: Token_Info = await self._get_to_token(
            to_chain=to_chain, to_token_address=to_token_address
        )
        from_token, to_token = await Token_Info.to_native_token(
            from_token=from_token, to_token=to_token
        )
        # quote = await self._get_quote(
        #     from_chain_id=from_chain_id,
        #     to_chain_id=to_chain_id,
        #     from_token=from_token,
        #     to_token=to_token,
        #     amount_to_send=amount_to_send,
        # )
        # if quote is None:
        #     logger.error(f"DON'T GET QOUTE")
        #     return RESULT_TRANSACTION.FAIL

        tx = await self._build_tx(
            from_chain_id=from_chain_id,
            to_chain_id=to_chain_id,
            from_token=from_token,
            to_token=to_token,
            amount_to_send=amount_to_send,
        )
        if tx is None:
            logger.error("FAIL BUILD TRANSACTION")
            return RESULT_TRANSACTION.FAIL
        # pprint.pprint(tx)
        return await self._send_transaction(
            from_token=from_token,
            to_address=tx["tx"]["to"],
            data=tx["tx"]["data"],
            amount_to_send=amount_to_send,
        )

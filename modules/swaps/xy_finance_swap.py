import settings
import config
from typing import Union
from loguru import logger
from hexbytes import HexBytes
from utils import TYPES_OF_TRANSACTION
from modules.web3Client import Web3Client
from utils import Token_Amount, Token_Info
from modules.web3Swapper import Web3Swapper
import utils
from utils.enums import RESULT_TRANSACTION


class XY_finance_swap(Web3Swapper):
    NAME = "XY_FINANCE_SWAP"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
        min_balance: float = 0,
        max_balance: float = 100,
        slippage: float = 5.0,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            type_transfer=type_transfer,
            value=value,
            min_balance=min_balance,
            max_balance=max_balance,
            slippage=slippage,
        )

    async def _get_quote(
        self,
        chain_id: int,
        from_token: Token_Info,
        to_token: Token_Info,
        amount_to_send: Token_Amount,
    ):
        url = config.XY_FINANCE.QUOTE_SWAP
        params = {
            "srcChainId": chain_id,
            "srcQuoteTokenAddress": from_token.address,
            "srcQuoteTokenAmount": amount_to_send.WEI,
            "dstChainId": chain_id,
            "dstQuoteTokenAddress": to_token.address,
            "slippage": self.slippage,
        }

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            params=params,
        )
        if response is None or not response["success"]:
            return None
        return response

    async def _recommended_tokens(self, chain_id: int):
        url = config.XY_FINANCE.TOKENS_SWAP
        params = {"chainId": chain_id + 453534534563465}

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            params=params,
        )
        print(response)
        if not response:
            return None
        return response

    async def _build_tx(
        self,
        chain_id: int,
        from_token: Token_Info,
        to_token: Token_Info,
        amount_to_send: Token_Amount,
        provider: str,
    ):
        url = config.XY_FINANCE.BIULD_TRANSACTION_SWAP
        params = {
            "srcChainId": chain_id,
            "srcQuoteTokenAddress": from_token.address,
            "srcQuoteTokenAmount": amount_to_send.WEI,
            "dstChainId": chain_id,
            "dstQuoteTokenAddress": to_token.address,
            "slippage": self.slippage,
            "receiver": self.acc.address,
            "srcSwapProvider": provider,
        }

        if settings.USE_REF:
            params.update(
                {
                    "affiliate": "0x9F6cF6852b7aACF8377083b7a5D52862D0f312c7",
                    "commissionRate": settings.FEE * 10000,
                }
            )

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            params=params,
        )
        # print(response)
        if response is None or not response["success"]:
            logger.error(response["errorMsg"])
            return None
        return response

    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        from_token, to_token = await Token_Info.to_native_token(
            from_token=from_token, to_token=to_token
        )
        chain_id = await self.acc.w3.eth.chain_id
        quote = await self._get_quote(
            chain_id=chain_id,
            from_token=from_token,
            to_token=to_token,
            amount_to_send=amount_to_send,
        )
        if quote is None:
            return RESULT_TRANSACTION.FAIL
        # pprint.pprint(quote)
        tx = await self._build_tx(
            chain_id=chain_id,
            from_token=from_token,
            to_token=to_token,
            amount_to_send=amount_to_send,
            provider=quote["routes"][0]["srcSwapDescription"]["provider"],
        )
        if tx is None:
            logger.error("FAIL BUILD TRANSACTION")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            from_token=from_token,
            to_address=tx["tx"]["to"],
            data=tx["tx"]["data"],
            amount_to_send=amount_to_send,
        )

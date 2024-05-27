from loguru import logger
import config
from typing import Union
from modules.web3Bridger import Web3Bridger
import utils
from utils.enums import RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Nitro(Web3Bridger):
    NAME = "NITRO"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
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
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
        from_chain_id: int,
        to_chain_id: int,
    ):
        url = config.NITRO.QUOTE
        params = {
            "amount": str(amount_to_send.WEI),
            "fromTokenAddress": str(from_token.address),
            "fromTokenChainId": str(from_chain_id),
            "toTokenAddress": str(to_token.address),
            "toTokenChainId": str(to_chain_id),
        }
        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            params=params,
        )
        if response is None:
            return None
        return response

    async def _build_transaction(self, quote: dict):
        url = config.NITRO.BUILD_TRANSACTON
        response = await utils.aiohttp.post_request(url=url, data=quote)
        if response is None:
            return None
        return response

    # https://docs.routerprotocol.com/api?v=PATHFINDER#/
    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
    ):
        from_chain_id: int = int(await self.acc.w3.eth.chain_id)
        to_chain_id: int = int(config.GENERAL.CHAIN_IDS.get(to_chain))

        from_token, to_token = await Token_Info.to_native_token(
            from_token=from_token, to_token=to_token
        )
        if to_token is None:
            logger.error("FAIL GET INFO")
            return RESULT_TRANSACTION.FAIL
        quote = await self._get_quote(
            amount_to_send=amount_to_send,
            from_token=from_token,
            to_token=to_token,
            from_chain_id=from_chain_id,
            to_chain_id=to_chain_id,
        )
        if quote is None:
            logger.error("DON'T GET QUOTE")
            return RESULT_TRANSACTION.FAIL
        quote.update(
            {"senderAddress": self.acc.address, "receiverAddress": self.acc.address}
        )
        transaction = await self._build_transaction(quote=quote)
        if transaction is None:
            logger.error("FAIL BUILD TRANSACTION")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            from_token=from_token,
            to_address=transaction["txn"]["to"],
            amount_to_send=amount_to_send,
            data=transaction["txn"]["data"],
        )

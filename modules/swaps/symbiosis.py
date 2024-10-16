import aiohttp
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


class Symbiosis(Web3Swapper):
    NAME = "SYMBIOSIS"

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
    ) -> dict:
        params = {
            "tokenAmountIn": {
                "address": from_token.address,
                "symbol": from_token.symbol,
                "chainId": chain_id,
                "decimals": amount_to_send.decimal,
                "amount": amount_to_send.wei,
            },
            "tokenOut": {
                "chainId": chain_id,
                "address": to_token.address,
                "symbol": to_token.symbol,
                "decimals": to_token.decimals,
            },
            "to": self.acc.address,
            "from": self.acc.address,
            "slippage": 50,
        }
        response = await utils.aiohttp.post_request(
            url="https://api.symbiosis.finance/crosschain/v1/swap", data=params
        )
        if response is None:
            return None
        return response

    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        try:
            chain_id = await self.acc.w3.eth.chain_id
            quote = await self._get_quote(
                chain_id=chain_id,
                from_token=from_token,
                to_token=to_token,
                amount_to_send=amount_to_send,
            )
            if quote is None:
                logger.error("FAIL BUILD TRANSACTION")
                return RESULT_TRANSACTION.FAIL
            logger.info(f"PRICE IMPACT {quote['priceImpact']}")
            return await self._send_transaction(
                from_token=from_token,
                to_address=quote["tx"]["to"],
                data=quote["tx"]["data"],
                amount_to_send=amount_to_send,
            )
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL

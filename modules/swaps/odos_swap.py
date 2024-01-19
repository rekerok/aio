from loguru import logger
import config
import eth_utils
from typing import Union
from utils import aiohttp
from utils import TYPES_OF_TRANSACTION
from utils import Token_Amount, Token_Info
from modules.web3Swapper import Web3Swapper
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION


class OdosSwap(Web3Swapper):
    NAME = "ODOS"

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
            slippage=slippage,
            max_balance=max_balance,
        )
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.ODOS.CONTRACTS.get(
                    self.acc.network.get(NETWORK_FIELDS.NAME)
                )
            ),
            abi=config.ODOS.ABI,
        )

    async def _get_quote(
        self, from_token: Token_Info, to_token: Token_Info, amount_to_send: Token_Amount
    ):
        url = "https://api.odos.xyz/sor/quote/v2"
        data = {
            "chainId": await self.acc.w3.eth.chain_id,
            "inputTokens": [
                {"tokenAddress": from_token.address, "amount": str(amount_to_send.WEI)}
            ],
            "outputTokens": [{"tokenAddress": to_token.address, "proportion": 1}],
            "userAddr": self.acc.address,
            "slippageLimitPercent": self.slippage,
            "compact": False,
        }
        response = await aiohttp.post_request(url=url, data=data)
        return response

    async def _get_assemble(self, path_id):
        url = "https://api.odos.xyz/sor/assemble"

        data = {
            "userAddr": self.acc.address,
            "pathId": path_id,
            "simulate": False,
        }

        response = await aiohttp.post_request(url=url, data=data)
        return response

    # https://docs.odos.xyz/
    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        if from_token.symbol == self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN):
            from_token.address = config.GENERAL.ZERO_ADDRESS
        if to_token.symbol == self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN):
            to_token.address = config.GENERAL.ZERO_ADDRESS

        quote = await self._get_quote(
            from_token=from_token, to_token=to_token, amount_to_send=amount_to_send
        )
        if not quote:
            logger.error("NOT QUOTE FOR TRANSACTION")
            return RESULT_TRANSACTION.FAIL
        assemble = await self._get_assemble(path_id=quote.get("pathId"))
        if not assemble:
            logger.error("NOT ASSEMBLE")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            data=assemble["transaction"]["data"],
            from_token=from_token,
            to_address=self.contract.address,
            amount_to_send=amount_to_send,
        )

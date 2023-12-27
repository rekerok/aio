import config
import eth_utils
from typing import Union
from utils import aiohttp
from utils import TYPES_OF_TRANSACTION
from utils.enums import NETWORK_FIELDS
from utils import Token_Amount, Token_Info
from modules.web3Swapper import Web3Swapper


class OdosSwap(Web3Swapper):
    NAME = "ODOS"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
        min_balance: float = 0,
        slippage: float = 5.0,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            type_transfer=type_transfer,
            value=value,
            min_balance=min_balance,
            slippage=slippage,
        )
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.ODOS.CONTRACTS.value.get(
                    self.acc.network.get(NETWORK_FIELDS.NAME)
                )
            ),
            abi=config.ODOS.ABI.value,
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

    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        if from_token.symbol == self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN):
            from_token.address = config.GENERAL.ZERO_ADDRESS.value
        if to_token.symbol == self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN):
            to_token.address = config.GENERAL.ZERO_ADDRESS.value

        quote = await self._get_quote(
            from_token=from_token, to_token=to_token, amount_to_send=amount_to_send
        )
        assemble = await self._get_assemble(path_id=quote.get("pathId"))
        value_approve = (
            None
            if from_token.symbol
            == self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN).upper()
            else amount_to_send
        )

        value = (
            amount_to_send
            if from_token.symbol
            == self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN).upper()
            else None
        )

        return await self._send_swap_transaction(
            data=assemble["transaction"]["data"],
            from_token=from_token,
            to_address=self.contract.address,
            value_approve=value_approve,
            value=value,
        )

import time
import eth_utils
import settings
import utils
from typing import Union
from helpers import Token_Info, Token_Amount, TYPE_OF_TRANSACTION, Web3Swapper


class InchSwap(Web3Swapper):
    NAME = "1INCH_SWAP"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPE_OF_TRANSACTION = None,
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

    async def _get_contract_address(
        self,
    ):
        url = f"https://api.1inch.dev/swap/v5.2/{await self.acc.w3.eth.chain_id}/approve/spender"

        headers = {
            "Authorization": f"Bearer {settings.INCH_SWAP_KEY}",
            "accept": "application/json",
        }
        response = await utils.aiohttp.get_json_aiohttp(url=url, headers=headers)
        return response["address"]

    async def _get_quote(
        self, from_token: Token_Info, to_token: Token_Info, amount: Token_Amount
    ):
        url = f"https://api.1inch.dev/swap/v5.2/{await self.acc.w3.eth.chain_id}/swap"
        headers = {
            "Authorization": f"Bearer {settings.INCH_SWAP_KEY}",
            "accept": "application/json",
        }

        params = {
            "src": from_token.address,
            "dst": to_token.address,
            "amount": amount.WEI,
            "from": self.acc.address,
            "slippage": 1,
        }

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            headers=headers,
            params=params,
        )

        return response["tx"]["data"]

    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        contract_address = eth_utils.address.to_checksum_address(
            await self._get_contract_address()
        )
        from_token, to_token = await self._to_native_token(
            from_token=from_token, to_token=to_token
        )

        if from_token.symbol != self.acc.network.get("token"):
            await self.acc.approve(
                token_address=from_token.address,
                spender=contract_address,
                amount=amount_to_send,
            )

        data = await self._get_quote(
            from_token=from_token, to_token=to_token, amount=amount_to_send
        )

        value = (
            amount_to_send.WEI
            if from_token.symbol == self.acc.network.get("token")
            else None
        )
        await self._send_swap_transaction(
            data=data,
            from_token=from_token,
            to_address=contract_address,
            value_approove=None,
            value=value,
        )

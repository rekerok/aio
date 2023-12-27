import time
import utils
import config
import settings
import eth_utils
from typing import Union
from loguru import logger
from utils import TYPES_OF_TRANSACTION
from utils import Token_Amount, Token_Info
from utils.enums import RESULT_TRANSACTION
from modules.web3Swapper import Web3Swapper


class InchSwap(Web3Swapper):
    NAME = "1INCH_SWAP"

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

    async def _get_contract_address(self, chain_id):
        url = f"https://api.1inch.dev/swap/v5.2/{chain_id}/approve/spender"
        headers = {
            "Authorization": f"Bearer {settings.INCH_SWAP_KEY}",
            "accept": "application/json",
        }
        response = await utils.aiohttp.get_json_aiohttp(url=url, headers=headers)
        if not response:
            return None
        return response.get("address")

    async def _get_swap_data(
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
            "slippage": 5,
        }

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            headers=headers,
            params=params,
        )

        if not response:
            return None
        return response["tx"]["data"]

    # https://docs.1inch.io/
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
        contract_address = await self._get_contract_address(chain_id=chain_id)
        if contract_address:
            contract_address = eth_utils.address.to_checksum_address(contract_address)
        else:
            logger.warning("CHECK APIKEY")
            return RESULT_TRANSACTION.FAIL
        logger.debug("NEED SLEEP 10 SEC")
        time.sleep(10)
        if from_token.address != config.GENERAL.NATIVE_TOKEN.value:
            await self.acc.approve(
                token_address=from_token.address,
                spender=contract_address,
                amount=amount_to_send,
            )
        data = await self._get_swap_data(
            from_token=from_token, to_token=to_token, amount=amount_to_send
        )
        if not data:
            logger.error("FAIL GET DATA FOR SWAP OR NOT BALANCE")
            return RESULT_TRANSACTION.FAIL

        value, value_approve = await Web3Swapper._get_value_and_allowance(
            amount=amount_to_send,
            from_native_token=True
            if from_token.address == config.GENERAL.NATIVE_TOKEN.value
            else False,
        )
        return await self._send_swap_transaction(
            data=data,
            from_token=from_token,
            to_address=contract_address,
            value_approve=None,
            value=value,
        )

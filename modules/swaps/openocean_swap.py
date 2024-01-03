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


class OpenoceanSwap(Web3Swapper):
    NAME = "OPENOCEAN"

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

    async def _get_transaction_data(
        self,
        from_token: Token_Info,
        to_token: Token_Info,
        amount: Token_Amount,
        chain_id: int,
    ):
        url = f"https://open-api.openocean.finance/v3/{chain_id}/swap_quote"

        params = {
            "chain": chain_id,
            "inTokenAddress": from_token.address,
            "outTokenAddress": to_token.address,
            "amount": f"{amount.ETHER}",
            "gasPrice": str(
                self.acc.w3.from_wei(await self.acc.w3.eth.gas_price, "gwei")
            ),
            "slippage": self.slippage,
            "account": self.acc.address,
        }

        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
            params=params,
        )
        if not response:
            return None
        return response

    # https://docs.openocean.finance/
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
        transaction = await self._get_transaction_data(
            from_token=from_token,
            to_token=to_token,
            amount=amount_to_send,
            chain_id=chain_id,
        )
        if not transaction:
            logger.error("FAIL GET DATA FOR SWAP")
            return RESULT_TRANSACTION.FAIL
        contract_address = eth_utils.address.to_checksum_address(
            transaction.get("data").get("to")
        )
        try:
            data = transaction.get("data").get("data")
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            data=data,
            from_token=from_token,
            to_address=contract_address,
            amount_to_send=amount_to_send,
        )

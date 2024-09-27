import utils
import config
import settings
import eth_utils
from typing import Union
from loguru import logger
from utils.token_info import Token_Info
from modules.web3Swapper import Web3Swapper
from utils.token_amount import Token_Amount
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION, TYPES_OF_TRANSACTION


class Zerox(Web3Swapper):
    NAME = "ZEROX"

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
        self.url = config.ZEROX.URLS.get(self.acc.network.get(NETWORK_FIELDS.NAME))
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.ZEROX.CONTRACTS.get(self.acc.network.get(NETWORK_FIELDS.NAME))
            ),
            abi=config.ZEROX.ABI,
        )

    async def _get_quote(
        self, from_token: Token_Info, to_token: Token_Info, amount_to_send: Token_Amount
    ):
        headers = {"0x-api-key": settings.ZEROX_KEY}
        params = {
            "sellToken": from_token.address,
            "buyToken": to_token.address,
            "sellAmount": amount_to_send.wei,
        }

        if settings.USE_REF:
            params.update(
                {
                    "feeRecipient": "0x9F6cF6852b7aACF8377083b7a5D52862D0f312c7",
                    "buyTokenPercentageFee": settings.FEE / 100,
                }
            )

        response = await utils.aiohttp.get_json_aiohttp(
            url=self.url + "/swap/v1/quote",
            headers=headers,
            params=params,
        )

        if not response:
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
        quote = await self._get_quote(
            from_token=from_token, to_token=to_token, amount_to_send=amount_to_send
        )
        if not quote:
            logger.warning("CHECK API KEY")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            data=quote.get("data"),
            from_token=from_token,
            to_address=quote.get("to"),
            amount_to_send=amount_to_send,
        )

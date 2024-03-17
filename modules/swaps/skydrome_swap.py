import time
import eth_utils
from loguru import logger
import config
from typing import Union
from modules.swaps.sushi_swap import SushiSwap
from modules.web3Client import Web3Client
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Skydrome(SushiSwap):
    NAME = "SKYDROME"

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
            contract=None
        )
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.SKYDROME.CONTRACTS.get(self.acc.network.get(NETWORK_FIELDS.NAME))
            ),
            abi=config.SKYDROME.ABI,
        )

    async def _get_amount_out(
        self,
        amountIn: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ) -> Token_Amount:
        try:
            amounts_out, swap_type = await self.contract.functions.getAmountOut(
                amountIn.WEI,
                from_token.address,
                to_token.address,
            ).call()
            return amounts_out, swap_type
        except Exception as error:
            logger.error(error)
            return None

    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        from_token, to_token = await Token_Info.to_wrapped_token(
            from_token=from_token,
            to_token=to_token,
            network=self.acc.network,
        )
        amount_in, swap_type = await self._get_amount_out(
            amountIn=amount_to_send,
            from_token=from_token,
            to_token=to_token,
        )

        if amount_in is None:
            return RESULT_TRANSACTION.FAIL

        amount_in = Token_Amount(
            amount=amount_in, decimals=to_token.decimals, wei=True
        )  # Сколько токенов получаю
        deadline = int(time.time()) + 10000
        args = (
            amount_in.WEI,
            [[from_token.address, to_token.address, swap_type]],
            self.acc.address,
            deadline,
        )
        if await Token_Info.is_native_token(network=self.acc.network, token=from_token):
            data = await self.get_data(
                contract=self.contract,
                function_of_contract="swapExactETHForTokens",
                args=args,
            )

        elif await Token_Info.is_native_token(network=self.acc.network, token=to_token):
            data = await self.get_data(
                contract=self.contract,
                function_of_contract="swapExactTokensForETH",
                args=(amount_to_send.WEI, *args),
            )

        else:
            data = await self.get_data(
                contract=self.contract,
                function_of_contract="swapExactTokensForTokens",
                args=(amount_to_send.WEI, *args),
            )
        if data is None:
            logger.error("FAIL GET DATA")
            return RESULT_TRANSACTION.FAIL

        return await self._send_transaction(
            data=data,
            to_address=self.contract.address,
            from_token=from_token,
            amount_to_send=amount_to_send,
        )

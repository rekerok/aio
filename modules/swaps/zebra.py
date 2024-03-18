import time
import eth_utils
import config
from typing import Union
from loguru import logger
from modules.web3Client import Web3Client
from modules.web3Swapper import Web3Swapper
from utils import TYPES_OF_TRANSACTION
from modules.swaps.sushi_swap import SushiSwap
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Zebra(Web3Swapper):
    NAME = "ZEBRA"

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
            # contract=None,
        )
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.ZEBRA.CONTRACTS.get(self.acc.network.get(NETWORK_FIELDS.NAME))
            ),
            abi=config.ZEBRA.ABI,
        )

    async def _get_amounts_out(
        self,
        amountIn: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ) -> Token_Amount:
        try:
            _, amounts_out = await self.contract.functions.getAmountsOut(
                amountIn.WEI,
                [
                    from_token.address,
                    to_token.address,
                ],
            ).call()
            return amounts_out
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
        amount_out_in = await self._get_amounts_out(
            amountIn=amount_to_send,
            from_token=from_token,
            to_token=to_token,
        )

        if amount_out_in is None:
            return RESULT_TRANSACTION.FAIL

        amount_in = Token_Amount(
            amount=int(amount_out_in - amount_out_in * self.slippage / 100),
            decimals=to_token.decimals,
            wei=True,
        )  # Сколько токенов получаю

        path = [from_token.address, to_token.address]
        to = self.acc.address
        deadline = int(time.time()) + 10000

        if await Token_Info.is_native_token(network=self.acc.network, token=from_token):
            data = await Web3Client.get_data(
                contract=self.contract,
                function_of_contract="swapExactETHForTokens",
                args=(amount_in.WEI, path, to, deadline),
            )

        elif await Token_Info.is_native_token(network=self.acc.network, token=to_token):
            data = await Web3Client.get_data(
                contract=self.contract,
                function_of_contract="swapExactTokensForETH",
                args=(amount_to_send.WEI, amount_in.WEI, path, to, deadline),
            )

        else:
            data = await Web3Client.get_data(
                contract=self.contract,
                function_of_contract="swapExactTokensForTokens",
                args=(amount_to_send.WEI, amount_in.WEI, path, to, deadline),
            )

        if data is None:
            logger.error("FAIL GET DATA")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            data=data,
            from_token=from_token,
            to_address=self.contract.address,
            amount_to_send=amount_to_send,
        )

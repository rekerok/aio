import time
import config
from typing import Union
from loguru import logger
from helpers import contracts
from helpers import Web3Swapper, Token_Amount, Token_Info
from utils import TYPE_OF_TRANSACTION


class SushiSwap(Web3Swapper):
    NAME = "SUSHISWAP"

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
        self.contract = self.acc.w3.eth.contract(
            address=contracts.SUSHI_ROUTERS.get(self.acc.network.get("name")),
            abi=config.SUSHI_ABI,
        )

    async def _get_amounts_out(
        self,
        amountIn: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ) -> Token_Amount:
        try:
            amounts_out = await self.contract.functions.getAmountsOut(
                amountIn.WEI,
                [from_token.address, to_token.address],
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
        from_token, to_token = await self._to_wrapped_token(
            from_token=from_token, to_token=to_token
        )
        amount_out_in = await self._get_amounts_out(
            amountIn=amount_to_send,
            from_token=from_token,
            to_token=to_token,
        )

        if amount_out_in is None:
            return

        amount_out = Token_Amount(
            amount=amount_out_in[0], decimals=from_token.decimals, wei=True
        )  # Сколько токенов отдаю

        amount_in = Token_Amount(
            amount=int(amount_out_in[1] - amount_out_in[1] * self.slippage / 100),
            decimals=to_token.decimals,
            wei=True,
        )  # Сколько токенов получаю

        path = [from_token.address, to_token.address]
        to = self.acc.address
        deadline = int(time.time()) + 10000

        data = await self._get_data(
            contract=self.contract,
            function_of_contract="swapExactETHForTokens",
            args=(amount_in.WEI, path, to, deadline),
        )

        if from_token.address == self.acc.w3.to_checksum_address(
            contracts.WETH_CONTRACTS.get(self.acc.network.get("name"))
        ):
            await self._send_swap_transaction(
                data=data,
                to_address=self.contract.address,
                from_token=from_token,
                value=amount_out,
                value_approove=None,
            )
        elif to_token.address == self.acc.w3.to_checksum_address(
            contracts.WETH_CONTRACTS.get(self.acc.network.get("name"))
        ):
            await self._send_swap_transaction(
                data=await self._get_data(
                    contract=self.contract,
                    function_of_contract="swapExactTokensForETH",
                    args=(amount_out.WEI, amount_in.WEI, path, to, deadline),
                ),
                to_address=self.contract.address,
                from_token=from_token,
                value_approove=amount_out,
            )
        else:
            await self._send_swap_transaction(
                data=await self._get_data(
                    contract=self.contract,
                    function_of_contract="swapExactTokensForTokens",
                    args=(amount_out.WEI, amount_in.WEI, path, to, deadline),
                ),
                to_address=self.contract.address,
                from_token=from_token,
                value_approove=amount_out,
            )

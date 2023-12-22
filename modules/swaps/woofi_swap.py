from typing import Union
import config
from helpers import contracts
from loguru import logger
from helpers import Web3Swapper, Token_Info, TYPE_OF_TRANSACTION, Token_Amount


class WoofiSwap(Web3Swapper):
    NAME = "WOOFI SWAP"

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
            address=contracts.WOOFI_SWAP.get(self.acc.network.get("name")),
            abi=config.WOOFI_ABI,
        )

    async def _query_swap(
        self, fromToken: Token_Info, toToken: Token_Info, fromAmount: Token_Amount
    ):
        try:
            amounts_out = await self.contract.functions.querySwap(
                fromToken.address, toToken.address, fromAmount.WEI
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
        from_token, to_token = await self._to_native_token(
            from_token=from_token, to_token=to_token
        )
        amount_in = await self._query_swap(
            fromToken=from_token, toToken=to_token, fromAmount=amount_to_send
        )
        if amount_in is None:
            return

        amount_in = Token_Amount(
            amount=int(amount_in - amount_in * self.slippage / 100),
            decimals=to_token.decimals,
            wei=True,
        )

        data = await self._get_data(
            self.contract,
            "swap",
            args=(
                from_token.address,  # fromToken
                to_token.address,  # toToken
                amount_to_send.WEI,  # fromAmount
                amount_in.WEI,  # minToAmount
                self.acc.address,  # to
                self.acc.address,  # rebateTo
            ),
        )

        await self._send_swap_transaction(
            data=data,
            from_token=from_token,
            to_address=self.contract.address,
            value_approove=None
            if from_token.address == contracts.NATIVE_TOKEN
            else amount_to_send,
            value=amount_to_send
            if from_token.address == contracts.NATIVE_TOKEN
            else None,
        )

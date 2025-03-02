import config
from typing import Union
from loguru import logger
from utils import TYPES_OF_TRANSACTION
from modules.web3Client import Web3Client
from utils import Token_Amount, Token_Info
from modules.web3Swapper import Web3Swapper
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION


class WoofiSwap(Web3Swapper):
    NAME = "WOOFI SWAP"

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
        self.contract = self.acc.w3.eth.contract(
            address=config.WOOFI.CONTRACTS.get(
                self.acc.network.get(NETWORK_FIELDS.NAME)
            ),
            abi=config.WOOFI.ABI,
        )

    async def _query_swap(
        self, fromToken: Token_Info, toToken: Token_Info, fromAmount: Token_Amount
    ):
        try:
            amounts_out = await self.contract.functions.querySwap(
                fromToken.address, toToken.address, fromAmount.wei
            ).call()
            return amounts_out
        except Exception as error:
            logger.error(error)
            return None

    # https://learn.woo.org/v/woofi-dev-docs/
    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        from_token, to_token = await Token_Info.to_native_token(
            from_token=from_token,
            to_token=to_token,
        )

        amount_in = await self._query_swap(
            fromToken=from_token, toToken=to_token, fromAmount=amount_to_send
        )
        if amount_in is None:
            logger.error("DON'T GET AMOUNT IN")
            return RESULT_TRANSACTION.FAIL

        amount_in = Token_Amount(
            amount=int(amount_in - amount_in * self.slippage / 100),
            decimals=to_token.decimals,
            wei=True,
        )

        data=await Web3Client.get_data(
            self.contract,
            "swap",
            args=(
                from_token.address,  # fromToken
                to_token.address,  # toToken
                amount_to_send.wei,  # fromAmount
                amount_in.wei,  # minToAmount
                self.acc.address,  # to
                self.acc.address,  # rebateTo
            ),
        )
        if data is None:
            logger.error("NOT DATA FOR SWAP")
            return RESULT_TRANSACTION.FAIL

        return await self._send_transaction(
            data=data,
            from_token=from_token,
            to_address=self.contract.address,
            amount_to_send=amount_to_send,
        )

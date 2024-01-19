import config
from typing import Union
from utils import TYPES_OF_TRANSACTION
from modules.swaps.sushi_swap import SushiSwap


class BaseSwap(SushiSwap):
    NAME = "BASESWAP"

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
            address=config.BASESWAP.CONTRACT,
            abi=config.BASESWAP.ABI,
        )

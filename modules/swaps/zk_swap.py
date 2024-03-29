import eth_utils
import config
from typing import Union
from loguru import logger
from utils import TYPES_OF_TRANSACTION
from modules.swaps.sushi_swap import SushiSwap


class ZkSwap(SushiSwap):
    NAME = "ZKSWAP"

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
            contract=None,
        )
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(config.ZKSWAP.CONTRACT),
            abi=config.ZKSWAP.ABI,
        )

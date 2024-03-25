from typing import Union

from loguru import logger

import config
import eth_utils
from modules import Web3Lending
from modules.lendings.aave import Aave
from utils.enums import RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class ZeroLend(Aave):
    NAME = "ZEROLEND"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        value: tuple[Union[int, float]] = None,
        type_lending: TYPES_OF_TRANSACTION = None,
        min_balance: float = 0,
        max_balance: float = 100,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            value=value,
            min_balance=min_balance,
            max_balance=max_balance,
            type_lending=type_lending,
            contract=False,
        )
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(config.ZEROLEND.CONTRACT),
            abi=config.ZEROLEND.ABI,
        )
        self.weth_token = eth_utils.address.to_checksum_address(config.ZEROLEND.WETH)
        self.pool = eth_utils.address.to_checksum_address(config.ZEROLEND.POOL)

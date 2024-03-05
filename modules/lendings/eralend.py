from typing import Union

from loguru import logger

import config
import eth_utils
from modules import Web3Lending
from modules.lendings.basilisk import Basilisk
from modules.web3Client import Web3Client
from utils.enums import RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Eralend(Basilisk):
    NAME = "ERALEND"

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
        )
        self.contract = self.acc.w3.eth.contract(
            eth_utils.address.to_checksum_address(
                config.ERALEND.LANDINGS.get(""),
            ),
            abi=config.ERALEND.ABI,
        )
        self.liquidity_contract = self.acc.w3.eth.contract(
            address=self.contract.address, abi=config.ERALEND.ABI
        )

        self.withdraw_fuctions = ["redeemUnderlying"]

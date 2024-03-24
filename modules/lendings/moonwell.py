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


class Moonwell(Web3Lending):
    NAME = "MOONWELL"

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

    async def _perform_deposit(
        self, amount_to_deposit: Token_Amount, token_to_deposit: Token_Info
    ):

        contract = self.acc.w3.eth.contract(
            eth_utils.address.to_checksum_address(
                config.MOONWELL.CONTRACT_DEPOSIT,
            ),
            abi=config.MOONWELL.ABI_DEPOSIT,
        )
        data = await self.get_data(
            contract=contract,
            function_of_contract="mint",
            args=(self.acc.address,),
        )
        if data is None:
            logger.error("FAIL GET DATA")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            from_token=token_to_deposit,
            to_address=contract.address,
            data=data,
            amount_to_send=amount_to_deposit,
        )

    async def _perform_withdraw(self, token_to_withdraw: Token_Info):
        contract = self.acc.w3.eth.contract(
            eth_utils.address.to_checksum_address(
                config.MOONWELL.WETH_TOKEN,
            ),
            abi=config.MOONWELL.ABI_WITHDRAW,
        )
        try:
            amount_to_deposited = await self.acc.get_balance(
                token_address=config.MOONWELL.WETH_TOKEN
            )
            if amount_to_deposited.ETHER < self.min_balance:
                logger.error(f"DEPOSIT < {self.min_balance}")
                return RESULT_TRANSACTION.FAIL
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        logger.info(f"WITHDRAW {amount_to_deposited.ETHER} {token_to_withdraw.symbol}")

        await self.acc.approve(
            token_address=contract.address,
            spender=contract.address,
            amount=amount_to_deposited,
        )
        data = await self.get_data(
            contract=contract,
            function_of_contract="redeem",
            args=(amount_to_deposited.WEI,),
        )
        if data is None:
            logger.error("FAIL GET DATA")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            from_token=token_to_withdraw, to_address=contract.address, data=data
        )

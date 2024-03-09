from typing import Union

from loguru import logger

import config
import eth_utils
from modules import Web3Lending
from utils.enums import RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Layerbank(Web3Lending):
    NAME = "LAYERBANK"

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
            address=eth_utils.address.to_checksum_address(config.LAYERBANK.CONTRACT),
            abi=config.LAYERBANK.ABI,
        )

    async def _perform_deposit(
        self, amount_to_deposit: Token_Amount, token_to_deposit: Token_Info
    ):
        data = await self.get_data(
            contract=self.contract,
            function_of_contract="supply",
            args=(
                eth_utils.address.to_checksum_address(config.LAYERBANK.WETH),
                amount_to_deposit.WEI,
            ),
        )
        if data is None:
            logger.error("FAIL GET DATA")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            from_token=token_to_deposit,
            to_address=self.contract.address,
            data=data,
            amount_to_send=amount_to_deposit,
        )

    async def _perform_withdraw(self, token_to_withdraw: Token_Info):
        try:
            amount_to_deposited = await self.acc.get_balance(
                token_address=config.LAYERBANK.WETH
            )
            min_balance = Token_Amount(
                    amount=self.min_balance,
                )
            if amount_to_deposited.WEI < min_balance.WEI:
                    logger.error(f"DEPOSIT < {min_balance.ETHER}")
                    return RESULT_TRANSACTION.FAIL
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        logger.info(f"WITHDRAW {amount_to_deposited.ETHER} {token_to_withdraw.symbol}")

        await self.acc.approve(
            token_address=config.LAYERBANK.WETH,
            spender=self.contract.address,
            amount=amount_to_deposited,
        )
        data = await self.get_data(
            contract=self.contract,
            function_of_contract="redeemUnderlying",
            args=(
                eth_utils.address.to_checksum_address(config.LAYERBANK.WETH),
                amount_to_deposited.WEI,
            ),
        )
        if data is None:
            logger.error("FAIL GET DATA")
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            from_token=token_to_withdraw, to_address=self.contract.address, data=data
        )

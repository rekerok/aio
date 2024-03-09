import random
from typing import Union

from loguru import logger

import config
import eth_utils
from modules import Web3Lending
from modules.web3Client import Web3Client
from utils.enums import RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Basilisk(Web3Lending):
    NAME = "BASILISK"

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
                config.BASILISK.LANDINGS.get(""),
            ),
            abi=config.BASILISK.ABI,
        )
        self.liquidity_contract = self.acc.w3.eth.contract(
            address=self.contract.address, abi=config.BASILISK.ABI
        )

        self.withdraw_fuctions = ["redeemUnderlying", "redeem"]

    async def _perform_deposit(
        self, amount_to_deposit: Token_Amount, token_to_deposit: Token_Info
    ):

        data = "0x1249c58b"
        return await self._send_transaction(
            from_token=token_to_deposit,
            to_address=self.contract.address,
            data=data,
            amount_to_send=amount_to_deposit,
        )

    async def _perform_withdraw(self, token_to_withdraw: Token_Info):
        try:
            liquidity_balance = (
                await self.liquidity_contract.functions.balanceOfUnderlying(
                    self.acc.address
                ).call()
            )
            liquidity_balance = Token_Amount(
                amount=liquidity_balance,
                decimals=token_to_withdraw.decimals,
                wei=True,
            )
            min_balance = Token_Amount(
                amount=self.min_balance,
            )
            if liquidity_balance.WEI < min_balance.WEI:
                logger.error(f"DEPOSIT < {min_balance.ETHER}")
                return RESULT_TRANSACTION.FAIL
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        logger.info(f"WITHDRAW {liquidity_balance.ETHER} {token_to_withdraw.symbol}")

        data = await Web3Client.get_data(
            contract=self.liquidity_contract,
            function_of_contract=random.choice(self.withdraw_fuctions),
            args=(liquidity_balance.WEI,),
        )
        return await self._send_transaction(
            from_token=token_to_withdraw,
            data=data,
            to_address=self.liquidity_contract.address,
        )

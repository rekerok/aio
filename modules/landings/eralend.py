from typing import Union

from loguru import logger

import config
import eth_utils
from modules import Web3Lending
from modules.web3Client import Web3Client
from utils.enums import RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Eralend(Web3Lending):
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

    async def _perform_deposit(
        self, amount_to_deposit: Token_Amount, token_to_deposit: Token_Info
    ):
        if await Token_Info.is_native_token(
            network=self.acc.network, token=token_to_deposit
        ):
            contract = eth_utils.address.to_checksum_address(
                config.ERALEND.LANDINGS.get("")
            )
            return await self._send_transaction(
                from_token=token_to_deposit,
                to_address=contract,
                amount_to_send=amount_to_deposit,
                data="0x1249c58b",
            )

        else:
            contract = self.acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(
                    config.ERALEND.LANDINGS.get(token_to_deposit.address)
                ),
                abi=config.ERALEND.ABI,
            )
            data = await Web3Client.get_data(
                contract=contract,
                function_of_contract="mint",
                args=(amount_to_deposit.WEI,),
            )
            return await self._send_transaction(
                from_token=token_to_deposit,
                to_address=contract.address,
                amount_to_send=amount_to_deposit,
                data=data,
            )

    async def _perform_withdraw(self, token_to_withdraw: Token_Info):
        contract_address = eth_utils.address.to_checksum_address(
            config.ERALEND.LANDINGS.get("")
        )
        liquidity_contract = self.acc.w3.eth.contract(
            address=contract_address, abi=config.ERALEND.ABI
        )

        # liquidity_balance = await Web3Client.get_data(
        #     contract=liquidity_contract,
        #     function_of_contract="balanceOfUnderlying",
        #     args=(self.acc.address,),
        # )
        try:
            liquidity_balance = await liquidity_contract.functions.balanceOfUnderlying(
                self.acc.address
            ).call()
            liquidity_balance = Token_Amount(
                amount=liquidity_balance,
                decimals=token_to_withdraw.decimals,
                wei=True,
            )
            logger.info(
                f"WITHDRAW {liquidity_balance.ETHER} {token_to_withdraw.symbol}"
            )
            if int(liquidity_balance.WEI) == 0:
                logger.error("NOT DEPOSITS")
                return RESULT_TRANSACTION.FAIL
            else:
                data = await Web3Client.get_data(
                    contract=liquidity_contract,
                    function_of_contract="redeemUnderlying",
                    args=(liquidity_balance.WEI,),
                )
                return await self._send_transaction(
                    from_token=token_to_withdraw,
                    data=data,
                    to_address=liquidity_contract.address,
                )
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL

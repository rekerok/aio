from abc import abstractmethod
import random
from typing import Union

from loguru import logger
from modules.account import Account
from modules.web3Client import Web3Client
import utils
import config
from utils.enums import (
    NETWORK_FIELDS,
    PARAMETR,
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Web3Lending(Web3Client):
    NAME = ""

    def __init__(
        self,
        private_key: str,
        network: dict,
        type_lending: TYPES_OF_TRANSACTION,
        value: tuple[Union[int, float]],
        min_balance: float = 0,
        max_balance: float = 100,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
        )
        try:
            self.value: tuple[Union[int, float]] = value
            self.min_balance: float = min_balance
            self.type_lending = type_lending
            self.max_balance: float = max_balance
        except Exception as error:
            logger.error("CHECK INPUT PARAMETRS")
            return

    async def _make_deposit_percent(
        self, token_to_deposit: Token_Info, balance: Token_Amount
    ):
        percent = random.uniform(self.value[0], self.value[1])
        amount_to_deposit = Token_Amount(
            balance.ether * percent / 100, decimals=token_to_deposit.decimals
        )

        logger.info(f"PERCENT: {percent} %")
        logger.info(f"DEPOSIT: {amount_to_deposit.ether} {token_to_deposit.symbol}")

        return await self._perform_deposit(
            amount_to_deposit=amount_to_deposit, token_to_deposit=token_to_deposit
        )

    async def _make_deposit_all_balance(
        self, token_to_deposit: Token_Info, balance: Token_Amount
    ):
        keep_amount = Token_Amount(
            amount=random.uniform(self.value[0], self.value[1]),
            decimals=token_to_deposit.decimals,
        )
        amount_to_deposit = Token_Amount(
            amount=balance.ether - keep_amount.ether, decimals=token_to_deposit.decimals
        )

        if keep_amount.ether > balance.ether:
            logger.error(f"KEEP AMOUNT:  {keep_amount.ether} > {balance.ether} BALANCE")
            return RESULT_TRANSACTION.FAIL

        logger.info(f"DEPOSIT: {amount_to_deposit.ether} {token_to_deposit.symbol}")

        return await self._perform_deposit(
            amount_to_deposit=amount_to_deposit, token_to_deposit=token_to_deposit
        )

    async def _make_deposit_amount(
        self, token_to_deposit: Token_Info, balance: Token_Amount
    ):
        amount_to_deposit = Token_Amount(
            amount=random.uniform(self.value[0], self.value[1]),
            decimals=token_to_deposit.decimals,
        )

        if amount_to_deposit.ether > balance.ether:
            logger.info(f"BALANCE: {balance.ether} < {amount_to_deposit.ether} SEND")
            return RESULT_TRANSACTION.FAIL

        logger.info(f"DEPOSIT: {amount_to_deposit.ether} {token_to_deposit.symbol}")

        return await self._perform_deposit(
            amount_to_deposit=amount_to_deposit, token_to_deposit=token_to_deposit
        )

    async def _choice_type_transaction(
        self,
    ):
        if self.type_lending == TYPES_OF_TRANSACTION.PERCENT:
            return self._make_deposit_percent
        elif self.type_lending == TYPES_OF_TRANSACTION.ALL_BALANCE:
            return self._make_deposit_all_balance
        else:
            return self._make_deposit_amount

    async def deposit(self, token_to_deposit: config.Token):
        logger.info("DEPOSIT")
        token_to_deposit: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=token_to_deposit.address
        )
        if token_to_deposit is None:
            return RESULT_TRANSACTION.FAIL
        balance: Token_Amount = await self.acc.get_balance(token_to_deposit.address)

        logger.info(f"WALLET: {self.acc.address}")
        logger.info(f"NETWORK: {self.acc.network.get(NETWORK_FIELDS.NAME)}")
        logger.info(f"BALANCE: {balance.ether} {token_to_deposit.symbol}")
        logger.info(f"DEX: {self.NAME} ")

        if not self.min_balance <= balance.ether <= self.max_balance:
            logger.error(
                f"NOT {self.min_balance} < {balance.ether} < {self.max_balance}"
            )
            return RESULT_TRANSACTION.FAIL

        if not await Web3Client.wait_gas(acc=self.acc):
            return RESULT_TRANSACTION.FAIL

        func_lending = await self._choice_type_transaction()
        return await func_lending(
            token_to_deposit=token_to_deposit,
            balance=balance,
        )

    async def withdraw(self, token_to_withdraw: config.Token):
        logger.info("WITHDRAW")
        logger.info(f"DEX: {self.NAME} ")
        logger.info(f"WALLET: {self.acc.address}")
        logger.info(f"NETWORK: {self.acc.network.get(NETWORK_FIELDS.NAME)}")

        token_to_withdraw: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=token_to_withdraw.address
        )
        
        if token_to_withdraw is None:
            logger.error("NOT INFO ABOUT WITHDRAW TOKEN")
            return RESULT_TRANSACTION.FAIL
        return await self._perform_withdraw(token_to_withdraw=token_to_withdraw)

    @abstractmethod
    async def _perform_deposit(
        self, amount_to_deposit: Token_Amount, token_to_deposit: Token_Info
    ):
        pass

    @abstractmethod
    async def _perform_withdraw(selfm, token_to_withdraw: Token_Amount):
        pass

    @staticmethod
    async def _create_database(wallets: list[str], params):
        database = list()
        for param in params:
            for wallet in (
                wallets
                if param.get(PARAMETR.WALLETS_FILE) == ""
                else await utils.files.read_file_lines(param.get(PARAMETR.WALLETS_FILE))
            ):
                token = random.choice(param.get(PARAMETR.TOKENS))
                acc = Account(private_key=wallet, network=param.get(PARAMETR.NETWORK))
                # allow_transaction, balance, token_info = await Web3Client.check_min_balance(
                #     acc=acc,
                #     token=param.get(PARAMETR.FROM_TOKEN),
                #     min_balance=param.get(PARAMETR.MIN_BALANCE),
                # )
                # if allow_transaction:
                database.append(
                    {
                        "private_key": wallet,
                        "network": param.get(PARAMETR.NETWORK),
                        "value": param.get(PARAMETR.VALUE),
                        "token": token.get(PARAMETR.TOKEN),
                        "app": random.choice(token.get(PARAMETR.LENDINGS)),
                        "type_lending": param.get(PARAMETR.TYPE_TRANSACTION),
                        "min_balance": param.get(PARAMETR.MIN_BALANCE),
                        "deposit": param.get(PARAMETR.LENDING_DEPOSIT),
                        # "max_balance": param.get(PARAMETR.MAX_BALANCE),
                    }
                )
        return database

    @staticmethod
    async def landing_use_database(settings, wallets: list[str] = None):
        if wallets is None:
            wallets = await utils.files.read_file_lines(
                path="files/wallets.txt",
            )
        database = await Web3Lending._create_database(
            wallets=wallets, params=settings.PARAMS
        )
        random.shuffle(database)
        counter = 1
        for data in database:
            logger.warning(f"OPERATION {counter}/{len(database)}")
            app_class = data.get("app")
            app = app_class(
                private_key=data.get("private_key"),
                network=data.get("network"),
                value=data.get("value"),
                type_lending=data.get("type_lending"),
                min_balance=data.get("min_balance"),
            )
            if data.get("deposit") == True:
                result = await app.deposit(token_to_deposit=data.get("token"))
            else:
                result = await app.withdraw(token_to_withdraw=data.get("token"))
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

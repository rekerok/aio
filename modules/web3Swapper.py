import utils
import random
import config
from typing import Union
from loguru import logger
from abc import abstractmethod
from modules.account import Account
from modules.web3Client import Web3Client
from utils import Token_Amount, Token_Info
from utils.enums import NETWORK_FIELDS, PARAMETR
from utils import TYPES_OF_TRANSACTION, RESULT_TRANSACTION


class Web3Swapper(Web3Client):
    def __init__(
        self,
        private_key: str,
        network: dict,
        type_transfer: TYPES_OF_TRANSACTION,
        value: tuple[Union[int, float]],
        min_balance: float,
        max_balance: float,
        slippage: float,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
        )
        self.type_transfer = type_transfer
        self.value = value
        self.min_balance = min_balance
        self.max_balance = max_balance
        self.slippage = slippage

    async def _make_swap_percent(
        self, from_token: Token_Info, to_token: Token_Info, balance: Token_Amount
    ):
        percent = random.uniform(self.value[0], self.value[1])
        amount_to_send = Token_Amount(
            balance.ETHER * percent / 100, decimals=from_token.decimals
        )

        logger.info(f"PERCENT: {percent} %")
        logger.info(f"SEND: {amount_to_send.ETHER} {from_token.symbol}")

        return await self._perform_swap(
            amount_to_send=amount_to_send, from_token=from_token, to_token=to_token
        )

    async def _make_swap_all_balance(
        self, from_token: Token_Info, to_token: Token_Info, balance: Token_Amount
    ):
        keep_amount = Token_Amount(
            amount=random.uniform(self.value[0], self.value[1]),
            decimals=from_token.decimals,
        )
        amount_to_send = Token_Amount(
            amount=balance.ETHER - keep_amount.ETHER, decimals=from_token.decimals
        )

        if keep_amount.ETHER > balance.ETHER:
            logger.error(f"KEEP AMOUNT:  {keep_amount.ETHER} > {balance.ETHER} BALANCE")
            return RESULT_TRANSACTION.FAIL

        logger.info(f"BALANCE: {balance.ETHER} {from_token.symbol}")
        logger.info(f"SEND: {amount_to_send.ETHER} {from_token.symbol}")

        return await self._perform_swap(amount_to_send, from_token, to_token)

    async def _make_swap_amount(
        self, from_token: Token_Info, to_token: Token_Info, balance: Token_Amount
    ):
        amount_to_send = Token_Amount(
            amount=random.uniform(self.value[0], self.value[1]),
            decimals=from_token.decimals,
        )

        if amount_to_send.ETHER > balance.ETHER:
            logger.info(f"BALANCE: {balance.ETHER} < {amount_to_send.ETHER} SEND")
            return RESULT_TRANSACTION.FAIL

        logger.info(f"SEND: {amount_to_send.ETHER} {from_token.symbol}")

        return await self._perform_swap(amount_to_send, from_token, to_token)

    async def _choice_type_transaction(
        self,
    ):
        if self.type_transfer == TYPES_OF_TRANSACTION.PERCENT:
            return self._make_swap_percent
        elif self.type_transfer == TYPES_OF_TRANSACTION.ALL_BALANCE:
            return self._make_swap_all_balance
        else:
            return self._make_swap_amount

    @abstractmethod
    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        pass

    async def swap(
        self, from_token: config.TOKEN = None, to_token: config.TOKEN = None
    ):
        from_token: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=from_token.ADDRESS
        )
        to_token: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=to_token.ADDRESS
        )
        if not from_token or not to_token:
            return RESULT_TRANSACTION.FAIL
        balance: Token_Amount = await self.acc.get_balance(from_token.address)

        logger.info(f"WALLET: {self.acc.address}")
        logger.info(f"NETWORK: {self.acc.network.get(NETWORK_FIELDS.NAME)}")
        logger.info(f"DEX: {self.NAME} ")
        logger.info(f"{from_token.symbol} -> {to_token.symbol}")

        if not self.min_balance <= balance.ETHER <= self.max_balance:
            logger.error(
                f"NOT {self.min_balance} < {balance.ETHER} < {self.max_balance}"
            )
            return RESULT_TRANSACTION.FAIL

        func_swap = await self._choice_type_transaction()

        return await func_swap(
            from_token=from_token,
            to_token=to_token,
            balance=balance,
        )

    @staticmethod
    async def _create_database(wallets: list[str], params):
        database = list()
        for param in params:
            for wallet in (
                wallets
                if param.get(PARAMETR.WALLETS_FILE) == ""
                else await utils.files.read_file_lines(param.get(PARAMETR.WALLETS_FILE))
            ):
                to_token = random.choice(param.get(PARAMETR.TO_TOKENS))
                database.append(
                    {
                        "private_key": wallet,
                        "network": param.get(PARAMETR.NETWORK),
                        "dex": random.choice(to_token.get(PARAMETR.DEXS)),
                        "type_swap": param.get(PARAMETR.TYPE_TRANSACTION),
                        "value": param.get(PARAMETR.VALUE),
                        "from_token": param.get(PARAMETR.FROM_TOKEN),
                        "min_balance": param.get(PARAMETR.MIN_BALANCE),
                        "max_balance": param.get(PARAMETR.MAX_BALANCE),
                        "to_token": to_token.get(PARAMETR.TO_TOKEN),
                    }
                )
        return database

    @staticmethod
    async def swap_use_database(settings):
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
        database = await Web3Swapper._create_database(
            wallets=wallets, params=settings.PARAMS
        )
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        counter = 1
        for data in database:
            logger.warning(f"OPERATION {counter}/{len(database)}")
            dex_class = data.get("dex")
            dex = dex_class(
                private_key=data.get("private_key"),
                network=data.get("network"),
                type_transfer=data.get("type_swap"),
                value=data.get("value"),
                min_balance=data.get("min_balance"),
                max_balance=data.get("max_balance"),
            )
            result = await dex.swap(
                from_token=data.get("from_token"),
                to_token=data.get("to_token"),
            )
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

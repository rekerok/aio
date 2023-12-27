import utils
import random
from typing import Union
from loguru import logger
from abc import abstractmethod
from modules.account import Account
from utils import Token_Amount, Token_Info
from utils.enums import NETWORK_FIELDS, PARAMETR
from utils import TYPES_OF_TRANSACTION, RESULT_TRANSACTION


class Web3Swapper:
    NAME = ""

    def __init__(
        self,
        private_key: str,
        network: dict,
        type_transfer: TYPES_OF_TRANSACTION,
        value: tuple[Union[int, float]],
        min_balance: float,
        slippage: float,
    ) -> None:
        self.network = network
        self.acc = Account(private_key=private_key, network=self.network)
        self.type_transfer = type_transfer
        self.value = value
        self.min_balance = min_balance
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

    @abstractmethod
    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        pass

    async def _get_data(self, contract, function_of_contract: str, args: tuple = None):
        try:
            return contract.encodeABI(
                function_of_contract,
                args=args,
            )
        except Exception as e:
            logger.error(e)
            return None

    async def _send_swap_transaction(
        self,
        data,
        from_token: Token_Info,
        to_address: str,
        value_approve: Token_Amount = None,
        value: Token_Amount = None,
    ):
        if value_approve:
            await self.acc.approve(
                token_address=from_token.address,
                spender=to_address,
                amount=value_approve,
            )
        return await self.acc.send_transaction(
            to_address=to_address, data=data, value=value
        )

    async def swap(self, from_token_address: str = None, to_token_address: str = None):
        from_token_address: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=from_token_address
        )
        to_token_address: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=to_token_address
        )

        balance: Token_Amount = await self.acc.get_balance(from_token_address.address)

        logger.info(f"WALLET: {self.acc.address}")
        logger.info(f"NETWORK: {self.acc.network.get(NETWORK_FIELDS.NAME)}")
        logger.info(f"DEX: {self.NAME} ")
        logger.info(f"{from_token_address.symbol} -> {to_token_address.symbol}")

        if balance.ETHER < self.min_balance:
            logger.error(f"Balance {balance.ETHER} < {self.min_balance}")
            return RESULT_TRANSACTION.FAIL

        if self.type_transfer == TYPES_OF_TRANSACTION.PERCENT:
            return await self._make_swap_percent(
                from_token=from_token_address,
                to_token=to_token_address,
                balance=balance,
            )
        elif self.type_transfer == TYPES_OF_TRANSACTION.ALL_BALANCE:
            return await self._make_swap_all_balance(
                from_token=from_token_address,
                to_token=to_token_address,
                balance=balance,
            )
        else:
            return await self._make_swap_amount(
                from_token=from_token_address,
                to_token=to_token_address,
                balance=balance,
            )

    @staticmethod
    async def _get_value_and_allowance(amount: Token_Amount, from_native_token: bool):
        if from_native_token:
            value = amount
            value_approve = None
        else:
            value = None
            value_approve = amount
        return value, value_approve

    @staticmethod
    async def _get_random_pair_for_swap(token_list: list):
        # Выбрать случайный токен "from"
        from_token = random.choice(token_list)

        # Выбрать случайный токен "to", отличающийся от "from"
        to_token = random.choice(
            [
                token
                for token in token_list
                if token.get("address") != from_token.get("address")
            ]
        )
        return from_token, to_token

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
                        "to_token": to_token.get(PARAMETR.TOKEN_ADDRESS),
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
            logger.info(f"OPERATION {counter}/{len(database)}")
            dex_class = data.get("dex")
            dex = dex_class(
                private_key=data.get("private_key"),
                network=data.get("network"),
                type_transfer=data.get("type_swap"),
                value=data.get("value"),
                min_balance=data.get("min_balance"),
            )
            result = await dex.swap(
                from_token_address=data.get("from_token"),
                to_token_address=data.get("to_token"),
            )
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

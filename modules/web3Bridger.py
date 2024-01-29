import random
import config
from typing import Union
from loguru import logger
from abc import abstractmethod
from modules.web3Client import Web3Client
from utils import Token_Amount, Token_Info
import utils
from utils.enums import (
    NETWORK_FIELDS,
    PARAMETR,
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)


class Web3Bridger(Web3Client):
    def __init__(
        self,
        private_key: str,
        network: dict,
        type_transfer: TYPES_OF_TRANSACTION,
        value: tuple[Union[int, float]],
        min_balance: float,
        slippage: float,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
        )
        self.type_transfer = type_transfer
        self.value = value
        self.min_balance = min_balance
        self.slippage = slippage

    async def _make_bridge_percent(
        self,
        from_token: Token_Info,
        to_token_address: str,
        to_network: config.Network,
        balance: Token_Amount,
    ):
        percent = random.uniform(self.value[0], self.value[1])
        amount_to_send = Token_Amount(
            balance.ETHER * percent / 100, decimals=from_token.decimals
        )

        logger.info(f"PERCENT: {percent} %")
        logger.info(f"SEND: {amount_to_send.ETHER} {from_token.symbol}")

        return await self._perform_bridge(
            amount_to_send=amount_to_send,
            from_token=from_token,
            to_chain=to_network,
            to_token_address=to_token_address,
        )

    async def _make_bridge_all_balance(
        self,
        from_token: Token_Info,
        to_token_address: str,
        to_network: config.Network,
        balance: Token_Amount,
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

        return await self._perform_bridge(
            amount_to_send=amount_to_send,
            from_token=from_token,
            to_chain=to_network,
            to_token_address=to_token_address,
        )

    async def _make_bridge_amount(
        self,
        from_token: Token_Info,
        to_token_address: str,
        to_network: config.Network,
        balance: Token_Amount,
    ):
        amount_to_send = Token_Amount(
            amount=random.uniform(self.value[0], self.value[1]),
            decimals=from_token.decimals,
        )

        if amount_to_send.ETHER > balance.ETHER:
            logger.error(f"BALANCE: {balance.ETHER} < {amount_to_send.ETHER} SEND")
            return RESULT_TRANSACTION.FAIL

        logger.info(f"SEND: {amount_to_send.ETHER} {from_token.symbol}")

        return await self._perform_bridge(
            amount_to_send=amount_to_send,
            from_token=from_token,
            to_chain=to_network,
            to_token_address=to_token_address,
        )

    @abstractmethod
    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token_address: str = "",
    ):
        pass

    async def _choice_type_transaction(
        self,
    ):
        if self.type_transfer == TYPES_OF_TRANSACTION.PERCENT:
            return self._make_bridge_percent
        elif self.type_transfer == TYPES_OF_TRANSACTION.ALL_BALANCE:
            return self._make_bridge_all_balance
        else:
            return self._make_bridge_amount

    async def bridge(
        self,
        from_token_address: str,
        to_token_address: str,
        to_network: config.Network,
    ):
        from_token: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=from_token_address
        )

        if not from_token:
            return RESULT_TRANSACTION.FAIL
        balance: Token_Amount = await self.acc.get_balance(from_token.address)
        if balance is None:
            logger.warning("CHECK PROXY")
            return RESULT_TRANSACTION.FAIL
        logger.info(f"WALLET: {self.acc.address}")
        logger.info(
            f"{self.acc.network.get(NETWORK_FIELDS.NAME)} ({from_token.symbol}) -> {to_network}"
        )
        logger.info(f"DEX: {self.NAME} ")
        if balance.ETHER < self.min_balance:
            logger.error(f"Balance {balance.ETHER} < {self.min_balance}")
            return RESULT_TRANSACTION.FAIL
        func_bridge = await self._choice_type_transaction()

        return await func_bridge(
            from_token=from_token,
            to_token_address=to_token_address,
            to_network=to_network,
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
                        "to_network": to_token.get(PARAMETR.NETWORK),
                        "to_token": to_token.get(PARAMETR.TOKEN_ADDRESS),
                    }
                )
        return database

    @staticmethod
    async def swap_use_database(settings):
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
        database = await Web3Bridger._create_database(
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
            )
            result = await dex.bridge(
                from_token_address=data.get("from_token"),
                to_token_address=data.get("to_token"),
                to_network=data.get("to_network"),
            )
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

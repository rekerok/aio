from modules.web3Client import Web3Client
import utils
import random
import config
from typing import Union
from loguru import logger
from modules.account import Account
from utils import Token_Amount, Token_Info
from utils.enums import (
    NETWORK_FIELDS,
    PARAMETR,
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)


class Transfers:
    def __init__(
        self,
        private_key: str,
        network: dict,
        value: tuple[Union[int, float]],
        type_transfer: TYPES_OF_TRANSACTION,
        to_address: str = None,
        token: config.Token = None,
        min_balance: float = 0,
    ) -> None:
        self.acc = Account(private_key=private_key, network=network)
        self.value = value
        self.type_transfer = type_transfer
        self.to_address = to_address
        self.token = token
        self.min_balance = min_balance

    async def _make_tranfer_percent(
        self, balance: Token_Amount, token_info: Token_Info
    ) -> None:
        percent = random.uniform(self.value[0], self.value[1])
        amount_to_send = Token_Amount(
            amount=balance.ether * percent / 100,
            decimals=token_info.decimals,
        )
        logger.info(f"PERCENT: {percent} %")
        logger.info(f"BALANCE: {balance.ether} {token_info.symbol}")
        logger.info(f"SEND: {amount_to_send.ether} {token_info.symbol}")

        return await self.acc.transfer(
            to_address=self.to_address,
            amount=amount_to_send,
            token_address=token_info.address,
        )

    async def _make_tranfer_all_amount(
        self, balance: Token_Amount, token_info: Token_Info
    ) -> None:
        kepp_amount = Token_Amount(
            amount=random.uniform(*self.value), decimals=token_info.decimals
        )
        amount_to_send = Token_Amount(
            amount=balance.ether - kepp_amount.ether, decimals=token_info.decimals
        )
        logger.info(f"BALANCE: {balance.ether} {token_info.symbol}")
        logger.info(f"SEND: {balance.ether-kepp_amount.ether} {token_info.symbol}")
        if kepp_amount.ether > balance.ether:
            logger.error(f"Keep amount {kepp_amount.ether} > {balance.ether}")
            return RESULT_TRANSACTION.FAIL

        return await self.acc.transfer(
            to_address=self.to_address,
            amount=amount_to_send,
            token_address=token_info.address,
        )

    async def _transfer_amount(
        self, balance: Token_Amount, token_info: Token_Info
    ) -> None:
        amount_to_send = random.uniform(self.value[0], self.value[1])
        amount_to_send = Token_Amount(
            amount=amount_to_send, decimals=token_info.decimals
        )
        logger.info(f"BALANCE: {balance.ether} {token_info.symbol}")
        logger.info(f"SEND: {amount_to_send.ether} {token_info.symbol}")

        if amount_to_send.wei > balance.wei:
            logger.error(f"BALANCE: {balance.ether} < {amount_to_send}")
            return RESULT_TRANSACTION.FAIL
        return await self.acc.transfer(
            to_address=self.to_address,
            amount=amount_to_send,
            token_address=token_info.address,
        )

    async def make_transfer(
        self,
    ):
        try:
            token_info: Token_Info = await Token_Info.get_info_token(
                acc=self.acc, token_address=self.token.address
            )
            balance: Token_Amount = await self.acc.get_balance(token_info.address)
            logger.info(f"FROM: {self.acc.address}")
            logger.info(f"TO: {self.to_address}")
            logger.info(f"NETWORK: {self.acc.network.get(NETWORK_FIELDS.NAME)}")
            logger.info(f"TOKEN: {token_info.symbol}")

            if balance.ether < self.min_balance:
                logger.error(f"BALANCE: {balance.ether} < {self.min_balance}")
                return RESULT_TRANSACTION.FAIL

            if self.type_transfer == TYPES_OF_TRANSACTION.PERCENT:
                return await self._make_tranfer_percent(
                    balance=balance, token_info=token_info
                )
            elif self.type_transfer == TYPES_OF_TRANSACTION.ALL_BALANCE:
                return await self._make_tranfer_all_amount(
                    balance=balance, token_info=token_info
                )
            else:
                return await self._transfer_amount(
                    balance=balance, token_info=token_info
                )
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL

    @staticmethod
    async def create_database(wallets: list[tuple], settings):
        database: list[dict] = list()
        for param in settings.PARAMS:
            for wallet in wallets:
                acc = Account(private_key=wallet[0], network=param.get(PARAMETR.NETWORK))
                allow_transaction, balance, token_info = (
                    await Web3Client.check_min_balance(
                        acc=acc,
                        token=param.get(PARAMETR.TOKEN),
                        min_balance=param.get(PARAMETR.MIN_BALANCE),
                    )
                )
                if allow_transaction:
                    database.append(
                        {
                            "private_key": wallet[0],
                            "recipient": wallet[1],
                            "network": param.get(PARAMETR.NETWORK),
                            "token": param.get(PARAMETR.TOKEN),
                            "min_balance": param.get(PARAMETR.MIN_BALANCE),
                            "type_transfer": param.get(PARAMETR.TYPE_TRANSACTION),
                            "value": param.get(PARAMETR.VALUE),
                        }
                    )
                    logger.success(
                        f"{acc.address} ({round(balance.ether,3)} {token_info.symbol}) ({param.get(PARAMETR.NETWORK)[NETWORK_FIELDS.NAME]}) add to DB"
                    )
                else:
                    logger.error(
                        f"{acc.address} ({round(balance.ether,3)} {token_info.symbol}) ({param.get(PARAMETR.NETWORK)[NETWORK_FIELDS.NAME]}) don't add to DB"
                    )
        return database

    @staticmethod
    async def transfer_use_database(settings):
        wallets = await utils.files.get_wallets_recipients(
            wallets_path=(
                "files/wallets.txt"
                if settings.WALLETS_FILE == ""
                else settings.WALLETS_FILE
            ),
            recipients_path=(
                "files/recipients.txt"
                if settings.RECIPIENTS_FILE == ""
                else settings.RECIPIENTS_FILE
            ),
        )
        if wallets is None:
            logger.error("FAIL GET WALLETS")
            return
        database = await Transfers.create_database(wallets=wallets, settings=settings)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        counter = 1
        for data in database:
            logger.warning(f"OPERATION {counter}/{len(database)}")
            tranfer = Transfers(
                private_key=data.get("private_key"),
                network=data.get("network"),
                type_transfer=data.get("type_transfer"),
                to_address=data.get("recipient"),
                token=data.get("token"),
                value=data.get("value"),
                min_balance=data.get("min_balance"),
            )
            result = await tranfer.make_transfer()
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

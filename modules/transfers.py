import random
from utils import *
from typing import Union
from loguru import logger
from helpers import Token_Amount, Token_Info, Token_Info
from .account import Account


class Transfers:
    def __init__(
        self,
        private_key: str,
        network: dict,
        value: tuple[Union[int, float]],
        type_transfer: TYPE_OF_TRANSACTION,
        to_address: str = None,
        token_address: str = None,
        min_balance: float = 0,
    ) -> None:
        self.acc = Account(private_key=private_key, network=network)
        self.value = value
        self.type_transfer = type_transfer
        self.to_address = to_address
        self.token_adress = token_address
        self.min_balance = min_balance

    async def _make_tranfer_percent(
        self, balance: Token_Amount, token_info: Token_Info
    ) -> None:
        percent = random.uniform(self.value[0], self.value[1])
        amount_to_send = Token_Amount(
            amount=balance.ETHER * percent / 100,
            decimals=token_info.decimals,
        )
        logger.info(f"Percentage of balance - {percent} %")
        logger.info(f"Balance {balance.ETHER} {token_info.symbol}")
        logger.info(f"Will send {amount_to_send.ETHER} {token_info.symbol}")
        logger.info(
            f"Remainder {balance.ETHER-amount_to_send.ETHER} {token_info.symbol}"
        )
        await self.acc.transfer(
            to_address=self.to_address,
            amount=amount_to_send,
            token_address=self.token_adress,
        )

    async def _make_tranfer_all_amount(
        self, balance: Token_Amount, token_info: Token_Info
    ) -> None:
        kepp_amount = random.uniform(self.value[0], self.value[1])
        amount_to_send = Token_Amount(
            amount=balance.ETHER - kepp_amount, decimals=token_info.decimals
        )
        logger.info(f"Balance {balance.ETHER} {token_info.symbol}")
        logger.info(f"Remainder {kepp_amount} {token_info.symbol}")
        if kepp_amount > balance.ETHER:
            logger.info(f"Keep amount {kepp_amount} > {balance.ETHER}")
            return

        amount_to_send = balance.ETHER - kepp_amount
        logger.info(f"Will send {amount_to_send} {token_info.symbol}")
        await self.acc.transfer(
            to_address=self.to_address,
            amount=amount_to_send,
            token_address=self.token_adress,
        )

    async def _transfer_amount(
        self, balance: Token_Amount, token_info: Token_Info
    ) -> None:
        amount_to_send = random.uniform(self.value[0], self.value[1])
        logger.info(f"Balance {balance.ETHER} {token_info.symbol}")
        if amount_to_send > balance.ETHER:
            logger.error(f"Balance {balance.ETHER} < {amount_to_send}")
            return

        logger.info(f"Будет отправлено {amount_to_send} {token_info.symbol}")
        logger.info(f"Remainder {balance.ETHER - amount_to_send} {token_info.symbol}")
        await self.acc.transfer(
            to_address=self.to_address,
            amount=amount_to_send,
            token_address=self.token_adress,
        )

    async def make_transfer(self):
        token_info: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=self.token_adress
        )
        balance: Token_Amount = await self.acc.get_balance(self.token_adress)
        logger.info(f"FROM: {self.acc.address}")
        logger.info(f"TO: {self.to_address}")
        logger.info(f"NETWORK: {self.acc.network.get('name')}")
        logger.info(f"TOKEN: {token_info.symbol}")
        logger.info(f"Starting to make transfer")
        if balance.ETHER < self.min_balance:
            logger.error(f"Balance {balance.ETHER} < {self.min_balance}")
            return

        if self.type_transfer == TYPE_OF_TRANSACTION.PERCENT:
            await self._make_tranfer_percent(balance=balance, token_info=token_info)
        elif self.type_transfer == TYPE_OF_TRANSACTION.AMOUNT:
            await self._make_tranfer_all_amount(balance=balance, token_info=token_info)
        else:
            await self._transfer_amount(balance=balance, token_info=token_info)

    @staticmethod
    async def create_database(wallets: list[tuple], settings):
        database: list[dict] = list()
        for param in settings.params:
            for wallet in wallets:
                database.append(
                    {
                        "private_key": wallet[0],
                        "recipient": wallet[1],
                        "network": param.get("network"),
                        "token_address": param.get("token"),
                        "min_balance": param.get("min_balance"),
                        "type_transfer": param.get("type_transfer"),
                        "value": param.get("value"),
                    }
                )
        return database

    @staticmethod
    async def transfer_use_database(settings):
        wallets = await files.get_wallets_recipients(
            wallets_path="files/wallets.txt", recipients_path="files/recipients.txt"
        )
        database = await Transfers.create_database(wallets=wallets, settings=settings)
        random.shuffle(database)

        for data in database:
            tranfer = Transfers(
                private_key=data.get("private_key"),
                network=data.get("network"),
                type_transfer=data.get("type_transfer"),
                to_address=data.get("recipient"),
                token_address=data.get("token_address"),
                value=data.get("value"),
                min_balance=data.get("min_balance"),
            )
            await tranfer.make_transfer()
            await time.sleep_view(settings.SLEEP)

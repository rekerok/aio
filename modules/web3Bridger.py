import random

import eth_account
import eth_account.account
import config
from typing import Union
from loguru import logger
from abc import abstractmethod
from modules.account import Account
from modules.web3Client import Web3Client
from settings import Client_Networks
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

    async def _get_to_token(
        self, to_chain: config.Network, to_token_address: str
    ) -> Token_Info:
        found_variable = None
        for network_name, network_dict in Client_Networks.__dict__.items():
            if (
                isinstance(network_dict, dict)
                and network_dict.get(NETWORK_FIELDS.NAME) == to_chain.get(NETWORK_FIELDS.NAME)
            ):
                found_variable = network_name
                break
        network_dict = getattr(Client_Networks, found_variable)
        if network_dict:
            to_token = await Token_Info.get_info_token(
                acc=Account(network=network_dict), token_address=to_token_address
            )
            if to_token:
                return to_token
            else:
                return None
        else:
            return None

    async def _get_to_network(self, to_chain: config.Network) -> Client_Networks:
        found_variable = None
        for network_name, network_dict in Client_Networks.__dict__.items():
            if (
                isinstance(network_dict, dict)
                and network_dict.get(NETWORK_FIELDS.NAME) == to_chain.get(NETWORK_FIELDS.NAME)
            ):
                found_variable = network_name
                break
        return getattr(Client_Networks, found_variable)
    
    async def _make_bridge_percent(
        self,
        from_token: Token_Info,
        balance: Token_Amount,
    ):
        percent = random.uniform(self.value[0], self.value[1])
        amount_to_send = Token_Amount(
            balance.ether * percent / 100, decimals=from_token.decimals
        )

        logger.info(f"PERCENT: {percent} %")
        logger.info(f"SEND: {amount_to_send.ether} {from_token.symbol}")

        return amount_to_send

    async def _make_bridge_all_balance(
        self,
        from_token: Token_Info,
        balance: Token_Amount,
    ):
        keep_amount = Token_Amount(
            amount=random.uniform(self.value[0], self.value[1]),
            decimals=from_token.decimals,
        )
        amount_to_send = Token_Amount(
            amount=balance.ether - keep_amount.ether, decimals=from_token.decimals
        )

        if keep_amount.ether > balance.ether:
            logger.error(f"KEEP AMOUNT:  {keep_amount.ether} > {balance.ether} BALANCE")
            return None

        logger.info(f"BALANCE: {balance.ether} {from_token.symbol}")
        logger.info(f"SEND: {amount_to_send.ether} {from_token.symbol}")

        return amount_to_send

    async def _make_bridge_amount(
        self,
        from_token: Token_Info,
        balance: Token_Amount,
    ):
        amount_to_send = Token_Amount(
            amount=random.uniform(self.value[0], self.value[1]),
            decimals=from_token.decimals,
        )

        if amount_to_send.ether > balance.ether:
            logger.error(f"BALANCE: {balance.ether} < {amount_to_send.ether} SEND")
            return None

        logger.info(f"SEND: {amount_to_send.ether} {from_token.symbol}")

        return amount_to_send

    @abstractmethod
    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
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
        from_token: config.Token,
        to_token: config.Token,
        to_network: config.Network,
    ):
        from_token: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=from_token.address
        )

        to_token: Token_Info = await self._get_to_token(
            to_chain=to_network, to_token_address=to_token.address
        )

        if not from_token or not to_token:
            return RESULT_TRANSACTION.FAIL
        balance: Token_Amount = await self.acc.get_balance(from_token.address)
        if balance is None:
            logger.warning("CHECK PROXY")
            return RESULT_TRANSACTION.FAIL
        logger.info(f"WALLET: {self.acc.address}")
        logger.info(
            f"{self.acc.network.get(NETWORK_FIELDS.NAME)} ({from_token.symbol}) -> {to_network.get(NETWORK_FIELDS.NAME)} ({to_token.symbol})"
        )
        logger.info(f"DEX: {self.NAME} ")
        if balance.ether < self.min_balance:
            logger.error(f"Balance {balance.ether} < {self.min_balance}")
            return RESULT_TRANSACTION.FAIL

        func_bridge = await self._choice_type_transaction()

        amount_to_send = await func_bridge(
            from_token=from_token,
            balance=balance,
        )

        if amount_to_send is None or not await Web3Client.wait_gas(acc=self.acc):
            return RESULT_TRANSACTION.FAIL

        return await self._perform_bridge(
            amount_to_send=amount_to_send,
            from_token=from_token,
            to_chain=to_network,
            to_token=to_token,
        )

    @staticmethod
    async def _create_database(wallets: list[str], params):
        database = list()
        for param in params:
            for wallet in wallets:
                try:
                    address = eth_account.account.Account.from_key(wallet).address
                    logger.info(("-" * 5) + " " + address)
                    logger.info(f"MIN = {param.get(PARAMETR.MIN_BALANCE)}")
                    valid_networks = []
                    for data in param.get(PARAMETR.FROM_DATA):
                        acc = Account(
                            private_key=wallet, network=data.get(PARAMETR.NETWORK)
                        )
                        token_info: Token_Info = await Token_Info.get_info_token(
                            acc=acc, token_address=data[PARAMETR.FROM_TOKEN].address
                        )
                        balance = await acc.get_balance(
                            token_address=data[PARAMETR.FROM_TOKEN].address
                        )
                        if balance.ether > param.get(PARAMETR.MIN_BALANCE):
                            valid_networks.append(
                                {
                                    "token_info": token_info,
                                    "balance": balance,
                                    "token": data[PARAMETR.FROM_TOKEN],
                                    "network": data.get(PARAMETR.NETWORK),
                                }
                            )
                            logger.success(
                                f"{data.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)} {balance.ether} {token_info.symbol}"
                            )
                        else:
                            logger.error(
                                f"{data.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)} {balance.ether} {token_info.symbol}"
                            )
                    if len(valid_networks) == 0:
                        logger.error(f"{acc.address} WITHOUT TRANSACTION")
                        continue
                    from_data = random.choice(valid_networks)
                    to_data = random.choice(param.get(PARAMETR.TO_DATA))
                    acc = Account(private_key=wallet, network=from_data.get("network"))

                    database.append(
                        {
                            "private_key": wallet,
                            "network": from_data.get("network"),
                            "dex": random.choice(to_data.get(PARAMETR.DEXES)),
                            "type_bridge": param.get(PARAMETR.TYPE_TRANSACTION),
                            "value": param.get(PARAMETR.VALUE),
                            "from_token": from_data.get("token"),
                            "min_balance": param.get(PARAMETR.MIN_BALANCE),
                            "to_network": to_data.get(PARAMETR.NETWORK),
                            "to_token": to_data.get(PARAMETR.TO_TOKEN),
                        }
                    )
                    logger.success(
                        f"{acc.address} ({round(balance.ether,3)} {token_info.symbol}) ({from_data['network'][NETWORK_FIELDS.NAME]}) add to DB"
                    )

                    logger.info("-" * 5)
                except Exception as error:
                    logger.error(f"{acc.address} WITHOUT TRANSACTION")
                    logger.error(error)
                    logger.info("-" * 5)
                    continue
        return database

    @staticmethod
    async def swap_use_database(settings, wallets: list[str] = None):
        if wallets is None:
            wallets = await utils.files.read_file_lines(
                path="files/wallets.txt",
            )
        database = await Web3Bridger._create_database(
            wallets=wallets, params=settings.PARAMS
        )
        random.shuffle(database)

        counter = 1
        for data in database:
            logger.warning(f"OPERATION {counter}/{len(database)}")
            dex_class = data.get("dex")
            dex = dex_class(
                private_key=data.get("private_key"),
                network=data.get("network"),
                type_transfer=data.get("type_bridge"),
                value=data.get("value"),
                min_balance=data.get("min_balance"),
                slippage=settings.SLIPPAGE,
            )
            result = await dex.bridge(
                from_token=data.get("from_token"),
                to_token=data.get("to_token"),
                to_network=data.get("to_network"),
            )
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

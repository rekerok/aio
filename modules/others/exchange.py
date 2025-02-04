import csv
import pprint
import random
import time
import ccxt
from loguru import logger
import utils
from utils.enums import PARAMETR


class Exchange:
    def __init__(
        self,
        apikey: str = None,
        secret: str = None,
        password: str = None,
    ) -> None:
        self._apikey = apikey
        self._secret = secret
        self._password = password

    async def withdraw_from_sub_accs(self): ...
    async def get_balances(self): ...
    async def _get_data_network(self, currency: str, chain: str): ...
    async def withdraw(
        self, address: str, currency: str, chain: str, amount: float
    ): ...
    async def create_file_csv(self): ...


class OKX(Exchange):
    def __init__(
        self, apikey: str = None, secret: str = None, password: str = None
    ) -> None:
        super().__init__(apikey, secret, password)
        self.okx = ccxt.okx(
            {
                "apiKey": self._apikey,
                "secret": self._secret,
                "password": self._password,
                "enableRateLimit": True,
            }
        )

    async def withdraw_from_sub_accs(
        self,
    ):
        subacc_list = self.okx.private_get_users_subaccount_list()

        for subacc_data in subacc_list["data"]:
            try:
                subacc_name = subacc_data["subAcct"]
                balances_data = self.okx.private_get_asset_subaccount_balances(
                    params={"subAcct": subacc_name}
                )["data"]
                if len(balances_data) == 0:
                    logger.info(f"{subacc_name} IS CLEAR")
                for currency_data in balances_data:
                    balance = currency_data["availBal"]
                    ccy = currency_data["ccy"]
                    try:
                        self.okx.private_post_asset_transfer(
                            params={
                                "type": 2,  # from subacc to main
                                "ccy": ccy,  # currency
                                "amt": balance,  # amount
                                "from": 6,  # funding acc
                                "to": 6,  # funding acc
                                "subAcct": subacc_name,  # subacc_name
                            }
                        )
                        logger.success(
                            f"FROM {subacc_name} TO MAIN TRANSFET {balance} {ccy}"
                        )
                    except Exception as error:
                        logger.error(error)
            except Exception as error:
                logger.error(error)

    async def get_balances(self):
        try:
            await self.withdraw_from_sub_accs()
            balances = self.okx.fetch_balance(params={"type": "funding"})["info"][
                "data"
            ]
            data = []
            for i in balances:
                price = float(
                    1
                    if i["ccy"] == "USDT"
                    else self.okx.fetch_ticker(f"{i['ccy']}/USDT")["last"]
                )
                data.append(
                    {
                        "symbol": i["ccy"],
                        "balance": float(i["availBal"]),
                        "price": price,
                        "amount": float(i["availBal"]) * price,
                    }
                )
            return data
        except Exception as error:
            logger.error(error)
            return None

    async def _get_data_network(self, currency: str, chain: str):
        try:
            data = self.okx.fetch_currencies()[currency]["networks"][chain]
            return data
        except:
            logger.error("don't get fee")
            return None

    async def withdraw(self, address: str, currency: str, chain: str, amount: float):
        try:
            await self.withdraw_from_sub_accs()
            data_network = await self._get_data_network(currency=currency, chain=chain)
            id = self.okx.withdraw(
                code=currency,
                amount=amount,
                address=address,
                tag=None,
                params={
                    "dest": 4,
                    "fee": data_network["fee"],
                    "chain": data_network["id"],
                },
            )["info"]["wdId"]
            logger.success(f"Withdraw {amount} {currency}-{chain} to {address}"),
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def create_file_csv(self):
        try:
            with open("files/okx.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(("token", "network", "fee", "min", "max"))
                currencies = self.okx.fetch_currencies()
                for token, data in currencies.items():
                    for network, date_network in data["networks"].items():
                        if date_network["active"]:
                            fee = date_network["fee"]
                            min_output = date_network["limits"]["withdraw"]["min"]
                            max_output = date_network["limits"]["withdraw"]["max"]
                            data = date_network["id"].split("-")
                            token, chain = data[0], "-".join(data[1:])
                            logger.info(
                                (
                                    token,
                                    chain,
                                    fee,
                                    min_output,
                                    max_output,
                                )
                            )
                            writer.writerow(
                                (
                                    token,
                                    chain,
                                    fee,
                                    min_output,
                                    max_output,
                                )
                            )
            logger.success("CREATE okx.csv")
        except Exception as e:
            logger.error(e)


class Bitget(Exchange):
    def __init__(
        self, apikey: str = None, secret: str = None, password: str = None
    ) -> None:
        super().__init__(apikey, secret, password)
        self.bitget = ccxt.bitget(
            {
                "apiKey": self._apikey,
                "secret": self._secret,
                "password": self._password,
                "enableRateLimit": True,
                "options": {"defaultType": "spot"},
            }
        )

    async def withdraw_from_sub_accs(
        self,
    ):
        info = self.bitget.privateSpotGetV2SpotAccountSubaccountAssets()
        main_user = self.bitget.privateSpotGetV2SpotAccountInfo()
        for asset in info["data"]:
            for balance in asset["assetsList"]:
                try:
                    self.bitget.privateSpotPostV2SpotWalletSubaccountTransfer(
                        params={
                            "fromType": "spot",
                            "toType": "spot",
                            "amount": balance["available"],
                            "coin": balance["coin"],
                            "fromUserId": asset["userId"],
                            "toUserId": main_user["data"]["userId"],
                        }
                    )
                    logger.success(
                        f"TRANSFER {balance['available']} {balance['coin']} TO MAIN ACC"
                    )
                except Exception as error:
                    logger.error(error)
                    logger.error(
                        f"ERROR WITHDRAW {balance['available']} {balance['coin']} TO MAIN ACC"
                    )

    async def get_balances(self):
        await self.withdraw_from_sub_accs()
        try:
            balances = self.bitget.fetch_balance()["info"]

            data = []
            for i in balances:
                price = float(
                    1
                    if i["coin"] == "USDT"
                    else self.bitget.fetch_ticker(f"{i['coin']}/USDT")["last"]
                )
                data.append(
                    {
                        "symbol": i["coin"],
                        "balance": float(i["available"]),
                        "price": price,
                        "amount": float(i["available"]) * price,
                    }
                )
                logger.info(
                    f"FIND {i['available']} {i['coin']}\t=\t{round(float(i['available']) * price,2)} USD"
                )
            return data
        except Exception as error:
            logger.error(error)
            return None

    async def _get_status_withdraw(self, id: str):
        try:
            time_now = int(time.time())

            withdraw_data = self.bitget.privateSpotGetSpotV1WalletWithdrawalList(
                {
                    "startTime": str(1),
                    "endTime": str(time_now),
                    # "orderId": id,
                }
            )
            print(withdraw_data)
        except Exception as error:
            logger.error(error)
            return None

    async def withdraw(self, address: str, currency: str, chain: str, amount: float):
        try:
            await self.withdraw_from_sub_accs()
            id = self.bitget.withdraw(
                code=currency,
                amount=amount,
                address=address,
                tag=None,
                params={"network": chain},
            )["info"]["data"]["orderId"]
            print(id)
            # await self._get_status_withdraw(id=id)
            logger.success(f"Withdraw {amount} {currency}-{chain} to {address}"),
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def create_file_csv(self):
        data = self.bitget.fetch_currencies()
        try:
            with open("files/bitget.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        "token",
                        "network",
                        "fee",
                        "min",
                    )
                )
                for token, info_token in data.items():
                    for network, info_network in info_token["networks"].items():
                        if info_network["active"]:
                            fee = info_network["fee"]
                            min_output = info_network["limits"]["withdraw"]["min"]
                            writer.writerow(
                                (
                                    info_token["code"],
                                    info_network["network"],
                                    f"{format(fee, 'f')} ",
                                    f"{format(min_output, 'f')}",
                                )
                            )
            logger.success("CREATE bitget.csv")
        except Exception as e:
            logger.error(e)


class Binance(Exchange):
    def __init__(
        self, apikey: str = None, secret: str = None, password: str = None
    ) -> None:
        super().__init__(apikey, secret, password)
        self.binance = ccxt.binance(
            {
                "apiKey": self._apikey,
                "secret": self._secret,
                "enableRateLimit": True,
                "options": {"defaultType": "spot"},
            }
        )

    async def withdraw_from_sub_accs(self):
        data = self.binance.sapiGetSubAccountList()
        for mail in data["subAccounts"]:
            for balance in self.binance.sapiV4GetSubAccountAssets(
                params={"email": mail["email"]}
            )["balances"]:
                try:

                    if float(balance["free"]) > 0:
                        params = {
                            "fromEmail": mail["email"],
                            "asset": balance["asset"],
                            "amount": balance["free"],
                            "fromAccountType": "SPOT",
                            "toAccountType": "SPOT",
                            # "timestamp": int(time.time()),
                        }
                        self.binance.sapiPostSubAccountUniversalTransfer(params=params)
                        logger.success(
                            f"WITHDRAW {balance['free']} {balance['asset']} TO MAIN ACCOUNT"
                        )
                except Exception as error:
                    logger.error(error)

    async def get_balances(self):
        try:
            await self.withdraw_from_sub_accs()
            balances = self.binance.fetch_balance()
            data = []
            for token, balance in balances["free"].items():
                if balance > 0:
                    try:
                        price = float(
                            1
                            if token == "USDT"
                            else self.binance.fetch_ticker(f"{token}/USDT")["last"]
                        )
                    except Exception as error:
                        logger.error(error)
                        price = 0
                    data.append(
                        {
                            "symbol": token,
                            "balance": float(balance),
                            "price": price,
                            "amount": float(balance) * price,
                        }
                    )
            return data
        except Exception as error:
            logger.error(error)

    async def withdraw(
        self, address: str, currency: str, chain: str, amount: float
    ): ...

    async def create_file_csv(self):
        try:
            with open("files/binance.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(("token", "network", "fee", "min", "max"))
                for token, data in self.binance.fetch_currencies().items():
                    for network, date_network in data["networks"].items():
                        if date_network["active"]:
                            fee = date_network["fee"]
                            min_output = date_network["limits"]["withdraw"]["min"]
                            max_output = date_network["limits"]["withdraw"]["max"]
                            writer.writerow(
                                (
                                    token,
                                    network,
                                    fee,
                                    min_output,
                                    max_output,
                                )
                            )
            logger.success("CREATE binance.csv")
        except Exception as e:
            logger.error(e)


async def withdraw_use_database(settings):
    exchange = settings.DATA[0][PARAMETR.TYPE_EXCHANGE](
        apikey=settings.DATA[0][PARAMETR.API_KEY],
        secret=settings.DATA[0][PARAMETR.API_SECRET],
        password=settings.DATA[0][PARAMETR.PASSWORD],
    )
    recipients = await utils.files.read_file_lines("files/recipients.txt")
    random.shuffle(recipients)
    for recipient in recipients:
        token = random.choice(settings.PARAMS[PARAMETR.TOKENS])
        if await exchange.withdraw(
            address=recipient,
            currency=token[PARAMETR.TOKEN],
            chain=token[PARAMETR.NETWORK],
            amount=round(
                random.uniform(
                    settings.PARAMS[PARAMETR.VALUE][0],
                    settings.PARAMS[PARAMETR.VALUE][1],
                ),
                random.randint(
                    settings.PARAMS[PARAMETR.ROUND][0],
                    settings.PARAMS[PARAMETR.ROUND][1],
                ),
            ),
        ):
            await utils.time.sleep_view(settings.SLEEP)
        else:
            await utils.time.sleep_view((5, 7))


async def create_file_csv(settings):
    exchange = settings.DATA[0][PARAMETR.TYPE_EXCHANGE](
        apikey=settings.DATA[0][PARAMETR.API_KEY],
        secret=settings.DATA[0][PARAMETR.API_SECRET],
        password=settings.DATA[0][PARAMETR.PASSWORD],
    )
    await exchange.create_file_csv()

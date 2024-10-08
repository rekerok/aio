import csv
import ccxt
from loguru import logger
import time
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
                currency,
                amount,
                address,
                {
                    "ccy": currency,
                    "amt": f"{amount}",
                    "dest": 4,
                    "toAddr": address,
                    "fee": currency,
                    "chain": chain,
                    "pwd": "-",
                },
            )["info"]["wdId"]
            logger.success(f"Withdraw {amount} {currency}-{chain} to {address}"),
        except Exception as e:
            logger.error(e)

    async def create_file_csv(self):
        try:
            with open("files/okx.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow(("token", "network", "fee", "min", "max"))
                for token, data in self.okx.fetch_currencies().items():
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
            logger.success("CREATE okx.csv")
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
    await exchange.withdraw_from_sub_accs()
    await exchange.create_file_csv()
    # await exchange.withdraw(
    #     address="",
    #     currency="USDT",
    #     chain="ARBONE",
    #     amount=1,
    # )

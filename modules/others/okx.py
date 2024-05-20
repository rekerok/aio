import csv
import ccxt
import utils
import random
from loguru import logger
from utils.enums import PARAMETR


class OKX:
    def __init__(
        self,
        apiKey: str,
        secret: str,
        password: str,
        check_send,
        proxy: str = None,
        attempt=15,
    ) -> None:
        self.okx = ccxt.okx(
            {
                "apiKey": apiKey,
                "secret": secret,
                "password": password,
                "enableRateLimit": True,
                "proxy": proxy,
            }
        )
        self.count_attempt = attempt
        self.check_send = check_send

    async def _get_data(self, currency: str = None, chain: str = None):
        try:
            if chain == "Avalanche C-Chain":
                chain = "Avalanche C"
            if chain == "Avalanche X-Chain":
                chain = "Avalanche X"
            return self.okx.fetch_currencies()[currency]["networks"][chain]
        except:
            logger.error("don't get fee")
            return None

    async def _wait_status_withdraw(self, id: str):
        try:
            attempt = 1
            while True:
                if attempt > self.count_attempt:
                    raise (
                        Exception(
                            "[OKX] Wait for withdrawal final status attempts limit exceeded."
                        )
                    )

                logger.info(f"ATTEMPT {attempt}/{self.count_attempt}")

                status = self.okx.private_get_asset_deposit_withdraw_status(
                    params={"wdId": id}
                )

                if "Cancellation complete" in status["data"][0]["state"]:
                    raise Exception("f[OKX] Withdrawal cancelled")

                if "Withdrawal complete" not in status["data"][0]["state"]:
                    attempt = attempt + 1
                    logger.debug("WAIT SEND 60 SEC")
                    await utils.time.sleep_view((60, 60))
                else:
                    logger.info("[OKX] Withdraw by OKX side was completed")
                    return True

        except Exception as e:
            raise Exception(f"[OKX] Wait for withdrawal final status error: {e}")

    async def withdraw(self, address: str, currency: str, chain: str, amount: float):
        try:
            await self.withdraw_from_subaccs()
            data_chains = await self._get_data(currency=currency, chain=chain)
            logger.info(f"start withdraw {amount} {data_chains['id']} to {address}")
            # 0.0006
            id = self.okx.withdraw(
                currency,
                amount,
                address,
                {
                    "ccy": currency,
                    "amt": f"{amount}",
                    "dest": 4,
                    "toAddr": address,
                    "fee": fee,
                    "chain": data_chains["id"],
                    "pwd": "-",
                },
            )["info"]["wdId"]
            if self.check_send:
                await self._wait_status_withdraw(id=id)
            logger.success(f"Withdraw {amount} {currency}-{chain} to {address}"),
        except Exception as e:
            logger.error(e)

    async def withdraw_from_subaccs(self):
        subacc_list = self.okx.private_get_users_subaccount_list()
        for subacc_data in subacc_list["data"]:
            try:
                subacc_name = subacc_data["subAcct"]
                for currency_data in self.okx.private_get_asset_subaccount_balances(
                    params={"subAcct": subacc_name}
                )["data"]:
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
                        logger.info(
                            f"from {subacc_name} to MAIN transfer {balance} {ccy}"
                        )
                    except Exception as error:
                        logger.error(error)
            except Exception as error:
                logger.error(error)

    @staticmethod
    async def create_database(wallets: list[str], params: list[dict]) -> list[dict]:
        database: list[dict] = list()
        for param in params:
            for wallet in (
                wallets
                if param[PARAMETR.RECIPIENTS_FILE] == ""
                else await utils.files.read_file_lines(param[PARAMETR.WALLETS_FILE])
            ):
                round_number = random.randint(*param[PARAMETR.ROUND])
                amount = round(
                    random.uniform(*param[PARAMETR.VALUE]),
                    round_number,
                )
                database.append(
                    {
                        "address": wallet,
                        "token": random.choice(param[PARAMETR.TOKENS]),
                        "amount": amount,
                    }
                )
        return database

    @staticmethod
    async def withdraw_use_database(settings):
        wallets = await utils.files.read_file_lines("files/recipients.txt")
        database = await OKX.create_database(wallets=wallets, params=settings.PARAMS)

        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)

        okx = OKX(
            apiKey=settings.KEYS.get(PARAMETR.OKX_API_KEY),
            secret=settings.KEYS.get(PARAMETR.OKX_API_SECRET),
            password=settings.KEYS.get(PARAMETR.OKX_PASSWORD),
            proxy=settings.PROXY,
            attempt=settings.ATTEMPT_WAIT_WITHDRAW,
            check_send=settings.WAIT_TO_SEND,
        )
        counter = 1
        for wallet in database:
            logger.info(f"OPERATION {counter}/{len(database)}")
            await okx.withdraw(
                address=wallet["address"],
                amount=wallet["amount"],
                chain=wallet["token"].NETWORK,
                currency=wallet["token"].EXCHANGE_NAME,
            )
            await utils.time.sleep_view(settings.SLEEP)
            logger.info("------------------------------------")
            counter += 1


def create_file_csv(okx):
    with open("files/okx.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(("token", "network", "fee", "min", "max"))
        for token, data in okx.fetch_currencies().items():
            for network, date_network in data["networks"].items():
                if date_network["active"]:
                    fee = date_network["fee"]
                    min_output = date_network["limits"]["withdraw"]["min"]
                    max_output = date_network["limits"]["withdraw"]["max"]
                    if network == "Avalanche C":
                        network = "Avalanche C-Chain"
                    if network == "Avalanche X":
                        network = "Avalanche X-Chain"
                    writer.writerow((token, network, fee, min_output, max_output))

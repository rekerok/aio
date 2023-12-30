import utils
import random
from loguru import logger
from utils.enums import PARAMETR, RESULT_TRANSACTION
from modules.account import Account


class WarmUpRefuel:
    @staticmethod
    async def _create_database(wallets: list[str], params: dict):
        database = list()
        for reful_app, networks in params.items():
            for network in networks:
                for wallet in (
                    wallets
                    if network.get(PARAMETR.WALLETS_FILE) == ""
                    else await utils.files.read_file_lines(
                        network.get(PARAMETR.WALLETS_FILE)
                    )
                ):
                    for i in range(
                        random.randint(*network.get(PARAMETR.COUNT_TRANSACTION))
                    ):
                        database.append(
                            {
                                "private_key": wallet,
                                "network": network.get(PARAMETR.NETWORK),
                                "refuel_app": reful_app,
                                "dst_data": random.choice(
                                    network.get(PARAMETR.TO_CHAINS)
                                ),
                            }
                        )
        return database

    @staticmethod
    async def get_fees(apps: dict):
        for app, networks in apps.items():
            logger.debug(app.NAME)
            await app.get_fees(networks)
            logger.info("------------------------------------")

    @staticmethod
    async def warm_up_refuel(settings):
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
        database = await WarmUpRefuel._create_database(
            wallets=wallets, params=settings.PARAMS
        )
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        counter = 1
        for data in database:
            logger.info(f"OPERATION {counter}/{len(database)}")

            amount_to_get = data.get("dst_data").get(PARAMETR.VALUE)
            to_chain = data.get("dst_data").get(PARAMETR.NAME)
            refuel_app = data.get("refuel_app")(
                private_key=data.get("private_key"),
                network=data.get("network"),
            )
            result = await refuel_app.refuel(
                amount_to_get=amount_to_get, to_chain=to_chain
            )
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            logger.info("------------------------------------")
            counter += 1

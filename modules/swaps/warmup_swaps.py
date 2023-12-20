import pprint
import random

from loguru import logger
from helpers.enums import TYPE_OF_TRANSACTION
from helpers.web3Swapper import Web3Swapper
import utils


class WarmUPSwaps:
    @staticmethod
    async def _create_database(wallets, params):
        database = list()
        for wallet in wallets:
            for dex, networks in params.items():
                for network in networks:
                    for i in range(random.randint(*network["count_swaps"])):
                        selected_tokens = random.sample(network["tokens"], 2)

                        # Проверяем, что выбраны различные токены
                        while selected_tokens[0] == selected_tokens[1]:
                            selected_tokens = random.sample(network["tokens"], 2)
                        database.append(
                            {
                                "private_key": wallet,
                                "network": network["network"],
                                "dex": dex,
                                "from_token_address": selected_tokens[0]["address"],
                                "to_token_address": selected_tokens[1]["address"],
                                "min_balance": selected_tokens[0]["min_balance"],
                                "value": network["percent_swap"],
                            }
                        )
        return database

    @staticmethod
    async def warmup(settings):
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
        database = await WarmUPSwaps._create_database(
            wallets=wallets, params=settings.params
        )
        pprint.pprint(database)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)

        counter = 1
        for data in database:
            dex: Web3Swapper = data["dex"](
                private_key=data["private_key"],
                network=data["network"],
                type_transfer=TYPE_OF_TRANSACTION.PERCENT,
                value=data["value"],
                min_balance=data["min_balance"],
                slippage=settings.SLIPPAGE,
            )
            logger.info("------------------------")
            logger.info(f"OPERATION {counter}/{len(database)}")
            await dex.swap(
                from_token_address=data["from_token_address"],
                to_token_address=data["to_token_address"],
            )
            counter += 1
            await utils.time.sleep_view(settings.SLEEP)
            logger.info("------------------------")

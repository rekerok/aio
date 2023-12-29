import utils
import random
from loguru import logger
from modules.account import Account
from utils import TYPES_OF_TRANSACTION
from modules.web3Swapper import Web3Swapper
from utils.enums import NETWORK_FIELDS, PARAMETR, RESULT_TRANSACTION


class WarmUPSwaps:
    @staticmethod
    async def _create_database(wallets, params):
        database = list()
        for wallet in wallets:
            for dex, networks in params.items():
                for network in networks:
                    for i in range(
                        random.randint(*network.get(PARAMETR.COUNT_TRANSACTION))
                    ):
                        database.append(
                            {
                                "private_key": wallet,
                                "network": network.get(PARAMETR.NETWORK),
                                "dex": dex,
                                "tokens": network.get(PARAMETR.TOKENS),
                                "value": network.get(PARAMETR.VALUE),
                            }
                        )
        return database

    @staticmethod
    async def warmup(settings):
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
        database = await WarmUPSwaps._create_database(
            wallets=wallets, params=settings.PARAMS
        )
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        random.shuffle(database)
        counter = 1
        for data in database:
            logger.info(f"OPERATION {counter}/{len(database)}")
            acc = Account(
                private_key=data.get("private_key"),
                network=data.get("network"),
            )
            pair_tokens = await Web3Swapper._get_random_pair_for_swap(
                tokens=data.get("tokens"), acc=acc
            )
            if pair_tokens[0] is None or pair_tokens[1] is None:
                logger.info(
                    Account(
                        private_key=data.get("private_key"), network=data.get("network")
                    ).address
                )
                logger.error(
                    f"NOT PAIR FOR SWAP IN {data.get('dex')} {data.get('network').get(NETWORK_FIELDS.NAME)}"
                )
                continue
            dex: Web3Swapper = data["dex"](
                private_key=data.get("private_key"),
                network=data.get("network"),
                type_transfer=TYPES_OF_TRANSACTION.PERCENT,
                value=data.get("value"),
                min_balance=pair_tokens[0].get(PARAMETR.MIN_BALANCE),
                slippage=settings.SLIPPAGE,
            )
            result = await dex.swap(
                from_token_address=pair_tokens[0].get(PARAMETR.TOKEN_ADDRESS),
                to_token_address=pair_tokens[1].get(PARAMETR.TOKEN_ADDRESS),
            )
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            logger.info("------------------------------------")
            counter += 1

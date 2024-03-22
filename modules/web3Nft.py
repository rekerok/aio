from abc import abstractmethod
import random

from loguru import logger
from modules.web3Client import Web3Client
import utils
from utils.enums import NETWORK_FIELDS, PARAMETR, RESULT_TRANSACTION


class Web3Nft(Web3Client):
    def __init__(self, private_key: str, network: dict) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
        )

    @abstractmethod
    async def _perform_mint(self, nft_contract_address: str = None):
        pass

    async def mint(self, nft_contract_address: str = None):
        logger.info(f"WALLET: {self.acc.address}")
        logger.info(f"NETWORK: {self.acc.network.get(NETWORK_FIELDS.NAME)}")
        logger.info(f"DEX: {self.NAME} ")
        return await self._perform_mint(nft_contract_address=nft_contract_address)

    @staticmethod
    async def _create_database(wallets: list[str], params):
        database = list()
        for param in params:
            for wallet in (
                wallets
                if param.get(PARAMETR.WALLETS_FILE) == ""
                else await utils.files.read_file_lines(param.get(PARAMETR.WALLETS_FILE))
            ):
                tmp = random.choice(param.get(PARAMETR.NFTS))
                database.append(
                    {
                        "private_key": wallet,
                        "network": param.get(PARAMETR.NETWORK),
                        "dex": tmp.get(PARAMETR.DEX),
                        "contract": random.choice(tmp.get(PARAMETR.CONTRACTS)),
                    }
                )
        return database

    @staticmethod
    async def mint_use_database(settings, wallets: list[str] = None):
        if wallets is None:
            wallets = await utils.files.read_file_lines(
                path="files/wallets.txt",
            )

        database = await Web3Nft._create_database(
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
            )
            result = await dex.mint(nft_contract_address=data.get("contract"))
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

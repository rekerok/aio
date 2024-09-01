import utils
import random
from loguru import logger
from modules.account import Account
from utils.enums import NETWORK_FIELDS, PARAMETR, RESULT_TRANSACTION


class Deployer:
    def __init__(self, acc: Account, bytecode: str = "0x") -> None:
        self.acc = acc
        self.bytecode = bytecode

    async def make_deploy(
        self,
    ):
        return await self.acc.deploy_contract(self.bytecode)

    @staticmethod
    async def deploy(private_key: str, network: dict, contract: dict):
        acc = Account(private_key=private_key, network=network)
        logger.info(f"FROM {acc.address}")
        logger.info(f"NETWORK {network.get(NETWORK_FIELDS.NAME)}")
        logger.info(f"Name deploy contract {contract.get(PARAMETR.NAME)}")
        deployre = Deployer(acc=acc, bytecode=contract.get(PARAMETR.BYTECODE_CONTRACT))
        return await deployre.make_deploy()

    @staticmethod
    async def create_database(wallets: list[str], params: dict) -> list[dict]:
        database: list[dict] = list()
        for param in params:
            for wallet in wallets:
                for i in range(random.randint(*param.get(PARAMETR.COUNT_TRANSACTION))):
                    deploy_contract = random.choice(param.get(PARAMETR.CONTRACTS))
                    database.append(
                        {
                            "network": param.get(PARAMETR.NETWORK),
                            "private_key": wallet,
                            "contract": deploy_contract,
                        }
                    )
        return database

    @staticmethod
    async def deploy_with_database(settings=None):
        wallets = await utils.files.read_file_lines("files/wallets.txt")
        database = await Deployer.create_database(
            wallets=wallets, params=settings.PARAMS
        )
        random.shuffle(database)
        counter = 1
        for data in database:
            logger.info(f"WALLET {counter}")
            result = await Deployer.deploy(
                private_key=data.get("private_key"),
                network=data.get("network"),
                contract=data.get("contract"),
            )
            if result == RESULT_TRANSACTION.SUCCESS:
                await utils.time.sleep_view(settings.SLEEP)
            else:
                await utils.time.sleep_view((10, 15))
            counter += 1

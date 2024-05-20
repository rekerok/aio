import random
import eth_utils

from loguru import logger
from modules.account import Account
from modules.web3Client import Web3Client
from settings import Client_Networks
import utils
import config
from utils.enums import NETWORK_FIELDS, PARAMETR, RESULT_TRANSACTION


async def rubyscore(settings, wallets: list[str] = None):
    if wallets is None:
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
    db = list()

    for param in settings.PARAMS:
        db.extend(
            [
                {"wallet": wallet, "network": param.get(PARAMETR.NETWORK)}
                for wallet in wallets
                for _ in range(random.randint(*param.get(PARAMETR.COUNT_TRANSACTION)))
            ]
        )
    random.shuffle(db)
    counter = 1
    for data in db:
        logger.warning(f"OPERATION {counter}/{len(db)}")

        try:
            acc = Account(private_key=data["wallet"], network=data["network"])
            logger.info("RUBYSCORE")
            logger.info(f"WALLET {acc.address}")
            logger.info(f"NETWORK {acc.network.get(NETWORK_FIELDS.NAME)}")
            contract = acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(
                    config.RUBYSCORE.CONTRACTS.get(
                        data["network"].get(NETWORK_FIELDS.NAME)
                    )
                ),
                abi=config.RUBYSCORE.ABI,
            )
            data_transaction = await Web3Client.get_data(
                contract=contract, function_of_contract="vote"
            )
            result = await acc.send_transaction(
                to_address=contract.address, data=data_transaction
            )
        except Exception as error:
            logger.error(error)
            result = RESULT_TRANSACTION.FAIL
        if result == RESULT_TRANSACTION.SUCCESS:
            await utils.time.sleep_view(settings.SLEEP)
        else:
            await utils.time.sleep_view((10, 15))
        counter += 1

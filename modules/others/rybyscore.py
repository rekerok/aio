import random
import eth_utils

from loguru import logger
from modules.account import Account
from modules.web3Client import Web3Client
from settings import Client_Networks
import utils
import config
from utils.enums import RESULT_TRANSACTION


async def rubyscore(settings):
    wallets = await utils.files.read_file_lines(
        path=(
            "files/wallets.txt"
            if settings.WALLETS_FILE == ""
            else settings.WALLETS_FILE
        )
    )

    wallets = [item for item in wallets for _ in range(random.randint(*settings.COUNT))]

    # print(wallets)
    random.shuffle(wallets)
    counter = 1
    for wallet in wallets:
        logger.warning(f"OPERATION {counter}/{len(wallets)}")

        try:
            acc = Account(private_key=wallet, network=Client_Networks.scroll)
            contract = acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(
                    config.RUBYSCORE.CONTRACT
                ),
                abi=config.RUBYSCORE.ABI,
            )
            data = await Web3Client.get_data(
                contract=contract, function_of_contract="vote"
            )
            result = await acc.send_transaction(to_address=contract.address, data=data)
        except Exception as error:
            logger.error(error)
            result = RESULT_TRANSACTION.FAIL
        if result == RESULT_TRANSACTION.SUCCESS:
            await utils.time.sleep_view(settings.SLEEP)
        else:
            await utils.time.sleep_view((10, 15))
        counter += 1

import random

from loguru import logger
from modules.account import Account
import utils
from utils.enums import PARAMETR, RESULT_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


async def create_database(wallets, params):
    database = []
    for param in params:
        for wallet in wallets:
            for i in range(random.randint(*param.get(PARAMETR.COUNT_TRANSACTION))):
                token = random.choice(param.get(PARAMETR.TOKENS))
                database.append(
                    {
                        "wallet": wallet,
                        "network": param.get(PARAMETR.NETWORK),
                        "contract": random.choice(param.get(PARAMETR.CONTRACTS)),
                        "token": token.get(PARAMETR.TOKEN),
                        "value": token.get(PARAMETR.VALUE),
                    }
                )
    return database


async def warmup_approver_mode(settings):
    wallets = await utils.files.read_file_lines(
        path="files/wallets.txt",
    )
    database = await create_database(wallets=wallets, params=settings.PARAMS)
    random.shuffle(database)
    counter = 1
    for data in database:
        logger.warning(f"{counter}/{len(data)}")
        acc = Account(private_key=data["wallet"], network=data["network"])
        token_info = await Token_Info.get_info_token(
            acc=acc, token_address=data["token"].address
        )
        amount = Token_Amount(
            amount=random.uniform(data["value"][0], data["value"][1]),
            decimals=token_info.decimals,
        )
        logger.info(f"wallet: {acc.address}")
        logger.info(f"approve: {amount.ETHER} {token_info.symbol}")
        result = await acc.approve(
            token_address=token_info.address,
            spender=data["contract"],
            amount=amount,
            check_approve=False,
        )
        if result == RESULT_TRANSACTION.SUCCESS:
            await utils.time.sleep_view(settings.SLEEP)
        else:
            await utils.time.sleep_view((10, 15))
        counter += 1

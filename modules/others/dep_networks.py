import random
import eth_account
from loguru import logger
from modules.others.exchange import OKX
import utils
from utils.enums import (
    NETWORK_FIELDS,
    PARAMETR,
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)


async def dep_to_network(settings):
    wallets = list()
    wallets2 = await utils.files.read_file_lines(path="files/wallets.txt")
    for i in wallets2:
        wallets.append((i, eth_account.Account.from_key(i).address))
    random.shuffle(wallets)

    okx = OKX(
        apiKey=settings.OKX.get(PARAMETR.API_KEY),
        secret=settings.OKX.get(PARAMETR.API_SECRET),
        password=settings.OKX.get(PARAMETR.PASSWORD),
        attempt=settings.OKX.get(PARAMETR.ATTEMPT),
        check_send=True,
    )
    counter = 1
    for wallet in wallets:
        logger.warning(f"OPERATION {counter}/{len(wallets)}")
        to_withdraw = random.choice(settings.PARAMS.get(PARAMETR.TOKENS))
        value = random.uniform(*settings.PARAMS.get(PARAMETR.VALUE))
        await okx.withdraw(
            wallet[1],
            currency=to_withdraw.get(PARAMETR.TOKEN).exchange_name,
            chain=to_withdraw.get(PARAMETR.TOKEN).network,
            amount=value,
        )
        logger.debug("SLEEP AFTER WITHDRAW")
        await utils.time.sleep_view(settings.SLEEPS[PARAMETR.AFTER_WITHDRAW])
        if not settings.CHANGE_NETWORK:
            dep_to = random.choice(settings.PARAMS[PARAMETR.TO_TOKEN])
            if (
                to_withdraw[PARAMETR.NETWORK][NETWORK_FIELDS.NAME]
                == dep_to[PARAMETR.NETWORK]
            ):
                logger.debug("SLEEP BETWEEN WALLETS")
                await utils.time.sleep_view(settings.SLEEPS[PARAMETR.BETWEEN_WALLETS])
                continue
        else:
            remaining_elements = [
                element
                for element in settings.PARAMS[PARAMETR.TO_TOKEN]
                if element[PARAMETR.NETWORK]
                != to_withdraw[PARAMETR.NETWORK][NETWORK_FIELDS.NAME]
            ]
            dep_to = random.choice(remaining_elements)
        dex_class = random.choice(to_withdraw[PARAMETR.DEXES])
        dex = dex_class(
            private_key=wallet[0],
            network=to_withdraw[PARAMETR.NETWORK],
            type_transfer=TYPES_OF_TRANSACTION.AMOUNT,
            value=(value * 0.85, value * 0.95),
            min_balance=0,
        )

        result = await dex.bridge(
            from_token=to_withdraw[PARAMETR.TOKEN],
            to_token=dep_to[PARAMETR.TOKEN],
            to_network=dep_to[PARAMETR.NETWORK],
        )
        if result == RESULT_TRANSACTION.SUCCESS:
            logger.debug("SLEEP BETWEEN_WALLETS")
            await utils.time.sleep_view(settings.SLEEPS[PARAMETR.BETWEEN_WALLETS])
        else:
            await utils.time.sleep_view((10, 15))
        counter += 1

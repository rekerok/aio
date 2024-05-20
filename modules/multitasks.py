import random
import eth_account
import eth_keys
import eth_utils
from loguru import logger
import utils

from utils.enums import PARAMETR


async def create_database(wallets, tasks):
    db = {}
    for wallet in wallets:
        tmp = {}
        for task in tasks:
            if wallet not in db:
                db[wallet] = list()
            db[wallet].append(
                {
                    "module": task.get(PARAMETR.MODULE),
                    "settings": task.get(PARAMETR.SETTINGS),
                }
            )
    return db


async def start_multitasks(settings):
    wallets = await utils.files.read_file_lines(
        path="files/wallets.txt",
    )
    counter = 1
    db = await create_database(wallets=wallets, tasks=settings.TASKS)
    while db:
        # Случайный выбор кошелька
        wallet = random.choice(list(db.keys()))
        if db[wallet]:
            # Получение первого задания из списка для выбранного кошелька
            task = db[wallet][0]
            # Выполнение задания
            module = db.get(wallet)[0].get("module")
            settings_module = db.get(wallet)[0].get("settings")
            await module(settings=settings_module, wallets=[wallet])
            # Удаление выполненного задания из списка заданий
            db[wallet] = db[wallet][1:]
            # Если список заданий пуст, удаляем его из словаря
            remaining_tasks = len(db[wallet])
            logger.debug(f"{eth_account.Account.from_key(wallet).address} REMAINING {remaining_tasks} tasks")
            if not db[wallet]:
                del db[wallet]
        logger.warning("SLEEP BETWEEN MODULES")
        await utils.time.sleep_view(settings.SLEEP_BETWEEN_MODULES)
        counter += 1

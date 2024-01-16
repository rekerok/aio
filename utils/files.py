import json
import random

from loguru import logger


def get_random_proxy():
    try:
        with open("files/proxy.txt", "r") as file:
            lines = [i.strip() for i in file.readlines()]
            return random.choice(lines)
    except Exception as error:
        logger.error(error)
        return []


async def load_json(path: str) -> dict:
    with open(path) as json_file:
        return json.load(json_file)


async def read_file_lines(path: str) -> list[str]:
    try:
        with open(path, "r") as file:
            lines = [i.strip() for i in file.readlines()]
            return lines
    except:
        return []


async def get_wallets_recipients(
    wallets_path: str, recipients_path: str
) -> list[tuple]:
    list_wallets = await read_file_lines(wallets_path)
    list_recipients = await read_file_lines(recipients_path)
    try:
        if len(list_wallets) != len(list_recipients):
            return list()
        return list(zip(list_wallets, list_recipients))
    except Exception as error:
        return list()


async def find_key(dictionary, value):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

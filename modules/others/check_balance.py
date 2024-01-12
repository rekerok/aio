import asyncio
import csv
import pprint
from modules.account import Account
import utils
from loguru import logger

from utils.enums import NETWORK_FIELDS, PARAMETR
from utils.token_info import Token_Info


async def collect_balance(wallet, params):
    balance = []
    for param in params:
        acc = Account(address=wallet, network=param.get(PARAMETR.NETWORK))
        balances = []
        for token in param.get(PARAMETR.TOKENS):
            while True:
                token_info = await Token_Info.get_info_token(
                    acc=acc, token_address=token
                )
                balance_of_wallet = await acc.get_balance(token_address=token)
                if balance_of_wallet is None or token_info is None:
                    logger.error(
                        f"ОШИБКА ПОДКЛЮЧЕНИЯ К РПЦ В СЕТИ {param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)}"
                    )
                    logger.warning("МЕНЯЮ РПЦ")
                    await acc.change_connection()
                else:
                    logger.success(
                        f"{wallet} {param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)} {balance_of_wallet.ETHER} {token_info.symbol}"
                    )
                    balances.append({token_info.symbol: balance_of_wallet.ETHER})
                    break
        balance.append({param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME): balances})
    return {wallet: balance}


async def check_balances(settings):
    wallets = await utils.files.read_file_lines("files/wallets.txt")
    results = []
    tasks = []
    for wallet in wallets:
        # results.append(await collect_balance(wallet=wallet, params=settings.params))
        tasks.append(
            asyncio.create_task(collect_balance(wallet=wallet, params=settings.params))
        )
    # pprint.pprint(results)
    done, pending = await asyncio.wait(tasks)
    with open("files/balances.csv", "w") as file:
        writer = csv.writer(file)
        first_task = 0
        for i in done:
            first_task = i.result()
            break
        header = ["№", "WALLET"]
        for address, networks in first_task.items():
            for network_info in networks:
                for network, coins_info in network_info.items():
                    for coin_info in coins_info:
                        for coin, _ in coin_info.items():
                            header.append(f"{network.name}-{coin}")
        writer.writerow(header)
        count = 1
        lines = []
        for i in done:
            line = [count, wallet]
            for wallet, balances in i.result().items():
                for balance in balances:
                    for token in balance[list(balance.keys())[0]]:
                        line.append(token[list(token.keys())[0]])
            lines.append(line)
            count += 1
        writer.writerows(lines)

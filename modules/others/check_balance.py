import asyncio
import csv
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
                    acc=acc, token_address=token.address
                )
                if token_info is None:
                    logger.error(f"NOT TOKEN INFO {token.address}")
                    await acc.change_connection()
                    continue
                balance_of_wallet = await acc.get_balance(
                    token_address=token_info.address
                )
                if not balance_of_wallet is None:
                    logger.success(
                        f"{wallet} {param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)} {balance_of_wallet.ether} {token_info.symbol}"
                    )
                    balances.append(
                        {
                            token_info.symbol: str(balance_of_wallet.ether).replace(
                                ".", ","
                            )
                        }
                    )
                    break
                logger.error(
                    f"NOT BALANCE INFO {acc.address} {acc.network[NETWORK_FIELDS.NAME]}"
                )
                await acc.change_connection()
        balance.append({param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME): balances})
    return {wallet: balance}


async def check_balances(settings):
    wallets = await utils.files.read_file_lines("files/addresses.txt")
    tasks = []
    counter = 1
    for wallet in wallets:
        logger.debug(f"OPERATION {counter}/{len(wallets)}")
        tasks.append(collect_balance(wallet=wallet, params=settings.params))
        counter += 1
    results = await asyncio.gather(*tasks)

    with open("files/balances.csv", "w") as file:
        writer = csv.writer(file)
        header = ["№", "WALLET"]
        for address, networks in results[0].items():
            for network_info in networks:
                for network, coins_info in network_info.items():
                    for coin_info in coins_info:
                        for coin, _ in coin_info.items():
                            header.append(f"{network.name}-{coin}")
        writer.writerow(header)
        count = 1
        for i in results:
            line = [count, list(i.keys())[0]]
            for wallet, balances in i.items():
                for balance in balances:
                    for token in balance[list(balance.keys())[0]]:
                        line.append(token[list(token.keys())[0]])
            count += 1
            writer.writerow(line)

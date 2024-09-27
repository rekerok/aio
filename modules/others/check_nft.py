import csv
import utils
from loguru import logger
from modules.account import Account
from utils.enums import NETWORK_FIELDS, PARAMETR


class Check_NFT:
    @staticmethod
    async def check_nft(settings):
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
        logger.info("START MODULE CHECK NFT")
        data = dict()
        counter = 1
        for wallet in wallets:
            logger.debug(f"{counter}) WALLET {wallet}")
            test = list()
            for param in settings.PARAMS:
                logger.warning(
                    f"NETWORK {param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)}"
                )
                acc = Account(address=wallet, network=param.get(PARAMETR.NETWORK))
                value = ""
                for nft in param.get(PARAMETR.NFTS):
                    while True:
                        try:
                            amount = await acc.get_balance(
                                token_address=nft.get(PARAMETR.TOKEN_ADDRESS)
                            )
                            if not amount:
                                continue
                            test.append(
                                {
                                    f"{param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)}-{nft.get(PARAMETR.NETWORK)}": amount.wei
                                }
                            )
                            logger.info(
                                f'NFT "{nft.get(PARAMETR.NAME)}" : {amount.wei}'
                            )
                            break
                        except Exception as e:
                            logger.warning(e)
                            acc = Account(
                                address=wallet, network=param.get(PARAMETR.NETWORK)
                            )
                print()
                data[wallet] = test
            counter += 1
            logger.info("-------------")
            with open("files/result_nft.csv", "w", newline="") as file:
                header = ["number", "wallet"]
                for param in settings.PARAMS:
                    network_name = param.get(PARAMETR.NETWORK).get(NETWORK_FIELDS.NAME)
                    for nft in param.get(PARAMETR.NFTS):
                        nft_name = nft.get(PARAMETR.NAME)
                        header.append(f"{network_name}-{nft_name}")
                writer = csv.writer(file)
                writer.writerow(header)
                count = 1
                for key, value in data.items():
                    line = [count, key]
                    for nft in value:
                        line.append(list(nft.values())[0])
                    writer.writerow(line)
                    count += 1
                summary_data = dict()
                for wallet, nft_list in data.items():
                    summary_data[wallet] = {}
                    for nft_data in nft_list:
                        for key, value in nft_data.items():
                            network, _ = key.split("-", 1)
                            summary_data[wallet][network] = (
                                summary_data[wallet].get(network, 0) + value
                            )

                writer.writerow([])
                writer.writerow([])
                writer.writerow([])
                writer.writerow([])
                writer.writerow([])
                writer.writerow([])

                header = ["wallet"]
                networks = set()
                for nft_list in data.values():
                    for nft_data in nft_list:
                        for key, _ in nft_data.items():
                            networks.add(key.split("-")[0])
                header.extend(networks)
                writer.writerow(header)
                for key, value in summary_data.items():
                    line = [key]
                    for network, count in value.items():
                        line.append(count)
                    writer.writerow(line)

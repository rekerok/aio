import csv
from mnemonic import Mnemonic
import eth_account

eth_account.Account().enable_unaudited_hdwallet_features()


class Create_Wallets:
    @staticmethod
    async def create_wallets(count, filename):
        mnemo = Mnemonic("english")
        wallet_data = []
        with open("files/" + filename, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["number", "address", "private", "mnemo"])
            for i in range(count):
                words = mnemo.generate(strength=128)
                acc = eth_account.Account().from_mnemonic(words)
                private = acc._private_key.hex()
                public = acc.address
                wallet_data.append((i + 1, public, private, words))
            writer.writerows(wallet_data)

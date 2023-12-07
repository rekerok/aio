import modules
from helpers.enums import TYPE_OF_TRANSACTION
from networks import Networks
from helpers.web3Swapper import Web3Swapper


class OKX_settings:
    # PROXY: str = "http://user:pass@ip:port"
    PROXY: str = ""
    SLEEP: tuple[int] = (60, 200)
    KEYS: dict = {
        "api_key": "",
        "api_secret": "",
        "password": "",
    }

    params: list = [
        {
            "network": "Linea",
            "symbol": "ETH",
            "amount": (0.01494673, 0.02241770),
            "round": (3, 5),
            "wallets_file": "",
        },
        # {
        #     "network": "Aptos",
        #     "symbol": "APT",
        #     "amount": {"min": 0.5, "max": 1},
        #     "round": {"min": 1, "max": 3},
        #     "wallets_file": "files/aptos_withdraw.txt",
        # },
    ]


class SWAP_SETTINGS:
    params = [
        {
            "network": Networks.linea,
            "type_swap": TYPE_OF_TRANSACTION.PERCENT,
            "value": (80, 90),
            "count_swaps": (2, 2),
            "tokens": [
                {"address": "", "min_balance": 0},  # ETH
                {
                    "address": "0xb5bedd42000b71fdde22d3ee8a79bd49a568fc8f",
                    "min_balance": 0,
                },  # wstETH
            ],
        },
    ]
    SLIPPAGE = 5
    SLEEP = (10, 50)


### NOT CHANGE ###
async def okx_withdrawer():
    await modules.OKX.withdraw_use_database(OKX_settings)


async def woofi_swap():
    await Web3Swapper.swap_use_database(
        settings=SWAP_SETTINGS, dex_class=modules.WoofiSwap
    )

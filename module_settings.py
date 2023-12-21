from modules import *
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


class TRANSFERS_SETTINGS:
    params = [
        {
            "network": Networks.linea,
            "token": "",
            "type_transfer": TYPE_OF_TRANSACTION.PERCENT,
            "value": (90, 95),
            "min_balance": 0.00075,
        },
    ]
    SLEEP = (100, 300)


# SushiSwap
# WoofiSwap
# InchSwap
# OdosSwap
# SyncSwap
class SWAP_SETTINGS:
    params = [
        {
            "network": Networks.polygon,
            "dexs": [OdosSwap, SushiSwap, InchSwap],
            "type_swap": TYPE_OF_TRANSACTION.PERCENT,
            "value": (90, 100),
            "from_token": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
            "min_balance": 0,
            "to_token": "",
            "wallets_file": "files/poly.txt",
        },
        {
            "network": Networks.avalanche,
            "dexs": [SushiSwap, OdosSwap],
            "type_swap": TYPE_OF_TRANSACTION.PERCENT,
            "value": (100, 100),
            "from_token": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            "min_balance": 0,
            "to_token": "",
            "wallets_file": "files/avax.txt",
        },
    ]
    SLIPPAGE = 5
    SLEEP = (10, 50)


class CHECK_NFT_SETTINGS:
    params = [
        {
            "network": Networks.polygon,
            "nfts": [
                {
                    "address": "0x6D6768A0b24299bEdE0492A4571D79F535c330D8",
                    "name": "How Far We've Come",
                },
                {
                    "address": "0xB6432d111bc2A022048b9aEA7C11b2d627184bdD",
                    "name": "azure",
                },
                {
                    "address": "0xe5325804D68033eDF65a86403B2592a99E1f06de",
                    "name": "fs",
                },
                {
                    "address": "0x8C531f965C05Fab8135d951e2aD0ad75CF3405A2",
                    "name": "Building",
                },
                {
                    "address": "0x61B2d56645d697Ac3a27c2fa1e5B26B45429d1A9",
                    "name": "Kauai Walmart",
                },
                {
                    "address": "0xd4Feff615c0E90f06340Be95d30e1f397779A184",
                    "name": "Cosmic flower",
                },
            ],
        },
        {
            "network": Networks.avalanche,
            "nfts": [
                {
                    "address": "0x6D6768A0b24299bEdE0492A4571D79F535c330D8",
                    "name": "How Far We've Come",
                },
                {
                    "address": "0xB6432d111bc2A022048b9aEA7C11b2d627184bdD",
                    "name": "azure",
                },
                {
                    "address": "0xe5325804D68033eDF65a86403B2592a99E1f06de",
                    "name": "fs",
                },
                {
                    "address": "0x8C531f965C05Fab8135d951e2aD0ad75CF3405A2",
                    "name": "Building",
                },
                {
                    "address": "0x61B2d56645d697Ac3a27c2fa1e5B26B45429d1A9",
                    "name": "Kauai Walmart",
                },
                {
                    "address": "0xd4Feff615c0E90f06340Be95d30e1f397779A184",
                    "name": "Cosmic flower",
                },
            ],
        },
    ]


class WARMUPSWAPS_SETTINGS:
    params = {
        InchSwap: [
            {
                "network": Networks.polygon,
                "tokens": [
                    {
                        "address": "",
                        "min_balance": 0,
                    },
                    {
                        "address": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",
                        "min_balance": 0,
                    },
                ],
                "count_swaps": (1, 2),
                "percent_swap": (10, 20),
            },
        ],
    }
    SLEEP = (1000, 2000)


### NOT CHANGE ###
async def okx_withdrawer():
    await OKX.withdraw_use_database(OKX_settings)


async def transfers():
    await Transfers.transfer_use_database(TRANSFERS_SETTINGS)


async def check_nft():
    await Check_NFT.check_nft(settings=CHECK_NFT_SETTINGS)


async def swaps():
    await Web3Swapper.swap_use_database(settings=SWAP_SETTINGS)


async def warm_up_swaps():
    await WarmUPSwaps.warmup(settings=WARMUPSWAPS_SETTINGS)

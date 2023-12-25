from modules import *
from utils import TYPE_OF_TRANSACTION
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
# IzumiSwap
class SWAP_SETTINGS:
    params = [
        {
            "network": Networks.zksync,
            "type_swap": TYPE_OF_TRANSACTION.PERCENT,
            "value": (90, 100),
            "from_token": "",
            "min_balance": 0,
            "to_tokens": [
                {
                    "address": "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C",
                    "dexs": [
                        WoofiSwap,
                        InchSwap,
                        OdosSwap,
                        SyncSwap,
                    ],  # usdt
                    "address": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
                    "dexs": [
                        WoofiSwap,
                        InchSwap,
                        OdosSwap,
                        SyncSwap,
                    ],  # usdc
                }
            ],
            "wallets_file": "",
        },
    ]
    SLIPPAGE = 1
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
    SLIPPAGE = 1
    SLEEP = (1000, 2000)


class MERKLY_SETTINGS:
    CHECK_COMISSION_NETWORKS = [Networks.polygon, Networks.base]
    params = [
        {
            "network": Networks.polygon,
            "to_chains": [
                {
                    "name": "beam",
                    "amount": (3.23, 3.23),
                }
            ],
            "count_transaction": (2, 2),
            "wallets_file": "",
        }
    ]
    SLEEP = (100, 150)


class DEPLOY_SETTINGS:
    params = [
        {
            "network": Networks.polygon,
            "contracts": [
                {
                    "name": "merkly",
                    "bytecode": "0x60806040526000805461ffff1916905534801561001b57600080fd5b5060fb8061002a6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c80630c55699c146037578063b49004e914605b575b600080fd5b60005460449061ffff1681565b60405161ffff909116815260200160405180910390f35b60616063565b005b60008054600191908190607a90849061ffff166096565b92506101000a81548161ffff021916908361ffff160217905550565b61ffff81811683821601908082111560be57634e487b7160e01b600052601160045260246000fd5b509291505056fea2646970667358221220666c87ec501268817295a4ca1fc6e3859faf241f38dd688f145135970920009264736f6c63430008120033",
                }
            ],
            "count": (1, 1),
        }
    ]
    SLEEP = (100, 200)


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


async def merkly():
    await Merkly.swap_use_database(settings=MERKLY_SETTINGS)


async def merkly_check_comission():
    await Merkly.get_fees(from_chains=MERKLY_SETTINGS.CHECK_COMISSION_NETWORKS)


async def deploy_contracts():
    await Deployer.deploy_with_database(settings=DEPLOY_SETTINGS)

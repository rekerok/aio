from modules import *
from config import Network, TOKENS
from settings import Client_Networks
from utils import TYPES_OF_TRANSACTION, PARAMETR


class DEX:
    ONE_INCH = InchSwap
    IZUMI = IzumiSwap
    ODOS = OdosSwap
    OPENOCEAN = OpenoceanSwap
    SUSHI = SushiSwap
    SYNCSWAP = SyncSwap
    WOOFI = WoofiSwap
    ZKSWAP = ZkSwap
    BASESWAP = BaseSwap
    ZEROX = Zerox
    XY_FINANCE_SWAP = XY_finance_swap
    RANGO_SWAP = RangoSwap
    ACROSS = Across
    STARGATE = Stargate
    ORBITER = Orbiter
    NITRO = Nitro
    XY_FINANCE_BRIDGE = XY_finance_bridge
    RANGO_BRIDGE = Rango_Bridge


class LENDINGS:
    ERALEND = Eralend


class REFUEL_APP:
    MERKLY = Merkly
    L2PASS = L2Pass


class OKX_settings:
    # PROXY: str = "http://user:pass@ip:port"
    PROXY: str = ""
    KEYS: dict = {
        PARAMETR.OKX_API_KEY: "",
        PARAMETR.OKX_API_SECRET: "",
        PARAMETR.OKX_PASSWORD: "",
    }
    PARAMS: list[dict] = [
        {
            PARAMETR.TOKEN: TOKENS.AVALANCHE.AVAX,
            PARAMETR.VALUE: (0.1, 0.1),
            PARAMETR.ROUND: (1, 1),
            PARAMETR.WALLETS_FILE: "",
        },
    ]
    SLEEP: tuple[int] = (60, 200)
    WAIT_TO_SEND = True
    ATTEMPT_WAIT_WITHDRAW = 15


class TRANSFERS_SETTINGS:
    PARAMS: list[dict] = [
        {
            PARAMETR.NETWORK: Client_Networks.avalanche,
            PARAMETR.TOKEN: TOKENS.AVALANCHE.AVAX,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (20, 50),
            PARAMETR.MIN_BALANCE: 0.0001,
        },
    ]
    SLEEP: tuple[int] = (1000, 4000)


class SWAP_SETTINGS:
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (100, 100),
            PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.USDC,
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.MAX_BALANCE: 1000,
            PARAMETR.TO_TOKENS: [
                {
                    PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.ETH,
                    PARAMETR.DEXS: [DEX.OPENOCEAN, DEX.ODOS],
                },
            ],
            PARAMETR.WALLETS_FILE: "",
        },
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (100, 100),
            PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.USDT,
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.MAX_BALANCE: 1000,
            PARAMETR.TO_TOKENS: [
                {
                    PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.ETH,
                    PARAMETR.DEXS: [DEX.OPENOCEAN, DEX.ODOS],
                },
            ],
            PARAMETR.WALLETS_FILE: "",
        },
    ]
    SLIPPAGE = 1
    SLEEP = (100, 100)


class BRIDGE_SETTINGS:
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.optimism,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (10, 15),
            PARAMETR.FROM_TOKEN: TOKENS.OPTIMISM.ETH,
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.TO_TOKENS: [
                {
                    PARAMETR.NETWORK: Network.SCROLL,
                    PARAMETR.TO_TOKEN: TOKENS.SCROLL.ETH,
                    PARAMETR.DEXS: [DEX.XY_FINANCE_BRIDGE],
                },
            ],
            PARAMETR.WALLETS_FILE: "",
        },
    ]
    SLIPPAGE = 5
    SLEEP = (10, 50)


class LANDINGS_SETTINGS:
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (1, 2),
            PARAMETR.LENDING_DEPOSIT: False,
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.TOKENS: [
                {
                    PARAMETR.TOKEN: TOKENS.ZKSYNC.ETH,
                    PARAMETR.LENDINGS: [LENDINGS.ERALEND],
                },
            ],
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.WALLETS_FILE: "",
        },
    ]
    SLIPPAGE = 1
    SLEEP = (10, 50)


class CHECK_NFT_SETTINGS:
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.polygon,
            PARAMETR.NFTS: [
                {
                    PARAMETR.TOKEN_ADDRESS: "0x6D6768A0b24299bEdE0492A4571D79F535c330D8",
                    PARAMETR.NAME: "How Far We've Come",
                },
                {
                    PARAMETR.TOKEN_ADDRESS: "0xB6432d111bc2A022048b9aEA7C11b2d627184bdD",
                    PARAMETR.NAME: "azure",
                },
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.avalanche,
            PARAMETR.NFTS: [
                {
                    PARAMETR.TOKEN_ADDRESS: "0xB6432d111bc2A022048b9aEA7C11b2d627184bdD",
                    PARAMETR.NAME: "azure",
                },
            ],
        },
    ]


class WARMUPSWAPS_SETTINGS:
    PARAMS = {
        DEX.ODOS: [
            {
                PARAMETR.NETWORK: Client_Networks.polygon,
                PARAMETR.TOKENS: [
                    {
                        PARAMETR.TOKEN: TOKENS.POLYGON.USDT,
                        PARAMETR.MIN_BALANCE: 1,
                        PARAMETR.MAX_BALANCE: 1000,
                    },
                    {
                        PARAMETR.TOKEN: TOKENS.POLYGON.USDC_BRIDGED,
                        PARAMETR.MIN_BALANCE: 1,
                        PARAMETR.MAX_BALANCE: 1000,
                    },
                ],
                PARAMETR.COUNT_TRANSACTION: (2, 3),
                PARAMETR.VALUE: (20, 30),
            },
        ],
    }
    USE_MAX_BALANCE = False
    SLIPPAGE = 5
    SLEEP = (20, 30)


class WARMPUSTARGATE_SETTINGS:
    USE_OKX = True
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.polygon,
            PARAMETR.TOKENS: [TOKENS.POLYGON.USDT],
            PARAMETR.TO_TOKENS: [
                {
                    PARAMETR.NETWORK: Network.AVALANCHE,
                    PARAMETR.TO_TOKEN: TOKENS.AVALANCHE.USDT,
                },
                {
                    PARAMETR.NETWORK: Network.OPTIMISM,
                    PARAMETR.TO_TOKEN: TOKENS.OPTIMISM.USDC,
                },
            ],
        }
    ]
    VALUE = (1, 4)
    MAX_FEES = {}


class REFUEL_SETTINGS:
    CHECK_COMISSION_NETWORKS = {
        REFUEL_APP.MERKLY: [
            Client_Networks.zksync,
        ],
        REFUEL_APP.L2PASS: [Client_Networks.zksync],
    }
    PARAMS = {
        REFUEL_APP.MERKLY: [
            {
                PARAMETR.NETWORK: Client_Networks.polygon,
                PARAMETR.TO_CHAINS: [
                    {
                        PARAMETR.NAME: Network.FUSE,
                        PARAMETR.VALUE: (0.0001, 0.001),
                    },
                ],
                PARAMETR.COUNT_TRANSACTION: (1, 1),
                PARAMETR.WALLETS_FILE: "",
            }
        ],
        REFUEL_APP.L2PASS: [
            {
                PARAMETR.NETWORK: Client_Networks.polygon,
                PARAMETR.TO_CHAINS: [
                    {
                        PARAMETR.NAME: Network.BEAM,
                        PARAMETR.VALUE: (0.0001, 0.001),
                    },
                ],
                PARAMETR.COUNT_TRANSACTION: (1, 1),
                PARAMETR.WALLETS_FILE: "",
            }
        ],
    }
    SLEEP = (50, 100)


class DEPLOY_SETTINGS:
    params = [
        {
            PARAMETR.NETWORK: Client_Networks.polygon,
            PARAMETR.CONTRACTS: [
                {
                    PARAMETR.NAME: "clear",
                    PARAMETR.BYTECODE_CONTRACT: "0x",
                },
            ],
            PARAMETR.COUNT_TRANSACTION: (1, 1),
        },
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.CONTRACTS: [
                {
                    PARAMETR.NAME: "clear",
                    PARAMETR.BYTECODE_CONTRACT: "0x",
                },
            ],
            PARAMETR.COUNT_TRANSACTION: (1, 1),
        },
    ]
    SLEEP = (5, 10)


class CHECK_BALANCES_SETTINGS:
    params = [
        {
            PARAMETR.NETWORK: Client_Networks.arbitrum,
            PARAMETR.TOKENS: [
                TOKENS.ARBITRUM.ETH,
                TOKENS.ARBITRUM.USDC,
                TOKENS.ARBITRUM.USDC_BRIDGED,
                TOKENS.ARBITRUM.USDT,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.optimism,
            PARAMETR.TOKENS: [
                TOKENS.OPTIMISM.ETH,
                TOKENS.OPTIMISM.USDC,
                TOKENS.OPTIMISM.USDC_BRIDGED,
                TOKENS.OPTIMISM.USDT,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.TOKENS: [
                TOKENS.ZKSYNC.ETH,
                TOKENS.ZKSYNC.USDC,
                TOKENS.ZKSYNC.USDT,
                TOKENS.ZKSYNC.DAI,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.base,
            PARAMETR.TOKENS: [TOKENS.BASE.ETH, TOKENS.BASE.USDbC],
        },
        {
            PARAMETR.NETWORK: Client_Networks.nova,
            PARAMETR.TOKENS: [TOKENS.NOVA.ETH],
        },
        {
            PARAMETR.NETWORK: Client_Networks.scroll,
            PARAMETR.TOKENS: [TOKENS.SCROLL.ETH],
        },
        {
            PARAMETR.NETWORK: Client_Networks.avalanche,
            PARAMETR.TOKENS: [
                TOKENS.AVALANCHE.AVAX,
                TOKENS.AVALANCHE.USDC,
                TOKENS.AVALANCHE.USDT,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.polygon,
            PARAMETR.TOKENS: [
                TOKENS.POLYGON.MATIC,
                TOKENS.POLYGON.USDC,
                TOKENS.POLYGON.USDT,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.bsc,
            PARAMETR.TOKENS: [TOKENS.BSC.BNB, TOKENS.BSC.USDT],
        },
    ]


class CREATE_WALLETS_SETTIGS:
    COUNT = 10
    FILE = "wallest.csv"


### NOT CHANGE ###
async def okx_withdrawer():
    await OKX.withdraw_use_database(settings=OKX_settings)


async def transfers():
    await Transfers.transfer_use_database(settings=TRANSFERS_SETTINGS)


async def check_nft():
    await Check_NFT.check_nft(settings=CHECK_NFT_SETTINGS)


async def swaps():
    await Web3Swapper.swap_use_database(settings=SWAP_SETTINGS)


async def bridges():
    await Web3Bridger.swap_use_database(settings=BRIDGE_SETTINGS)


async def landings():
    await Web3Lending.landing_use_database(settings=LANDINGS_SETTINGS)
    # pass


async def warm_up_swaps():
    await WarmUPSwaps.warmup(settings=WARMUPSWAPS_SETTINGS)


async def warm_up_refuel():
    await WarmUpRefuel.warm_up_refuel(settings=REFUEL_SETTINGS)


async def get_fees_refuel():
    await WarmUpRefuel.get_fees(apps=REFUEL_SETTINGS.CHECK_COMISSION_NETWORKS)


async def deploy_contracts():
    await Deployer.deploy_with_database(settings=DEPLOY_SETTINGS)


async def create_wallets():
    await Create_Wallets().create_wallets(
        count=CREATE_WALLETS_SETTIGS.COUNT, filename=CREATE_WALLETS_SETTIGS.FILE
    )


async def check_balance():
    await check_balances(settings=CHECK_BALANCES_SETTINGS)

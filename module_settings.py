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
    SKYDROME = Skydrome
    ACROSS = Across
    STARGATE = Stargate
    ORBITER = Orbiter
    NITRO = Nitro
    XY_FINANCE_BRIDGE = XY_finance_bridge
    RANGO_BRIDGE = Rango_Bridge


class LENDINGS:
    ERALEND = Eralend
    LAYERBANK = Layerbank
    AAVE = Aave
    BASILISK = Basilisk
    ZEROLEND = ZeroLend
    REACTOR_FUSION = Reactor_Fusion


class NFTS:
    L2PASS = L2pass_NFT


class REFUEL_APP:
    MERKLY = Merkly
    L2PASS = L2Pass


class MODULES:
    OKX_WITHDRAW = OKX.withdraw_use_database
    TRANSFER = Transfers.transfer_use_database
    SWAPS = Web3Swapper.swap_use_database
    BRIDGES = Web3Bridger.swap_use_database
    LENDINGS = Web3Lending.landing_use_database
    MINT_NFT = Web3Nft.mint_use_database
    WARMUP_SWAPS = WarmUPSwaps.warmup
    WARMUP_REFUEL = WarmUpRefuel.warm_up_refuel
    DEPLOY_CONTRACTS = Deployer.deploy_with_database


class OKX_settings:
    SLEEP: tuple[int] = (60, 200)
    WAIT_TO_SEND = False
    ATTEMPT_WAIT_WITHDRAW = 15
    PROXY: str = ""  # "http://user:pass@ip:port"

    KEYS: dict = {
        PARAMETR.OKX_API_KEY: "",
        PARAMETR.OKX_API_SECRET: "",
        PARAMETR.OKX_PASSWORD: "",
    }

    PARAMS: list[dict] = [
        {
            PARAMETR.TOKENS: [TOKENS.ARBITRUM.ETH, TOKENS.OPTIMISM.ETH],
            PARAMETR.VALUE: (0.1, 0.1),
            PARAMETR.ROUND: (0, 3),
            PARAMETR.RECIPIENTS_FILE: "",
        },
    ]

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: tuple[int] = None,
        WAIT_TO_SEND: bool = None,
        ATTEMPT_WAIT_WITHDRAW: int = None,
        KEYS: dict = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if WAIT_TO_SEND is not None:
            self.WAIT_TO_SEND = WAIT_TO_SEND
        if ATTEMPT_WAIT_WITHDRAW is not None:
            self.ATTEMPT_WAIT_WITHDRAW = ATTEMPT_WAIT_WITHDRAW
        if KEYS is not None:
            self.KEYS = KEYS
        if PARAMS is not None:
            self.PARAMS = PARAMS


class TRANSFERS_SETTINGS:
    SLEEP: tuple[int] = (1000, 4000)
    WALLETS_FILE: str = ""  # DEFAULT files/wallets.txt
    RECIPIENTS_FILE: str = ""  # DEFAULT files/recipients.txt

    PARAMS: list[dict] = [
        {
            PARAMETR.NETWORK: Client_Networks.avalanche,
            PARAMETR.TOKEN: TOKENS.AVALANCHE.AVAX,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (20, 50),
            PARAMETR.MIN_BALANCE: 0.0001,
        },
    ]

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: int = None,
        WALLETS_FILE: str = None,
        RECIPIENTS_FILE: str = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if WALLETS_FILE is not None:
            self.WALLETS_FILE = WALLETS_FILE
        if RECIPIENTS_FILE is not None:
            self.RECIPIENTS_FILE = RECIPIENTS_FILE
        if PARAMS is not None:
            self.PARAMS = PARAMS


class SWAP_SETTINGS:
    SLEEP = (50, 50)
    SLIPPAGE = 1

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
                    PARAMETR.DEXS: [DEX.IZUMI],
                },
            ],
            PARAMETR.WALLETS_FILE: "",
        },
    ]

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: int = None,
        SLIPPAGE: int = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if SLIPPAGE is not None:
            self.SLIPPAGE = SLIPPAGE
        if PARAMS is not None:
            self.PARAMS = PARAMS


class BRIDGE_SETTINGS:
    SLEEP = (100, 200)
    SLIPPAGE = 5

    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.avalanche,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.AMOUNT,
            PARAMETR.VALUE: (1.5, 1.5),
            PARAMETR.FROM_TOKEN: TOKENS.AVALANCHE.USDC,
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.TO_TOKENS: [
                {
                    PARAMETR.NETWORK: Network.ZKSYNC,
                    PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.USDC,
                    PARAMETR.DEXS: [DEX.NITRO],
                },
            ],
            PARAMETR.WALLETS_FILE: "",
        },
    ]

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: int = None,
        SLIPPAGE: int = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if SLIPPAGE is not None:
            self.SLIPPAGE = SLIPPAGE
        if PARAMS is not None:
            self.PARAMS = PARAMS


class LANDINGS_SETTINGS:
    SLEEP = (100, 100)

    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (10, 10),
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

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: int = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if PARAMS is not None:
            self.PARAMS = PARAMS


class MINT_NFT_SETTINGS:
    SLEEP = (100, 200)

    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.scroll,
            PARAMETR.NFTS: [
                {
                    PARAMETR.DEX: NFTS.L2PASS,
                    PARAMETR.CONTRACTS: ["0x0000049F63Ef0D60aBE49fdD8BEbfa5a68822222"],
                },
            ],
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.WALLETS_FILE: "",
        },
    ]

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: int = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if PARAMS is not None:
            self.PARAMS = PARAMS


class WARMUPSWAPS_SETTINGS:
    SLEEP = (20, 30)
    SLIPPAGE = 3
    USE_MAX_BALANCE = False
    WALLETS_FILE = ""  # DEFAULT files/wallets.txt
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

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: tuple[int] = None,
        SLIPPAGE: int = None,
        USE_MAX_BALANCE: bool = None,
        WALLETS_FILE: str = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if SLIPPAGE is not None:
            self.SLIPPAGE = SLIPPAGE
        if USE_MAX_BALANCE is not None:
            self.USE_MAX_BALANCE = USE_MAX_BALANCE
        if WALLETS_FILE is not None:
            self.WALLETS_FILE = WALLETS_FILE
        if PARAMS is not None:
            self.PARAMS = PARAMS


class REFUEL_SETTINGS:
    SLEEP = (150, 200)
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

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: tuple[int] = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if PARAMS is not None:
            self.PARAMS = PARAMS


class DEPLOY_SETTINGS:
    SLEEP = (5, 10)
    PARAMS = [
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
    ]

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: tuple[int] = None,
        PARAMS: list[dict] = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if PARAMS is not None:
            self.PARAMS = PARAMS


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


class CHECK_BALANCES_SETTINGS:
    params = [
        {
            PARAMETR.NETWORK: Client_Networks.arbitrum,
            PARAMETR.TOKENS: [
                # TOKENS.ARBITRUM.ETH,
                TOKENS.ARBITRUM.USDC,
                # TOKENS.ARBITRUM.USDC_BRIDGED,
                # TOKENS.ARBITRUM.USDT,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.optimism,
            PARAMETR.TOKENS: [
                # TOKENS.OPTIMISM.ETH,
                TOKENS.OPTIMISM.USDC,
                TOKENS.OPTIMISM.USDC_BRIDGED,
                # TOKENS.OPTIMISM.USDT,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.TOKENS: [
                # TOKENS.ZKSYNC.ETH,
                TOKENS.ZKSYNC.USDC,
                # TOKENS.ZKSYNC.USDT,
                # TOKENS.ZKSYNC.DAI,
            ],
        },
        # {
        #     PARAMETR.NETWORK: Client_Networks.base,
        #     PARAMETR.TOKENS: [TOKENS.BASE.ETH, TOKENS.BASE.USDbC],
        # },
        # {
        #     PARAMETR.NETWORK: Client_Networks.nova,
        #     PARAMETR.TOKENS: [TOKENS.NOVA.ETH],
        # },
        # {
        #     PARAMETR.NETWORK: Client_Networks.scroll,
        #     PARAMETR.TOKENS: [
        #         TOKENS.SCROLL.ETH,
        #         TOKENS.SCROLL.USDC,
        #         TOKENS.SCROLL.USDT,
        #     ],
        # },
        {
            PARAMETR.NETWORK: Client_Networks.avalanche,
            PARAMETR.TOKENS: [
                # TOKENS.AVALANCHE.AVAX,
                TOKENS.AVALANCHE.USDC,
                # TOKENS.AVALANCHE.USDT,
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.polygon,
            PARAMETR.TOKENS: [
                # TOKENS.POLYGON.MATIC,
                TOKENS.POLYGON.USDC_BRIDGED,
                TOKENS.POLYGON.USDC,
                # TOKENS.POLYGON.USDT,
            ],
        },
        # {
        #     PARAMETR.NETWORK: Client_Networks.bsc,
        #     PARAMETR.TOKENS: [TOKENS.BSC.BNB, TOKENS.BSC.USDT],
        # },
    ]


class CREATE_WALLETS_SETTIGS:
    COUNT = 10
    FILE = "wallest.csv"


class MULTITASKS_SETTINGS:
    SLEEP_BETWEEN_MODULES = (30, 60)
    TASKS = [
        {
            PARAMETR.MODULE: MODULES.LENDINGS,
            PARAMETR.SETTINGS: LANDINGS_SETTINGS(
                PARAMS=[
                    {
                        PARAMETR.NETWORK: Client_Networks.zksync,
                        PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
                        PARAMETR.VALUE: (10, 10),
                        PARAMETR.LENDING_DEPOSIT: True,
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
            ),
        },
        {
            PARAMETR.MODULE: MODULES.LENDINGS,
            PARAMETR.SETTINGS: LANDINGS_SETTINGS(
                PARAMS=[
                    {
                        PARAMETR.NETWORK: Client_Networks.zksync,
                        PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
                        PARAMETR.VALUE: (10, 10),
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
            ),
        },
    ]


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


async def mint_nfts():
    await Web3Nft.mint_use_database(settings=MINT_NFT_SETTINGS)


async def warm_up_swaps():
    await WarmUPSwaps.warmup(settings=WARMUPSWAPS_SETTINGS)


async def warm_up_refuel():
    await WarmUpRefuel.warm_up_refuel(settings=REFUEL_SETTINGS)


async def get_fees_refuel():
    await WarmUpRefuel.get_fees(apps=REFUEL_SETTINGS.CHECK_COMISSION_NETWORKS)


async def multitasks():
    await start_multitasks(settings=MULTITASKS_SETTINGS)


async def deploy_contracts():
    await Deployer.deploy_with_database(settings=DEPLOY_SETTINGS)


async def create_wallets():
    await Create_Wallets().create_wallets(
        count=CREATE_WALLETS_SETTIGS.COUNT, filename=CREATE_WALLETS_SETTIGS.FILE
    )


async def check_balance():
    await check_balances(settings=CHECK_BALANCES_SETTINGS)

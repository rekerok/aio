from modules import *
from config import Network, TOKENS
from settings import Client_Networks
from utils import TYPES_OF_TRANSACTION, PARAMETR


class EXCHANGES:
    OKX = OKX
    BINANCE = Binance
    BITGET = Bitget


class DEX:
    ONE_INCH = InchSwap
    IZUMI = IzumiSwap
    PANCAKESWAP = PancakeSwap
    ODOS = OdosSwap
    OPENOCEAN = OpenoceanSwap
    SUSHI = SushiSwap
    SYNCSWAP = SyncSwap
    ZKSWAP = ZkSwap
    BASESWAP = BaseSwap
    ZEROX = Zerox
    XY_FINANCE_SWAP = XY_finance_swap
    RANGO_SWAP = RangoSwap
    SKYDROME = Skydrome
    MUTE = Mute
    SPACEFI = SpaceFi
    ZEBRA = Zebra
    SYMBIOSIS = Symbiosis
    NITRO_SWAP = NitroSwap
    ACROSS = Across
    STARGATE = Stargate
    ORBITER = Orbiter
    NITRO = Nitro
    XY_FINANCE_BRIDGE = XY_finance_bridge
    RELAY = Relay
    TESTNET_BRIDGE_LAYERZERO = Testnet_Bridge_Layerzero
    TESTNET_BRIDGES = Testnet_Bridges
    HYPERLANE_ETH = Hyperlane
    # RANGO_BRIDGE = Rango_Bridge
    RUBYSCORE_VOTE = rubyscore


class LENDINGS:
    AAVE = Aave
    BASILISK = Basilisk
    ERALEND = Eralend
    LAYERBANK = Layerbank
    MOONWELL = Moonwell
    REACTOR_FUSION = Reactor_Fusion
    ZEROLEND = ZeroLend


class NFTS:
    FREE_NFT = Free_NFT
    L2PASS = L2pass_NFT
    NFT2ME = NFT2ME


class REFUEL_APP:
    MERKLY = Merkly
    L2PASS = L2Pass


class MODULES:
    # OKX_WITHDRAW = OKX.withdraw_use_database
    TRANSFER = Transfers.transfer_use_database
    SWAPS = Web3Swapper.swap_use_database
    BRIDGES = Web3Bridger.swap_use_database
    LENDINGS = Web3Lending.landing_use_database
    MINT_NFT = Web3Nft.mint_use_database
    # WARMUP_SWAPS = WarmUPSwaps.warmup
    # WARMUP_REFUEL = WarmUpRefuel.warm_up_refuel
    DEPLOY_CONTRACTS = Deployer.deploy_with_database
    RUBYSCORE_VOTE = rubyscore


class OKX_settings:
    SLEEP: tuple[int] = (60, 200)
    WAIT_TO_SEND = False
    ATTEMPT_WAIT_WITHDRAW = 15
    PROXY: str = ""  # "http://user:pass@ip:port"

    DATA: list[dict] = [
        {
            PARAMETR.TYPE_EXCHANGE: EXCHANGES.BITGET,
            PARAMETR.API_KEY: "",
            PARAMETR.API_SECRET: "",
            PARAMETR.PASSWORD: "",
        }
    ]

    PARAMS: list[dict] = [
        {
            PARAMETR.TOKENS: [{PARAMETR.NETWORK: "BASE", PARAMETR.TOKEN: "ETH"}],
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
    SLEEP = (10, 50)
    SLIPPAGE = 1

    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.arbitrum,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (2, 5),
            PARAMETR.FROM_DATA: [TOKENS.ARBITRUM.ETH],
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.MAX_BALANCE: 1000,
            PARAMETR.TO_DATA: [
                {
                    PARAMETR.TO_TOKEN: TOKENS.ARBITRUM.USDT,
                    PARAMETR.DEXS: [DEX.SUSHI],
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
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.AMOUNT,
            PARAMETR.VALUE: (0.00001, 0.00001),
            PARAMETR.FROM_DATA: [
                # {
                #     PARAMETR.NETWORK: Client_Networks.optimism,
                #     PARAMETR.FROM_TOKEN: TOKENS.OPTIMISM.ETH,
                # },
                {
                    PARAMETR.NETWORK: Client_Networks.arbitrum,
                    PARAMETR.FROM_TOKEN: TOKENS.ARBITRUM.ETH,
                },
            ],
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.TO_DATA: [
                {
                    PARAMETR.NETWORK: Network.SEPOLIA,
                    PARAMETR.TO_TOKEN: TOKENS.SEPOLIA.ETH,
                    PARAMETR.DEXS: [DEX.TESTNET_BRIDGE_LAYERZERO],
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


class DEP_TO_NETWORK_SETTINGS:
    SLEEPS = {
        PARAMETR.AFTER_WITHDRAW: (60 * 4, 60 * 10),
        PARAMETR.BETWEEN_WALLETS: (60 * 10, 60 * 20),
    }
    OKX = {
        PARAMETR.API_KEY: "",
        PARAMETR.API_SECRET: "",
        PARAMETR.PASSWORD: "",
        PARAMETR.ATTEMPT: 15,
    }
    CHANGE_NETWORK = (
        True  # Если сеть в которую депаешь совпадет с той в которую будет деп
    )
    PARAMS = {
        PARAMETR.VALUE: (0.002, 0.004),
        PARAMETR.TOKENS: [
            {
                PARAMETR.TOKEN: TOKENS.BASE.ETH,
                PARAMETR.NETWORK: Client_Networks.base,
                PARAMETR.DEXS: [
                    DEX.STARGATE,
                ],
            },
            # {
            #     PARAMETR.TOKEN: TOKENS.OPTIMISM.ETH,
            #     PARAMETR.NETWORK: Client_Networks.optimism,
            #     PARAMETR.DEXS: [
            #         DEX.STARGATE,
            #     ],
            # },
            # {
            #     PARAMETR.TOKEN: TOKENS.ARBITRUM.ETH,
            #     PARAMETR.NETWORK: Client_Networks.arbitrum,
            #     PARAMETR.DEXS: [
            #         DEX.STARGATE,
            #     ],
            # },
        ],
        PARAMETR.TO_TOKEN: [
            {
                PARAMETR.NETWORK: Network.BASE,
                PARAMETR.TOKEN: TOKENS.BASE.ETH,
            },
            # {
            #     PARAMETR.NETWORK: Network.ARBITRUM,
            #     PARAMETR.TOKEN: TOKENS.ARBITRUM.ETH,
            # },
            {
                PARAMETR.NETWORK: Network.OPTIMISM,
                PARAMETR.TOKEN: TOKENS.OPTIMISM.ETH,
            },
        ],
    }


class LENDINGS_SETTINGS:
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
            PARAMETR.NETWORK: Client_Networks.base,
            PARAMETR.NFTS: [
                {
                    PARAMETR.DEX: NFTS.FREE_NFT,
                    PARAMETR.CONTRACTS: ["0xb3da098a7251a647892203e0c256b4398d131a54"],
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
    SLEEP = (60 * 2, 60 * 3)
    SLIPPAGE = 1
    USE_MAX_BALANCE = True
    WALLETS_FILE = ""  # DEFAULT files/wallets.txt
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.COUNT_TRANSACTION: (2, 4),
            PARAMETR.DEXS: [DEX.XY_FINANCE_SWAP, DEX.ODOS, DEX.ZKSWAP],
            PARAMETR.TOKENS: [
                {
                    PARAMETR.TOKEN: TOKENS.ZKSYNC.USDT,
                    PARAMETR.VALUE: (50, 60),
                    PARAMETR.MIN_BALANCE: 1,
                    PARAMETR.MAX_BALANCE: 100,
                },
                {
                    PARAMETR.TOKEN: TOKENS.ZKSYNC.USDC,
                    PARAMETR.VALUE: (50, 60),
                    PARAMETR.MIN_BALANCE: 1,
                    PARAMETR.MAX_BALANCE: 100,
                },
                {
                    PARAMETR.TOKEN: TOKENS.ZKSYNC.ETH,
                    PARAMETR.VALUE: (50, 60),
                    PARAMETR.MIN_BALANCE: 0,
                    PARAMETR.MAX_BALANCE: 100,
                },
            ],
        },
        {
            PARAMETR.NETWORK: Client_Networks.base,
            PARAMETR.DEXS: [
                DEX.ODOS,
                # DEX.XY_FINANCE_SWAP,
                DEX.ZEROX,
                # DEX.SUSHI,
            ],
            PARAMETR.COUNT_TRANSACTION: (10, 20),
            PARAMETR.TOKENS: [
                {
                    PARAMETR.TOKEN: TOKENS.BASE.USDbC,
                    PARAMETR.VALUE: (100, 100),
                    PARAMETR.MIN_BALANCE: 1,
                    PARAMETR.MAX_BALANCE: 100,
                },
                {
                    PARAMETR.TOKEN: TOKENS.BASE.ETH,
                    PARAMETR.VALUE: (50, 70),
                    PARAMETR.MIN_BALANCE: 0,
                    PARAMETR.MAX_BALANCE: 100,
                },
            ],
        },
    ]

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


class WARMUP_APPROVER_MODE_SETTINGS:
    SLEEP = (60 * 2, 60 * 3)
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.COUNT_TRANSACTION: (5, 10),
            PARAMETR.CONTRACTS: [
                "0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d",
                "0x5673B6e6e51dE3479B8deB22dF46B12308db5E1e",
                "0x5673B6e6e51dE3479B8deB22dF46B12308db5E1e",
            ],
            PARAMETR.TOKENS: [
                {
                    PARAMETR.TOKEN: TOKENS.ZKSYNC.USDT,
                    PARAMETR.VALUE: (10, 30),
                },
                {
                    PARAMETR.TOKEN: TOKENS.ZKSYNC.USDC,
                    PARAMETR.VALUE: (10, 30),
                },
                {
                    PARAMETR.TOKEN: TOKENS.ZKSYNC.DAI,
                    PARAMETR.VALUE: (10, 30),
                },
            ],
        },
    ]


class MERKLY_REFUEL_SETTINGS:
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


class RYBYSCORE_VOTE_SETTINGS:
    SLEEP = (60 * 1, 60 * 3)
    WALLETS_FILE: str = ""
    PARAMS = [
        {PARAMETR.NETWORK: Client_Networks.scroll, PARAMETR.COUNT_TRANSACTION: (1, 1)},
        {PARAMETR.NETWORK: Client_Networks.zksync, PARAMETR.COUNT_TRANSACTION: (1, 3)},
        {PARAMETR.NETWORK: Client_Networks.base, PARAMETR.COUNT_TRANSACTION: (1, 3)},
    ]

    ######### NOT CHANGE #########
    def __init__(
        self,
        SLEEP: tuple[int] = None,
        COUNT: tuple[int] = None,
        WALLETS_FILE: str = None,
    ) -> None:
        if SLEEP is not None:
            self.SLEEP = SLEEP
        if COUNT is not None:
            self.COUNT = COUNT
        if WALLETS_FILE is not None:
            self.WALLETS_FILE = WALLETS_FILE


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
            PARAMETR.TOKENS: [
                TOKENS.SCROLL.ETH,
                TOKENS.SCROLL.USDC,
                TOKENS.SCROLL.USDT,
            ],
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
                TOKENS.POLYGON.USDC_BRIDGED,
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


class MULTITASKS_SETTINGS:
    SLEEP_BETWEEN_MODULES = (60 * 15, 60 * 25)

    TASKS = [
        {
            PARAMETR.MODULE: MODULES.SWAPS,
            PARAMETR.SETTINGS: SWAP_SETTINGS(
                SLEEP=(60 * 5, 60 * 10),
                PARAMS=[
                    {
                        PARAMETR.NETWORK: Client_Networks.zksync,
                        PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
                        PARAMETR.VALUE: (90, 95),
                        PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.ETH,
                        PARAMETR.MIN_BALANCE: 0,
                        PARAMETR.MAX_BALANCE: 1000,
                        PARAMETR.TO_TOKENS: [
                            {
                                PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.USDC,
                                PARAMETR.DEXS: [
                                    DEX.ODOS,
                                    DEX.IZUMI,
                                    DEX.SPACEFI,
                                    DEX.MUTE,
                                    DEX.XY_FINANCE_SWAP,
                                ],
                            },
                            {
                                PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.USDT,
                                PARAMETR.DEXS: [
                                    DEX.ODOS,
                                    DEX.IZUMI,
                                    DEX.SPACEFI,
                                    DEX.MUTE,
                                    DEX.XY_FINANCE_SWAP,
                                    DEX.SYNCSWAP,
                                ],
                            },
                        ],
                        PARAMETR.WALLETS_FILE: "",
                    },
                ],
            ),
        },
        {
            PARAMETR.MODULE: MODULES.SWAPS,
            PARAMETR.SETTINGS: SWAP_SETTINGS(
                SLEEP=(60 * 5, 60 * 10),
                PARAMS=[
                    {
                        PARAMETR.NETWORK: Client_Networks.zksync,
                        PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
                        PARAMETR.VALUE: (100, 100),
                        PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.USDC,
                        PARAMETR.MIN_BALANCE: 100,
                        PARAMETR.MAX_BALANCE: 1000,
                        PARAMETR.TO_TOKENS: [
                            {
                                PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.USDT,
                                PARAMETR.DEXS: [
                                    DEX.ODOS,
                                    DEX.IZUMI,
                                    DEX.SPACEFI,
                                    DEX.MUTE,
                                    DEX.XY_FINANCE_SWAP,
                                    DEX.SYNCSWAP,
                                ],
                            },
                        ],
                        PARAMETR.WALLETS_FILE: "",
                    },
                    {
                        PARAMETR.NETWORK: Client_Networks.zksync,
                        PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
                        PARAMETR.VALUE: (100, 100),
                        PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.USDT,
                        PARAMETR.MIN_BALANCE: 100,
                        PARAMETR.MAX_BALANCE: 1000,
                        PARAMETR.TO_TOKENS: [
                            {
                                PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.USDC,
                                PARAMETR.DEXS: [
                                    DEX.ODOS,
                                    DEX.IZUMI,
                                    DEX.SPACEFI,
                                    DEX.MUTE,
                                    DEX.XY_FINANCE_SWAP,
                                ],
                            },
                        ],
                        PARAMETR.WALLETS_FILE: "",
                    },
                ],
            ),
        },
        {
            PARAMETR.MODULE: MODULES.SWAPS,
            PARAMETR.SETTINGS: SWAP_SETTINGS(
                SLEEP=(60 * 5, 60 * 10),
                PARAMS=[
                    {
                        PARAMETR.NETWORK: Client_Networks.zksync,
                        PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
                        PARAMETR.VALUE: (100, 100),
                        PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.USDC,
                        PARAMETR.MIN_BALANCE: 100,
                        PARAMETR.MAX_BALANCE: 1000,
                        PARAMETR.TO_TOKENS: [
                            {
                                PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.ETH,
                                PARAMETR.DEXS: [
                                    DEX.ODOS,
                                    DEX.IZUMI,
                                    DEX.SPACEFI,
                                    DEX.MUTE,
                                    DEX.XY_FINANCE_SWAP,
                                    DEX.SYNCSWAP,
                                ],
                            },
                        ],
                        PARAMETR.WALLETS_FILE: "",
                    },
                    {
                        PARAMETR.NETWORK: Client_Networks.zksync,
                        PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
                        PARAMETR.VALUE: (100, 100),
                        PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.USDT,
                        PARAMETR.MIN_BALANCE: 100,
                        PARAMETR.MAX_BALANCE: 1000,
                        PARAMETR.TO_TOKENS: [
                            {
                                PARAMETR.TO_TOKEN: TOKENS.ZKSYNC.ETH,
                                PARAMETR.DEXS: [
                                    DEX.ODOS,
                                    DEX.IZUMI,
                                    DEX.SPACEFI,
                                    DEX.MUTE,
                                    DEX.XY_FINANCE_SWAP,
                                    DEX.SYNCSWAP,
                                ],
                            },
                        ],
                        PARAMETR.WALLETS_FILE: "",
                    },
                ],
            ),
        },
    ]


### NOT CHANGE ###
async def exhange_withdrawer():
    await withdraw_use_database(settings=OKX_settings)


async def transfers():
    await Transfers.transfer_use_database(settings=TRANSFERS_SETTINGS)


async def check_nft():
    await Check_NFT.check_nft(settings=CHECK_NFT_SETTINGS)


async def swaps():
    await Web3Swapper.swap_use_database(settings=SWAP_SETTINGS)


async def bridges():
    await Web3Bridger.swap_use_database(settings=BRIDGE_SETTINGS)


async def landings():
    await Web3Lending.landing_use_database(settings=LENDINGS_SETTINGS)


async def dep_to_networks():
    await dep_to_network(settings=DEP_TO_NETWORK_SETTINGS)


async def mint_nfts():
    await Web3Nft.mint_use_database(settings=MINT_NFT_SETTINGS)


async def warm_up_swaps():
    await WarmUPSwaps.warmup(settings=WARMUPSWAPS_SETTINGS)


# async def warm_up_refuel():
#     await WarmUpRefuel.warm_up_refuel(settings=REFUEL_SETTINGS)


async def approve_warmup():
    await warmup_approver_mode(settings=WARMUP_APPROVER_MODE_SETTINGS)


async def get_fees_refuel():
    await WarmUpRefuel.get_fees(apps=MERKLY_REFUEL_SETTINGS.CHECK_COMISSION_NETWORKS)


async def get_hyperlane_eth_fee():
    await Hyperlane.check_fees()


async def multitasks():
    await start_multitasks(settings=MULTITASKS_SETTINGS)


async def rubyscore_vote():
    await rubyscore(settings=RYBYSCORE_VOTE_SETTINGS)


async def deploy_contracts():
    await Deployer.deploy_with_database(settings=DEPLOY_SETTINGS)


async def create_wallets():
    await Create_Wallets().create_wallets(
        count=CREATE_WALLETS_SETTIGS.COUNT, filename=CREATE_WALLETS_SETTIGS.FILE
    )


async def check_balance():
    await check_balances(settings=CHECK_BALANCES_SETTINGS)

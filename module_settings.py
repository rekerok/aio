from modules import *
from config import Network
from settings import Client_Networks
from utils import TYPES_OF_TRANSACTION, PARAMETR, TOKENS


class DEX:
    ONE_INCH = InchSwap
    IZUMI = IzumiSwap
    ODOS = OdosSwap
    OPENOCEAN = OpenoceanSwap
    SUSHI = SushiSwap
    SYNCSWAP = SyncSwap
    WOOFI = WoofiSwap


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
            PARAMETR.NETWORK: "Linea",
            PARAMETR.SYMBOL: "ETH",
            PARAMETR.VALUE: (0.01494673, 0.02241770),
            PARAMETR.ROUND: (3, 5),
            PARAMETR.WALLETS_FILE: "",
        },
    ]
    SLEEP: tuple[int] = (60, 200)


class TRANSFERS_SETTINGS:
    PARAMS: list[dict] = [
        {
            PARAMETR.NETWORK: Client_Networks.linea,
            PARAMETR.TOKEN_ADDRESS: "",
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (90, 95),
            PARAMETR.MIN_BALANCE: 0.00075,
        },
    ]
    SLEEP: tuple[int] = (100, 300)


class SWAP_SETTINGS:
    PARAMS = [
        {
            PARAMETR.NETWORK: Client_Networks.zksync,
            PARAMETR.TYPE_TRANSACTION: TYPES_OF_TRANSACTION.PERCENT,
            PARAMETR.VALUE: (25, 40),
            PARAMETR.FROM_TOKEN: TOKENS.ZKSYNC.ETH,
            PARAMETR.MIN_BALANCE: 0,
            PARAMETR.TO_TOKENS: [
                {
                    PARAMETR.TOKEN_ADDRESS: TOKENS.ZKSYNC.USDT,
                    PARAMETR.DEXS: [DEX.SYNCSWAP, DEX.ONE_INCH],
                },
            ],
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
        DEX.ONE_INCH: [
            {
                PARAMETR.NETWORK: Client_Networks.zksync,
                PARAMETR.TOKENS: [
                    {
                        PARAMETR.TOKEN_ADDRESS: TOKENS.ZKSYNC.DAI,
                        PARAMETR.MIN_BALANCE: 10,
                    },
                    {
                        PARAMETR.TOKEN_ADDRESS: TOKENS.ZKSYNC.USDC,
                        PARAMETR.MIN_BALANCE: 10,
                    },
                    {
                        PARAMETR.TOKEN_ADDRESS: TOKENS.ZKSYNC.USDC,
                        PARAMETR.MIN_BALANCE: 10,
                    },
                ],
                PARAMETR.COUNT_TRANSACTION: (3, 4),
                PARAMETR.VALUE: (100, 100),
            },
        ],
        DEX.SYNCSWAP: [
            {
                PARAMETR.NETWORK: Client_Networks.zksync,
                PARAMETR.TOKENS: [
                    {
                        PARAMETR.TOKEN_ADDRESS: TOKENS.ZKSYNC.USDC,
                        PARAMETR.MIN_BALANCE: 10,
                    },
                    {
                        PARAMETR.TOKEN_ADDRESS: TOKENS.ZKSYNC.USDC,
                        PARAMETR.MIN_BALANCE: 10,
                    },
                ],
                PARAMETR.COUNT_TRANSACTION: (1, 2),
                PARAMETR.VALUE: (100, 100),
            },
        ],
    }
    SLIPPAGE = 3
    SLEEP = (100, 200)


class REFUEL_SETTINGS:
    CHECK_COMISSION_NETWORKS = {
        REFUEL_APP.MERKLY: [Client_Networks.arbitrum, Client_Networks.avalanche],
        REFUEL_APP.L2PASS: [Client_Networks.arbitrum, Client_Networks.avalanche],
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
                    PARAMETR.NAME: "merkly",
                    PARAMETR.BYTECODE_CONTRACT: "0x60806040526000805461ffff1916905534801561001b57600080fd5b5060fb8061002a6000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c80630c55699c146037578063b49004e914605b575b600080fd5b60005460449061ffff1681565b60405161ffff909116815260200160405180910390f35b60616063565b005b60008054600191908190607a90849061ffff166096565b92506101000a81548161ffff021916908361ffff160217905550565b61ffff81811683821601908082111560be57634e487b7160e01b600052601160045260246000fd5b509291505056fea2646970667358221220666c87ec501268817295a4ca1fc6e3859faf241f38dd688f145135970920009264736f6c63430008120033",
                }
            ],
            "count": (1, 1),
        }
    ]
    SLEEP = (100, 200)


### NOT CHANGE ###
async def okx_withdrawer():
    await OKX.withdraw_use_database(settings=OKX_settings)


async def transfers():
    await Transfers.transfer_use_database(settings=TRANSFERS_SETTINGS)


async def check_nft():
    await Check_NFT.check_nft(settings=CHECK_NFT_SETTINGS)


async def swaps():
    await Web3Swapper.swap_use_database(settings=SWAP_SETTINGS)


async def warm_up_swaps():
    await WarmUPSwaps.warmup(settings=WARMUPSWAPS_SETTINGS)


async def warm_up_refuel():
    await WarmUpRefuel.warm_up_refuel(settings=REFUEL_SETTINGS)


async def get_fees_refuel():
    await WarmUpRefuel.get_fees(apps=REFUEL_SETTINGS.CHECK_COMISSION_NETWORKS)


async def deploy_contracts():
    await Deployer.deploy_with_database(settings=DEPLOY_SETTINGS)

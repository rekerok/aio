from config import Network
from utils.enums import NETWORK_FIELDS

LIMIT_GWEI = 30
GAS_MULTIPLAY = 1.3
COUNT_CHECK_GAS = 10000
SLEEP_AFTER_APPROOVE = (50, 70)
USE_PROXY = False

### API KEYS ###
INCH_SWAP_KEY = ""
ZEROX_KEY = ""

### REFFERAL ###
USE_REF = False
FEE = 1


### НАСТРОЙКИ СЕТЕЙ ###
class Client_Networks:
    ethereum = {
        NETWORK_FIELDS.NAME: Network.ETHEREUM,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/eth",
        ],
        NETWORK_FIELDS.EXPLORER: "https://etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
    }

    arbitrum = {
        NETWORK_FIELDS.NAME: Network.ARBITRUM,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/arbitrum",
            "https://arbitrum.llamarpc.com",
            "wss://arbitrum-one.publicnode.com",
            "https://arbitrum-one.public.blastapi.io",
        ],
        NETWORK_FIELDS.EXPLORER: "https://arbiscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
    }

    optimism = {
        NETWORK_FIELDS.NAME: Network.OPTIMISM,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/optimism",
            "wss://optimism.publicnode.com",
            "https://rpc.optimism.gateway.fm",
            "https://optimism.blockpi.network/v1/rpc/public",
        ],
        NETWORK_FIELDS.EXPLORER: "https://optimistic.etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    base = {
        NETWORK_FIELDS.NAME: Network.BASE,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/base",
            "https://base.llamarpc.com",
            "https://mainnet.base.org",
            "https://base.gateway.tenderly.co",
        ],
        NETWORK_FIELDS.EXPLORER: "https://basescan.org/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
        NETWORK_FIELDS.LIMIT_GAS: 1,
    }

    zksync = {
        NETWORK_FIELDS.NAME: Network.ZKSYNC,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/zksync_era",
            "https://mainnet.era.zksync.io",
            "https://1rpc.io/zksync2-era",
        ],
        NETWORK_FIELDS.EXPLORER: "https://explorer.zksync.io/",
        NETWORK_FIELDS.EIP1559: False,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    scroll = {
        NETWORK_FIELDS.NAME: Network.SCROLL,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/scroll",
        ],
        NETWORK_FIELDS.EXPLORER: "https://scrollscan.com/",
        NETWORK_FIELDS.EIP1559: False,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
        NETWORK_FIELDS.LIMIT_GAS: 0.5,
    }

    nova = {
        NETWORK_FIELDS.NAME: Network.NOVA,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/arbitrumnova",
            "https://arbitrum-nova.public.blastapi.io",
            "https://arbitrum-nova.publicnode.com",
            "https://arbitrum-nova.blockpi.network/v1/rpc/public",
        ],
        NETWORK_FIELDS.EXPLORER: "https://nova.arbiscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    linea = {
        NETWORK_FIELDS.NAME: Network.LINEA,
        NETWORK_FIELDS.RPCS: [
            "https://linea.blockpi.network/v1/rpc/public",
            "https://rpc.linea.build",
        ],
        NETWORK_FIELDS.EXPLORER: "https://lineascan.build/",
        NETWORK_FIELDS.EIP1559: False,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    avalanche = {
        NETWORK_FIELDS.NAME: Network.AVALANCHE,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/avalanche",
            "https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc",
            "https://avalanche.blockpi.network/v1/rpc/public",
            "https://1rpc.io/avax/c",
        ],
        NETWORK_FIELDS.EXPLORER: "https://snowtrace.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "AVAX",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    polygon = {
        NETWORK_FIELDS.NAME: Network.POLYGON,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/polygon",
            "wss://polygon.gateway.tenderly.co",
            "wss://polygon-bor.publicnode.com",
            "https://polygon-bor.publicnode.com",
        ],
        NETWORK_FIELDS.EXPLORER: "https://polygonscan.com/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "MATIC",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    fantom = {
        NETWORK_FIELDS.NAME: Network.FANTOM,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/fantom/",
        ],
        NETWORK_FIELDS.EXPLORER: "https://ftmscan.com/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "FTM",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    bsc = {
        NETWORK_FIELDS.NAME: Network.BSC,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/bsc/",
            "wss://bsc.publicnode.com",
            "https://bsc-dataseed.bnbchain.org",
        ],
        NETWORK_FIELDS.EXPLORER: "https://bscscan.com/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "BNB",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

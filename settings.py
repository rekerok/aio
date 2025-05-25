from config import Network
from utils.enums import NETWORK_FIELDS

LIMIT_GWEI = 30
GAS_MULTIPLAY = (1.3, 1.9)
COUNT_CHECK_GAS = 1000000
SLEEP_AFTER_APPROOVE = (60, 150)
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
            "https://eth.drpc.org",
        ],
        NETWORK_FIELDS.EXPLORER: "https://etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
        NETWORK_FIELDS.LIMIT_GAS: 0.00001,
    }

    arbitrum = {
        NETWORK_FIELDS.NAME: Network.ARBITRUM,
        NETWORK_FIELDS.RPCS: [
            "https://arbitrum-one.public.blastapi.io",
        ],
        NETWORK_FIELDS.EXPLORER: "https://arbiscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    optimism = {
        NETWORK_FIELDS.NAME: Network.OPTIMISM,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/optimism",
            "https://optimism.meowrpc.com",
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
        ],
        NETWORK_FIELDS.EXPLORER: "https://explorer.zksync.io/",
        NETWORK_FIELDS.EIP1559: False,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    scroll = {
        NETWORK_FIELDS.NAME: Network.SCROLL,
        NETWORK_FIELDS.RPCS: [
            "https://scroll-mainnet.public.blastapi.io",
            "https://rpc.scroll.io",
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
            "https://1rpc.io/linea",
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
            "wss://0xrpc.io/avax",
        ],
        NETWORK_FIELDS.EXPLORER: "https://snowtrace.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "AVAX",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    sepolia = {
        NETWORK_FIELDS.NAME: Network.SEPOLIA,
        NETWORK_FIELDS.RPCS: [
            "https://1rpc.io/sepolia",
        ],
        NETWORK_FIELDS.EXPLORER: "https://sepolia.etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    arbitrum_sepolia = {
        NETWORK_FIELDS.NAME: Network.ARBITRUM,
        NETWORK_FIELDS.RPCS: [
            "https://sepolia-rollup.arbitrum.io/rpc",
        ],
        NETWORK_FIELDS.EXPLORER: "https://sepolia.arbiscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    base_sepolia = {
        NETWORK_FIELDS.NAME: Network.BASE,
        NETWORK_FIELDS.RPCS: [
            "https://sepolia.base.org",
        ],
        NETWORK_FIELDS.EXPLORER: "https://sepolia.basescan.org/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    optimism_sepolia = {
        NETWORK_FIELDS.NAME: Network.OPTIMISM,
        NETWORK_FIELDS.RPCS: [
            "https://sepolia.optimism.io",
        ],
        NETWORK_FIELDS.EXPLORER: "https://sepolia-optimism.etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }
    optimism_sepolia = {
        NETWORK_FIELDS.NAME: Network.OPTIMISM,
        NETWORK_FIELDS.RPCS: [
            "https://sepolia.optimism.io",
        ],
        NETWORK_FIELDS.EXPLORER: "https://sepolia-optimism.etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    sahara = {
        NETWORK_FIELDS.NAME: Network.SAHARA,
        NETWORK_FIELDS.RPCS: [
            "https://mainnet.saharalabs.ai",
        ],
        NETWORK_FIELDS.EXPLORER: "https://explorer.saharaa.info/",
        NETWORK_FIELDS.EIP1559: False,
        NETWORK_FIELDS.NATIVE_TOKEN: "SAHARA",
        NETWORK_FIELDS.CHECK_GAS: False,
    }
    
    t3rn = {
        NETWORK_FIELDS.NAME: Network.T3RN,
        NETWORK_FIELDS.RPCS: [
            "https://brn.rpc.caldera.xyz/http",
        ],
        NETWORK_FIELDS.EXPLORER: "https://brn.explorer.caldera.xyz/",
        NETWORK_FIELDS.EIP1559: False,
        NETWORK_FIELDS.NATIVE_TOKEN: "BRN",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    polygon = {
        NETWORK_FIELDS.NAME: Network.POLYGON,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/polygon",
            "https://polygon.rpc.subquery.network/public",
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
            "https://1rpc.io/bnb",
        ],
        NETWORK_FIELDS.EXPLORER: "https://bscscan.com/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "BNB",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

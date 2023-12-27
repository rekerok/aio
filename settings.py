from config import Network
from utils.enums import NETWORK_FIELDS

LIMIT_GWEI = 35
GAS_MULTIPLAY = 1.3
COUNT_CHECK_GAS = 1000

### API KEYS ###
INCH_SWAP_KEY = ""


### НАСТРОЙКИ СЕТЕЙ ###
class Client_Networks:
    ethereum = {
        NETWORK_FIELDS.NAME: Network.ETHEREUM,
        NETWORK_FIELDS.RPCS: [
            "https://eth.llamarpc.com",
            "wss://ethereum.publicnode.com",
            "https://rpc.mevblocker.io",
        ],
        NETWORK_FIELDS.EXPLORER: "https://etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
    }

    arbitrum = {
        NETWORK_FIELDS.NAME: Network.ARBITRUM,
        NETWORK_FIELDS.RPCS: [
            "https://arbitrum.llamarpc.com",
            "wss://arbitrum-one.publicnode.com",
            "https://endpoints.omniatech.io/v1/arbitrum/one/public",
        ],
        NETWORK_FIELDS.EXPLORER: "https://arbiscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
    }

    optimism = {
        NETWORK_FIELDS.NAME: Network.OPTIMISM,
        NETWORK_FIELDS.RPCS: [
            "https://optimism.llamarpc.com",
            "wss://optimism.publicnode.com",
            "https://mainnet.optimism.io",
        ],
        NETWORK_FIELDS.EXPLORER: "https://optimistic.etherscan.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    base = {
        NETWORK_FIELDS.NAME: Network.BASE,
        NETWORK_FIELDS.RPCS: ["https://base.llamarpc.com"],
        NETWORK_FIELDS.EXPLORER: "https://basescan.org/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    zksync = {
        NETWORK_FIELDS.NAME: Network.ZKSYNC,
        NETWORK_FIELDS.RPCS: [
            "https://mainnet.era.zksync.io",
            "https://zksync-era.blockpi.network/v1/rpc/public",
        ],
        NETWORK_FIELDS.EXPLORER: "https://explorer.zksync.io/",
        NETWORK_FIELDS.EIP1559: False,
        NETWORK_FIELDS.NATIVE_TOKEN: "ETH",
        NETWORK_FIELDS.CHECK_GAS: True,
    }

    scroll = {
        NETWORK_FIELDS.NAME: Network.SCROLL,
        NETWORK_FIELDS.RPCS: [
            "https://scroll.blockpi.network/v1/rpc/public",
            "https://rpc-scroll.icecreamswap.com",
            "https://rpc.ankr.com/scroll",
        ],
        NETWORK_FIELDS.EXPLORER: "https://scrollscan.com/",
        NETWORK_FIELDS.EIP1559: False,
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
        NETWORK_FIELDS.CHECK_GAS: True,
    }

    avalanche = {
        NETWORK_FIELDS.NAME: Network.AVALANCHE,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/avalanche",
        ],
        NETWORK_FIELDS.EXPLORER: "https://snowtrace.io/",
        NETWORK_FIELDS.EIP1559: True,
        NETWORK_FIELDS.NATIVE_TOKEN: "AVAX",
        NETWORK_FIELDS.CHECK_GAS: False,
    }

    polygon = {
        NETWORK_FIELDS.NAME: Network.POLYGON,
        NETWORK_FIELDS.RPCS: [
            "https://rpc.ankr.com/polygon/",
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

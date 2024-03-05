from enum import Enum, auto


class TYPES_OF_TRANSACTION(Enum):
    AMOUNT = auto()
    PERCENT = auto()
    ALL_BALANCE = auto()


class RESULT_TRANSACTION(Enum):
    FAIL = auto()
    SUCCESS = auto()
    NOT_BALANCE = auto()


class NETWORK_FIELDS(Enum):
    NAME = auto()
    RPCS = auto()
    EIP1559 = auto()
    EXPLORER = auto()
    CHECK_GAS = auto()
    NATIVE_TOKEN = auto()


class PARAMETR(Enum):
    ID = auto()
    DEX = auto()
    DEXS = auto()
    NFTS = auto()
    NAME = auto()
    ROUND = auto()
    TOKEN = auto()
    VALUE = auto()
    TOKENS = auto()
    SYMBOL = auto()
    MODULE = auto()
    NETWORK = auto()
    NETWORKS = auto()
    TO_TOKEN = auto()
    NAME_NFT = auto()
    LENDINGS = auto()
    TO_CHAINS = auto()
    SETTINGS = auto()
    TO_TOKENS = auto()
    CONTRACTS = auto()
    FROM_TOKEN = auto()
    MAX_BALANCE = auto()
    MIN_BALANCE = auto()
    OKX_API_KEY = auto()
    OKX_PASSWORD = auto()
    WALLETS_FILE = auto()
    POOL_ADDRESS = auto()
    TOKEN_ADDRESS = auto()
    OKX_API_SECRET = auto()
    RECIPIENTS_FILE = auto()
    LENDING_DEPOSIT = auto()
    TYPE_TRANSACTION = auto()
    BYTECODE_CONTRACT = auto()
    COUNT_TRANSACTION = auto()


class TOKENS:
    class OPTIMISM:
        ETH = ""
        WETH = "0x4200000000000000000000000000000000000006"
        USDT = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"
        USDC = "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"
        USDC_BRIDGED = "0x7F5c764cBc14f9669B88837ca1490cCa17c31607"
        DAI = "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
        WBTC = "0x68f180fcCe6836688e9084f035309E29Bf0A2095"
        OP = "0x4200000000000000000000000000000000000042"

    class ARBITRUM:
        ETH = ""
        WETH = "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1"
        USDT = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
        USDC = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
        USDC_BRIDGED = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
        WBTC = "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"
        ARB = "0x912CE59144191C1204E64559FE8253a0e49E6548"

    class ZKSYNC:
        ETH = ""
        WETH = "0xf00DAD97284D0c6F06dc4Db3c32454D4292c6813"
        USDT = "0x493257fD37EDB34451f62EDf8D2a0C418852bA4C"
        USDC = "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4"
        DAI = "0x4B9eb6c0b6ea15176BBF62841C6B2A8a398cb656"
        WBTC = "0xBBeB516fb02a01611cBBE0453Fe3c580D7281011"

    class LINEA:
        ETH = ""
        WETH = "0x2C1b868d6596a18e32E61B901E4060C872647b6C"
        USDT = "0x2C1b868d6596a18e32E61B901E4060C872647b6C"
        USDC = "0x176211869cA2b568f2A7D4EE941E073a821EE1ff"
        DAI = "0x4AF15ec2A0BD43Db75dd04E62FAA3B8EF36b00d5"
        WBTC = "0x3aAB2285ddcDdaD8edf438C1bAB47e1a9D05a9b4"

    class SCROLL:
        ETH = ""
        WETH = "0x5300000000000000000000000000000000000004"
        USDT = "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df"
        USDC = "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4"
        DAI = "0xcA77eB3fEFe3725Dc33bccB54eDEFc3D9f764f97"
        WBTC = "0x3C1BCa5a656e69edCD0D4E36BEbb3FcDAcA60Cf1"

    class NOVA:
        ETH = ""
        WETH = "0x722E8BdD2ce80A4422E880164f2079488e115365"
        DAI = "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
        ARB = "0xf823C3cD3CeBE0a1fA952ba88Dc9EEf8e0Bf46AD"

    class BASE:
        ETH = ""
        WETH = "0x4200000000000000000000000000000000000006"
        USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        USDbC = "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca"
        DAI = "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb"

    class BSC:
        BSC = ""
        WBNB = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
        ETH = "0x2170Ed0880ac9A755fd29B2688956BD959F933F8"
        USDT = "0x55d398326f99059fF775485246999027B3197955"
        USDC = "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"

    class POLYGON:
        MATIC = ""
        WMATIC = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
        WETH = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"
        USDT = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
        USDC = "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359"
        USDC_BRIDGED = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        WBTC = "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6"

    class AVALANCHE:
        AVAX = ""
        WAVAX = "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7"
        USDT = "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7"
        USDC = "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E"
        BTC_B = "0x152b9d0FdC40C096757F570A51E494bd4b943E50"

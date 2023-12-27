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


class PARAMETR:
    DEXS = auto()
    NFTS = auto()
    NAME = auto()
    ROUND = auto()
    VALUE = auto()
    TOKENS = auto()
    SYMBOL = auto()
    NETWORK = auto()
    NETWORKS = auto()
    NAME_NFT = auto()
    TO_CHAINS = auto()
    TO_TOKENS = auto()
    CONTRACTS = auto()
    FROM_TOKEN = auto()
    MIN_BALANCE = auto()
    OKX_API_KEY = auto()
    OKX_PASSWORD = auto()
    WALLETS_FILE = auto()
    TOKEN_ADDRESS = auto()
    OKX_API_SECRET = auto()
    TYPE_TRANSACTION = auto()
    BYTECODE_CONTRACT = auto()
    COUNT_TRANSACTION = auto()

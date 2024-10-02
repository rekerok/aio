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
    LIMIT_GAS = auto()
    CHECK_GAS = auto()
    NATIVE_TOKEN = auto()


class PARAMETR(Enum):
    ID = auto()
    ABI = auto()
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
    ATTEMPT = auto()
    TO_DATA = auto()
    API_KEY = auto()
    NETWORK = auto()
    NETWORKS = auto()
    CONTRACT = auto()
    TO_TOKEN = auto()
    NAME_NFT = auto()
    LENDINGS = auto()
    SETTINGS = auto()
    PASSWORD = auto()
    TO_CHAINS = auto()
    TO_TOKENS = auto()
    CONTRACTS = auto()
    FROM_DATA = auto()
    FROM_TOKEN = auto()
    API_SECRET = auto()
    FROM_TOKENS = auto()
    MAX_BALANCE = auto()
    MIN_BALANCE = auto()
    WALLETS_FILE = auto()
    POOL_ADDRESS = auto()
    TOKEN_ADDRESS = auto()
    TYPE_EXCHANGE = auto()
    AFTER_WITHDRAW = auto()
    RECIPIENTS_FILE = auto()
    LENDING_DEPOSIT = auto()
    BETWEEN_WALLETS = auto()
    TYPE_TRANSACTION = auto()
    BYTECODE_CONTRACT = auto()
    COUNT_TRANSACTION = auto()

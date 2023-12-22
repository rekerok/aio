
from enum import Enum, auto


class TYPE_OF_TRANSACTION(Enum):
    ALL_BALANCE = auto()
    PERCENT = auto()
    AMOUNT = auto()

class STATUS(Enum):
    OK = auto()
    FAIL = auto()
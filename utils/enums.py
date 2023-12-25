
from enum import Enum, auto


class TYPE_OF_TRANSACTION(Enum):
    ALL_BALANCE = auto()
    PERCENT = auto()
    AMOUNT = auto()

class RESULT_TRANSACTION(Enum):
    SUCCESS = auto()
    FAIL = auto()
# Декоратор для повторных попыток
from functools import wraps

from loguru import logger

from utils.enums import RESULT_TRANSACTION


def retry_async(attempts: int = 3):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                result = await func(*args, **kwargs)
                if result == RESULT_TRANSACTION.SUCCESS:
                    return result
                logger.warning(f"Retry attempt {attempt + 1} failed.")
            return RESULT_TRANSACTION.FAIL

        return wrapper

    return decorator

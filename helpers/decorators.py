from utils import time


def check_gas(func):
    async def wrapper(*args, **kwargs):
        await time.wait_gas()
        await func(*args, **kwargs)

    return wrapper

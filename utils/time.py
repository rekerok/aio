from tqdm import trange
import time
import random
import asyncio
from settings import COUNT_CHECK_GAS
from loguru import logger
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.middleware import async_geth_poa_middleware


async def sleep_view(sleep: tuple):
    for i in trange(random.randint(*sleep), ncols=70):
        time.sleep(1)


async def get_gas(network: dict) -> int:
    try:
        rpcs: list[str] = network.get("rpc")
        w3 = AsyncWeb3(
            AsyncHTTPProvider(
                endpoint_uri=random.choice(rpcs),
            )
        )
        w3.middleware_onion.inject(async_geth_poa_middleware, layer=0)
        return w3.from_wei(await w3.eth.gas_price, "gwei")
    except:
        return None


async def wait_gas(w3, LIMIT_GWEI=None):

    for i in range(COUNT_CHECK_GAS):
        try:
            gas_now = w3.from_wei(await w3.eth.gas_price, "gwei")
        except:
            logger.error(f"Gas Receiving Error")
            continue
        if not gas_now:
            logger.error(f"Gas Receiving Error")
            continue
        if gas_now > LIMIT_GWEI:
            logger.info(
                f"Check GAS {i+1}/{COUNT_CHECK_GAS} GAS = {gas_now} > {LIMIT_GWEI}"
            )
            sleep_time = round(random.uniform(30, 60), 3)
            logger.info(f"SLEEP {sleep_time} sec")
            await asyncio.sleep(random.uniform(30, 60))
        else:
            logger.success(
                f"Check GAS {i+1}/{COUNT_CHECK_GAS} GAS = {gas_now} < {LIMIT_GWEI}"
            )
            return True
    return False

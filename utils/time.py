import asyncio
from logging import config
import random
import time
import tqdm
from loguru import logger
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.middleware import async_geth_poa_middleware
from networks import Networks
from settings import *


async def sleep_view(sleep: tuple):
    for i in tqdm.tqdm(range(random.randint(sleep[0], sleep[1]))):
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


async def wait_gas():
    gas_now = await get_gas(network=Networks.ethereum)
    if CHECK_GWEI:
        for i in range(COUNT_CHECK_GAS):
            gas_now = await get_gas(network=Networks.ethereum)
            if not gas_now:
                logger.error(f"Gas Receiving Error")
                continue
            if gas_now > LIMIT_GWEI:
                logger.info(f"Check GAS Try {i+1}/{COUNT_CHECK_GAS}")
                logger.info(f"GAS NOW {gas_now} > {LIMIT_GWEI}")
                sleep_time = round(random.uniform(30, 60), 3)
                logger.info(f"SLEEP {sleep_time} sec")
                await asyncio.sleep(random.uniform(30, 60))
            else:
                logger.success(f"GAS NOW {gas_now} < {LIMIT_GWEI}")
                break
    else:
        logger.info(f"GAS NOW {gas_now}")

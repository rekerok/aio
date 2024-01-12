import asyncio
import random
import aiohttp
from loguru import logger

import utils


def get_random_proxy():
    try:
        with open("files/proxy.txt", "r") as file:
            lines = [i.strip() for i in file.readlines()]
            return random.choice(lines)
    except Exception as error:
        logger.error(error)
        return []


async def get_json_aiohttp(
    url: str,
    proxy: str = None,
    params=None,
    headers={"Content-Type": "application/json"},
) -> dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(
                        f"HTTP request failed with status code {response.status}"
                    )
                    return None
    except Exception as error:
        logger.error(f"An error occurred during the HTTP request: {str(error)}")
        return None


async def post_request(
    url: str,
    data: dict = None,
    proxy: str = None,
    headers={"Content-Type": "application/json"},
):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url=url,
            headers=headers,
            json=data,
            proxy=proxy,
        )

        if response.status == 200:
            response_data = await response.json()

            return response_data
        else:
            return None

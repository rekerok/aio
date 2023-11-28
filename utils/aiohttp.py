import aiohttp


async def get_json_aiohttp(url: str, proxy: str = None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

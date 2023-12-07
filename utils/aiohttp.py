import aiohttp


async def get_json_aiohttp(url: str, proxy: str = None, data=None) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def post_request(url: str, data: dict = None, proxy: str = None):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url=url,
            headers={"Content-Type": "application/json"},
            json=data,
            proxy=proxy,
        )

        if response.status == 200:
            response_data = await response.json()

            return response_data
        else:
            return None

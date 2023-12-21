import aiohttp


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
                    print(f"HTTP request failed with status code {response.status}")
                    return None
    except Exception as e:
        print(f"An error occurred during the HTTP request: {str(e)}")
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

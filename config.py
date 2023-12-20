import asyncio
from utils import aiohttp
from utils import files
from utils import aiohttp

PRICES_TOKENS = asyncio.run(
    aiohttp.get_json_aiohttp(url="https://api.gateio.ws/api/v4/spot/tickers")
)

### ABIS ###
ERC20_ABI: dict = asyncio.run(files.load_json("files/abis/erc20.json"))
SUSHI_ABI: dict = asyncio.run(files.load_json("files/abis/sushiswap.json"))
WOOFI_ABI: dict = asyncio.run(files.load_json("files/abis/woofiswap.json"))
ODOS_ABI: dict = asyncio.run(files.load_json("files/abis/odosswap.json"))
SYNCSWAP_ABI: dict = {
    "router": asyncio.run(files.load_json("files/abis/syncswap_router.json")),
    "pool_factory": asyncio.run(
        files.load_json("files/abis/syncswap_pool_factory.json")
    ),
    "pool": asyncio.run(files.load_json("files/abis/syncswap_pool.json")),
}
MERKLY_ABI: dict = asyncio.run(files.load_json("files/abis/merkly.json"))

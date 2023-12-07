import asyncio
from utils import aiohttp
from utils import files
from utils import aiohttp

PRICES_TOKENS = asyncio.run(
    aiohttp.get_json_aiohttp(url="https://api.gateio.ws/api/v4/spot/tickers")
)

### ABIS ###
ERC20_ABI: dict = asyncio.run(files.load_json("files/abis/erc20.json"))
WOOFI_ABI: dict = asyncio.run(files.load_json("files/abis/woofiswap.json"))

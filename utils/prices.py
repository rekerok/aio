import ccxt


async def price_one_toke_in_other(in_token: str, out_token: str) -> float:
    exchange = ccxt.binance(
        {
            "enableRateLimit": True,
        }
    )

    price_in = exchange.fetch_ticker(f"{in_token.upper()}/USDT", params={})["last"]
    price_out = exchange.fetch_ticker(f"{out_token.upper()}/USDT", params={})["last"]

    return float(price_in / price_out)


async def get_price_token(token_name: str) -> float:
    token_name = token_name.upper()
    exchange = ccxt.okx(
        {
            "enableRateLimit": True,
        }
    )
    try:
        if token_name == "USDT":
            return 1
        return exchange.fetch_ticker(f"{token_name}/USDT", params={})["last"]
    except:
        return 0

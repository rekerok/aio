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
    exchange = ccxt.binance(
        {
            "enableRateLimit": True,
        }
    )
    try:
        return exchange.fetch_ticker(f"{token_name.upper()}/USDT", params={})["last"]
    except:
        return 0.0
    # asyncio.run(price_one_toke_in_other(in_token="btc", out_token="apt"))

import asyncio
import questionary
from questionary import Choice
from module_settings import *


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Withdraw from OKX", okx_withdrawer),
            Choice("2) Transfers module", transfers),
            Choice("3) Check NFT", check_nft),
            Choice("4) Woofi swap", woofi_swap),
            Choice("5) SushiSwap", sushi_swap),
            Choice("6) 1InchSwap", inch_swap),
            Choice("6) OdosSwap", odos_swap),
        ],
        qmark="⚙️ ",
        pointer="✅ ",
    ).ask()
    return result


async def main(module=None):
    await module()


if __name__ == "__main__":
    module = get_module()
    asyncio.run(main(module=module))
    # asyncio.run(main())

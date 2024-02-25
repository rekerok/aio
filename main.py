import os
import asyncio
from loguru import logger
import questionary
from module_settings import *
from questionary import Choice


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Withdraw from OKX", okx_withdrawer),
            Choice("2) Transfers", transfers),
            Choice("3) Check NFT", check_nft),
            Choice("4) Swap", swaps),
            Choice("5) Bridge", bridges),
            Choice("6) Lendings", landings),
            Choice("7) Mint NFT", mint_nfts),
            Choice("8) WarmUP swaps", warm_up_swaps),
            Choice("9) WarmUP refuel", warm_up_refuel),
            Choice("10) Get refuel fees", get_fees_refuel),
            Choice("11) Deploy contracts", deploy_contracts),
            Choice("12) Create wallets", create_wallets),
            Choice("13) Check balances", check_balance),
        ],
        qmark="⚙️ ",
        pointer="✅ ",
    ).ask()
    return result


async def main(module=None):
    await module()
    logger.debug("FINISHHHHHHHH")


if __name__ == "__main__":
    module = get_module()
    asyncio.run(main(module=module))
    # asyncio.run(main())

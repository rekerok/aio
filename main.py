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
            Choice("1) Withdraw exchange", exhange_withdrawer),
            Choice("2) Create csv file exchange", exhange_create_csv),
            Choice("3) Transfers", transfers),
            Choice("4) Check NFT", check_nft),
            Choice("5) Swap", swaps),
            Choice("6) Bridge", bridges),
            Choice("7) Lendings", landings),
            Choice("8) Dep to network", dep_to_networks),
            Choice("9) Mint NFT", mint_nfts),
            Choice("10) Rubyscore vote", rubyscore_vote),
            Choice("12) WarmUP swaps", warm_up_swaps),
            Choice("13) WarmUP refuel", warm_up_refuel),
            Choice("14) WarnUP approver mode", approve_warmup),
            Choice("15) Multi Tasks", multitasks),
            Choice("16) Get refuel fees", get_fees_refuel),
            Choice("17) Get hyperlane eth fees", get_hyperlane_eth_fee),
            Choice("18) Deploy contracts", deploy_contracts),
            Choice("19) Create wallets", create_wallets),
            # Choice("20) esxai reedemption", esxai_reedemption),
            Choice("21) Check balances", check_balance),
        ],
        qmark="⚙️ ",
        pointer="✅ ",
    ).ask()
    return result


async def main(module=None):
    logger.debug("STARTTTTTTTTT")
    await module()
    logger.debug("FINISHHHHHHHH")


if __name__ == "__main__":
    module = get_module()
    asyncio.run(main(module=module))
    # asyncio.run(main())

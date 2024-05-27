import random

from loguru import logger
import config
from modules.account import Account
from modules.web3Bridger import Web3Bridger
from modules.web3Client import Web3Client
from settings import Client_Networks
import utils
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info

api_url_main = "https://api.orbiter.finance/sdk/"
api_url_test = "https://openapi2.orbiter.finance/sdk/"


class Orbiter(Web3Bridger):
    NAME = "ORBITER"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[int | float] = None,
        min_balance: float = 0,
        slippage: float = 1,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            type_transfer=type_transfer,
            value=value,
            min_balance=min_balance,
            slippage=slippage,
        )

    async def _get_router(
        self,
        from_chain_id: int,
        to_chain_id: int,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        url = api_url_main + "routers/"
        response = await utils.aiohttp.get_json_aiohttp(url=url)
        if not response or response["status"] == "error":
            return None
        try:
            allow_router = []
            with open("response.txt", "w") as file:
                file.write(str(response))
            for router in response["result"]:
                if (
                    router["srcChain"] == str(from_chain_id)
                    and router["tgtChain"] == str(to_chain_id)
                    and router["srcToken"].lower() == from_token.address.lower()
                    and router["tgtToken"].lower() == to_token.address.lower()
                ):
                    allow_router.append(router)
            return random.choice(allow_router)
        except Exception as error:
            logger.error(error)
            return None

    async def _get_chainId_orbiter(self, to_chain_id: int | str):
        url = api_url_main + "chains/"
        response = await utils.aiohttp.get_json_aiohttp(url=url)
        if not response or response["status"] == "error":
            return None
        try:
            for chain in response["result"]:
                if chain["chainId"] == str(to_chain_id):
                    return 9000 + int(chain["internalId"])
        except Exception as error:
            return None

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
    ):
        from_chain_id: int = int(await self.acc.w3.eth.chain_id)
        to_chain_id: int = int(config.GENERAL.CHAIN_IDS.get(to_chain))
        if from_token.symbol == "ETH":
            from_token.address = config.GENERAL.ZERO_ADDRESS
        if to_token.symbol == "ETH":
            to_token.address = config.GENERAL.ZERO_ADDRESS
        router = await self._get_router(
            from_chain_id=from_chain_id,
            to_chain_id=to_chain_id,
            from_token=from_token,
            to_token=to_token,
        )
        if router is None:
            logger.error("DON'T GET ROUTER")
            return RESULT_TRANSACTION.FAIL
        commission = Token_Amount(
            amount=float(router["withholdingFee"]), decimals=from_token.decimals
        )
        logger.info(f"FEE {commission.ETHER} {from_token.symbol}")
        code_chain = await self._get_chainId_orbiter(to_chain_id=to_chain_id)
        if float(router["minAmt"]) > amount_to_send.ETHER:
            logger.error(
                f"AMOUNT ERROR MIN_AMOUNT {float(router['minAmt'])} > VALUE {amount_to_send.ETHER}"
            )
            return RESULT_TRANSACTION.FAIL
        balance = await self.acc.get_balance(token_address=from_token.address)
        if commission.ETHER + amount_to_send.ETHER > balance.ETHER:
            logger.error(
                f"AMOUNT ERROR FEE + VALUE {commission.ETHER + amount_to_send.ETHER} > BALANCE {balance.ETHER}"
            )
            return RESULT_TRANSACTION.FAIL
        amount_to_send = Token_Amount(
            amount=round(amount_to_send.WEI + commission.WEI, -4) + code_chain,
            decimals=from_token.decimals,
            wei=True,
        )
        if from_token.symbol == "ETH":
            return await self._send_transaction(
                from_token=from_token,
                to_address=router["endpoint"],
                amount_to_send=amount_to_send,
            )
        else:
            return await self.acc.transfer(
                to_address=router["endpoint"],
                amount=amount_to_send,
                token_address=from_token.address,
            )

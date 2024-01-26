import pprint
import utils
import config
import settings
from typing import Union
from loguru import logger
from utils import TYPES_OF_TRANSACTION
from utils import Token_Amount, Token_Info
from utils.enums import RESULT_TRANSACTION
from modules.web3Swapper import Web3Swapper


class RangoSwap(Web3Swapper):
    NAME = "RANGO"
    API_KEY = "c6381a79-2817-4602-83bf-6a641a409e32"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
        min_balance: float = 0,
        max_balance: float = 100,
        slippage: float = 5.0,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            type_transfer=type_transfer,
            value=value,
            min_balance=min_balance,
            max_balance=max_balance,
            slippage=slippage,
        )

    async def _get_info(self):
        headers = {"apiKey": RangoSwap.API_KEY}
        url = config.RANGO.META
        response = await utils.aiohttp.get_json_aiohttp(url=url, headers=headers)
        if not response:
            return None
        return response

    async def _get_blockchain_name(self, chain_id: hex, info: dict):
        for chain in info["blockchains"]:
            if chain["chainId"] == str(chain_id):
                return chain

    async def _prepare_token(self, token: Token_Info, info: dict, blockchain: str):
        if await Token_Info.is_native_token(self.acc.network, token=token):
            token.address = None
        for token_info in info["tokens"]:
            if blockchain.upper() == token_info["blockchain"].upper():
                if token.address is None:
                    if token.address == token_info["address"]:
                        return token_info
                else:
                    try:
                        if token.address.lower() == token_info["address"].lower():
                            return token_info
                    except:
                        continue
        return None

    async def _get_quote(
        self,
        from_token: Token_Info,
        to_token: Token_Info,
        amount_to_send: Token_Amount,
        chain_id: int,
        info: dict,
    ):
        blockchain_info = await self._get_blockchain_name(chain_id=chain_id, info=info)
        from_token_info = await self._prepare_token(
            token=from_token, info=info, blockchain=blockchain_info["name"]
        )
        to_token_info = await self._prepare_token(
            token=to_token, info=info, blockchain=blockchain_info["name"]
        )
        if from_token_info is None or to_token_info is None:
            return None

        headers = {"apiKey": RangoSwap.API_KEY}
        url = config.RANGO.ROUTING
        params = {
            "from": {
                "blockchain": blockchain_info["name"],
                "symbol": from_token_info["symbol"],
                "address": from_token_info["address"],
            },
            "to": {
                "blockchain": blockchain_info["name"],
                "symbol": to_token_info["symbol"],
                "address": to_token_info["address"],
            },
            "amount": amount_to_send.ETHER,
            "slippage": self.slippage,
            "checkPrerequisites": True,
            "selectedWallets": {blockchain_info["name"]: self.acc.address},
            "connectedWallets": [
                {
                    "blockchain": blockchain_info["name"],
                    "addresses": [self.acc.address],
                }
            ],
        }

        # if settings.USE_REF:
        #     params.update(
        #         {
        #             "affiliateRef": "gd0C76",
        #             "affiliatePercent": 1,
        #             "affiliateWallets": {
        #                 blockchain_info[
        #                     "name"
        #                 ]: "0x9f6cf6852b7aacf8377083b7a5d52862d0f312c7"
        #             },
        #         }
        #     )

        response = await utils.aiohttp.post_request(
            url=url, data=params, headers=headers
        )
        if not response:
            return None
        return response

    async def _build_tx(self, quote: dict):
        headers = {"apiKey": RangoSwap.API_KEY}
        url = config.RANGO.BUILD_TX
        # pprint.pprint(quote)
        params = {
            "requestId": quote["requestId"],
            "step": len(quote["result"]["swaps"]),
            "userSettings": {"slippage": self.slippage, "infiniteApprove": False},
            "validations": {"balance": True, "fee": True, "approve": False},
        }

        response = await utils.aiohttp.post_request(
            url=url, data=params, headers=headers
        )

        if not response or not response.get("ok"):
            return None
        return response

    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        chain_id = hex(await self.acc.w3.eth.chain_id)
        info = await self._get_info()
        if info is None:
            logger.error("FAIL GET CHAIN INFO")
            return RESULT_TRANSACTION.FAIL
        quote = await self._get_quote(
            from_token=from_token,
            to_token=to_token,
            amount_to_send=amount_to_send,
            chain_id=chain_id,
            info=info,
        )
        if quote is None:
            logger.error("FAIL GET QUOTE")
            return RESULT_TRANSACTION.FAIL
        transation_data = await self._build_tx(quote=quote)
        if transation_data is None:
            return RESULT_TRANSACTION.FAIL
        return await self._send_transaction(
            from_token=from_token,
            to_address=transation_data["transaction"]["to"],
            amount_to_send=amount_to_send,
            data=transation_data["transaction"]["data"],
        )

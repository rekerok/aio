import random
import config
import utils
from loguru import logger
from modules.account import Account
from modules.web3Bridger import Web3Bridger
from modules.web3Client import Web3Client
from settings import Client_Networks
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Rango_Bridge(Web3Bridger):
    NAME = "RANGO BRIDGE"
    API_KEY = "c6381a79-2817-4602-83bf-6a641a409e32"

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

    async def _get_to_network(
        self,
        to_chain: config.Network,
    ):
        found_variable = None
        for network_name, network_dict in Client_Networks.__dict__.items():
            if (
                isinstance(network_dict, dict)
                and network_dict.get(NETWORK_FIELDS.NAME) == to_chain
            ):
                found_variable = network_name
                break
        return getattr(Client_Networks, found_variable)

    async def _get_info(self):
        headers = {"apiKey": Rango_Bridge.API_KEY}
        url = config.RANGO.META
        response = await utils.aiohttp.get_json_aiohttp(url=url, headers=headers)
        if not response:
            return None
        return response

    async def _get_blockchain_name(self, chain_id: hex, info: dict):
        for chain in info["blockchains"]:
            if chain["chainId"] == str(chain_id):
                return chain

    async def _prepare_token(
        self, token: Token_Info, info: dict, blockchain: str, to_network=None
    ):
        network = self.acc.network if to_network is None else to_network
        if await Token_Info.is_native_token(network=network, token=token):
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
        from_chain_id,
        to_chain_id,
        info: dict,
        to_network: dict,
    ):
        from_blockchain_info = await self._get_blockchain_name(
            chain_id=from_chain_id, info=info
        )
        to_blockchain_info = await self._get_blockchain_name(
            chain_id=to_chain_id, info=info
        )
        from_token_info = await self._prepare_token(
            token=from_token, info=info, blockchain=from_blockchain_info["name"]
        )
        to_token_info = await self._prepare_token(
            token=to_token,
            info=info,
            blockchain=to_blockchain_info["name"],
            to_network=to_network,
        )
        if from_token_info is None or to_token_info is None:
            return None

        if from_token_info is None or to_token_info is None:
            return None
        headers = {"apiKey": Rango_Bridge.API_KEY}
        url = config.RANGO.ROUTING
        params = {
            "from": {
                "blockchain": from_blockchain_info["name"],
                "symbol": from_token_info["symbol"],
                "address": from_token_info["address"],
            },
            "to": {
                "blockchain": to_blockchain_info["name"],
                "symbol": to_token_info["symbol"],
                "address": to_token_info["address"],
            },
            "amount": amount_to_send.ether,
            "slippage": self.slippage,
            "checkPrerequisites": True,
            "selectedWallets": {
                from_blockchain_info["name"]: self.acc.address,
                to_blockchain_info["name"]: self.acc.address,
            },
            "connectedWallets": [
                {
                    "blockchain": from_blockchain_info["name"],
                    "addresses": [self.acc.address],
                },
                {
                    "blockchain": to_blockchain_info["name"],
                    "addresses": [self.acc.address],
                },
            ],
        }

        # # if settings.USE_REF:
        # #     params.update(
        # #         {
        # #             "affiliateRef": "gd0C76",
        # #             "affiliatePercent": 1,
        # #             "affiliateWallets": {
        # #                 blockchain_info[
        # #                     "name"
        # #                 ]: "0x9f6cf6852b7aacf8377083b7a5d52862d0f312c7"
        # #             },
        # #         }
        # #     )

        response = await utils.aiohttp.post_request(
            url=url, data=params, headers=headers
        )
        if not response:
            return None
        return response

    async def _build_tx(self, quote: dict):
        headers = {"apiKey": Rango_Bridge.API_KEY}
        url = config.RANGO.BUILD_TX
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
            logger.error(response["error"])
            return None
        return response

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
    ):
        from_chain_id = await self.acc.w3.eth.chain_id
        to_chain_id = int(config.GENERAL.CHAIN_IDS.get(to_chain))
        to_network = await self._get_to_network(to_chain=to_chain)
        info = await self._get_info()
        if info is None:
            logger.error("FAIL GET CHAIN INFO")
            return RESULT_TRANSACTION.FAIL
        from_chain_id_hex = hex(await self.acc.w3.eth.chain_id)
        to_chain_id_hex = hex(int(config.GENERAL.CHAIN_IDS.get(to_chain)))

        quote = await self._get_quote(
            from_token=from_token,
            to_token=to_token,
            amount_to_send=amount_to_send,
            from_chain_id=from_chain_id_hex,
            to_chain_id=to_chain_id_hex,
            info=info,
            to_network=to_network,
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

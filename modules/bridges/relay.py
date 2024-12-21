import pprint
from loguru import logger
import config
from typing import Union
from modules.web3Bridger import Web3Bridger
import utils
from utils.enums import (
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Relay(Web3Bridger):
    NAME = "RELAY BRIDGE"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
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

    async def get_networks(self):
        url = config.RELAY.CHAINS
        response = await utils.aiohttp.get_json_aiohttp(
            url=url,
        )
        if response is None:
            return None
        return response

    async def get_config(self, from_chaind_id: int, to_chain_id: int):
        url = config.RELAY.CONFIG
        params = {
            "originChainId": str(from_chaind_id),
            "destinationChainId": str(to_chain_id),
            "user": self.acc.address,
            "currency": "eth",
        }
        response = await utils.aiohttp.get_json_aiohttp(url=url, params=params)
        if response is None:
            return None
        return response

    async def get_quote(
        self,
        from_chaind_id: int,
        to_chain_id: int,
        amount: Token_Amount,
        recipient: str = None,
    ):
        url = config.RELAY.QUOTE
        params = {
            "user": str(self.acc.address),
            "originChainId": int(from_chaind_id),
            "destinationChainId": int(to_chain_id),
            "originCurrency": "0x0000000000000000000000000000000000000000",
            "destinationCurrency": "11111111111111111111111111111111",
            "amount": str(int(amount.wei)),
            "recipient": str(recipient),
            "tradeType": "EXACT_INPUT",
            "refferTo": "relay.link/swap",
        }
        response = await utils.aiohttp.post_request(url=url, data=params)
        if response is None:
            return None
        return response

    # async def get_quote(
    #     self,
    #     from_chaind_id: int,
    #     to_chain_id: int,
    #     amount: Token_Amount,
    #     recipient: str = None,
    # ):
    #     url = config.RELAY.BRIDGE_DATA
    #     params = {
    #         "user": str(self.acc.address),
    #         "originChainId": str(from_chaind_id),
    #         "destinationChainId": str(to_chain_id),
    #         "recipient": str(recipient),
    #         "amount": str(amount.wei),
    #         "currency": "eth",
    #         # "source": "relay.link",
    #     }
    #     response = await utils.aiohttp.post_request(url=url, data=params)
    #     if response is None:
    #         return None
    #     return response
    # async def get_bridge_data(
    #     self,
    #     from_chaind_id: int,
    #     to_chain_id: int,
    #     amount: Token_Amount,
    #     recipient: str = None,
    # ):
    #     url = config.RELAY.BRIDGE_DATA
    #     params = {
    #         "user": str(self.acc.address),
    #         "originChainId": int(from_chaind_id),
    #         "destinationChainId": int(to_chain_id),
    #         "currency": "eth",
    #         "amount": str(amount.wei),
    #         "recipient": "0xa5F565650890fBA1824Ee0F21EbBbF660a179934",
    #         "useExactInput": True,  # "source": "relay.link",
    #     }
    #     response = await utils.aiohttp.post_request(url=url, data=params)
    #     if response is None:
    #         return None
    #     return response

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
        recipient: str = None,
    ):
        from_chain_id: int = int(await self.acc.w3.eth.chain_id)
        to_chain_id: int = int(config.GENERAL.CHAIN_IDS.get(to_chain))
        # chains = await self.get_networks()
        config_transaction = await self.get_config(
            from_chaind_id=from_chain_id, to_chain_id=to_chain_id
        )
        if not (config_transaction["enabled"] and config_transaction is not None):
            logger.error(f"BRIGE NOT ENABLE OR NOT CONFIG")
            return RESULT_TRANSACTION.FAIL
        quote = await self.get_quote(
            from_chaind_id=from_chain_id,
            to_chain_id=to_chain_id,
            amount=amount_to_send,
            recipient=recipient,
        )
        # bridge_data = await self.get_bridge_data(
        #     from_chaind_id=from_chain_id,
        #     to_chain_id=to_chain_id,
        #     amount=amount_to_send,
        #     recipient=recipient,
        # )
        if quote is None:
            logger.error(f"NOT QUOTE")
            return RESULT_TRANSACTION.FAIL
        # pprint.pprint(quote)
        # if bridge_data is None:
        #     logger.error(f"NOT BRIDGE DATA")
        #     return RESULT_TRANSACTION.FAIL
        return await self.acc.send_transaction(
            to_address=quote["steps"][0]["items"][0]["data"]["to"],
            data=quote["steps"][0]["items"][0]["data"]["data"],
            value=amount_to_send,
        )

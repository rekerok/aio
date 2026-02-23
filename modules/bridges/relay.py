import pprint
from loguru import logger
import config
from typing import Union
from modules.account import Account
from modules.web3Bridger import Web3Bridger
import utils
from utils.enums import (
    NETWORK_FIELDS,
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

    async def get_quote(
        self, from_chaind_id: int, to_chain_id: int, amount: Token_Amount
    ):
        url = config.RELAY.QUOTE
        params = {
            "user": self.acc.address,
            "originChainId": from_chaind_id,
            "destinationChainId": to_chain_id,
            "originCurrency": config.GENERAL.ZERO_ADDRESS,
            "destinationCurrency": config.GENERAL.ZERO_ADDRESS,
            "amount": str(amount.wei),
            "tradeType": "EXACT_INPUT",
        }
        response = await utils.aiohttp.post_request(url=url, data=params)
        if response is None:
            return None
        return response

    async def get_bridge_data(
        self,
        from_chaind_id: int,
        to_chain_id: int,
        amount: Token_Amount,
    ):
        url = config.RELAY.BRIDGE_DATA
        params = {
            "user": self.acc.address,
            "originChainId": str(from_chaind_id),
            "destinationChainId": str(to_chain_id),
            "txs": [{"to": self.acc.address, "value": amount.wei, "data": "0x"}],
            "source": "relay.link",
        }
        response = await utils.aiohttp.post_request(url=url, data=params)
        if response is None:
            return None
        return response

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
    ):
        from_chain_id: int = int(await self.acc.w3.eth.chain_id)
        to_chain_id: int = int(config.GENERAL.CHAIN_IDS.get(to_chain.get(NETWORK_FIELDS.NAME)))
        to_chain_info = await super()._get_to_network(to_chain=to_chain)
        if to_chain_id == 1:  ## ETHEREUM
            if not await super().wait_gas(acc=Account(network=to_chain_info)):
                return RESULT_TRANSACTION.FAIL
        config_transaction = await self.get_quote(
            from_chaind_id=from_chain_id,
            to_chain_id=to_chain_id,
            amount=amount_to_send,
        )
        # pprint.pprint(config_transaction)
        if config_transaction is None:
            logger.error(f"BRIGE NOT ENABLE OR NOT CONFIG")
            return RESULT_TRANSACTION.FAIL
        # bridge_data = await self.get_bridge_data(
        #     from_chaind_id=from_chain_id, to_chain_id=to_chain_id, amount=amount_to_send
        # )
        # if bridge_data is None:
        #     logger.error(f"NOT BRIDGE DATA")
        #     return RESULT_TRANSACTION.FAIL
        return await self.acc.send_transaction(
            to_address=config_transaction["steps"][0]["items"][0]["data"]["to"],
            data=config_transaction["steps"][0]["items"][0]["data"]["data"],
            value=amount_to_send,
        )

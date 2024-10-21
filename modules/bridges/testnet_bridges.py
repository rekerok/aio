import random
from loguru import logger
import config
from typing import Union

from modules.web3Bridger import Web3Bridger
from modules.web3Client import Web3Client

from utils.enums import (
    NETWORK_FIELDS,
    PARAMETR,
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info
import eth_utils


class Testnet_Bridges(Web3Bridger):
    NAME = "TESTNET_BRIDGES_SEPOLIA"

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
            slippage=0.5,
        )

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
    ):

        if to_chain == config.Network.ARBITRUM:
            contract = self.acc.w3.eth.contract(
                address=config.TESTNET_BRIDGES.PARAMS[to_chain][PARAMETR.CONTRACT],
                abi=config.TESTNET_BRIDGES.PARAMS[to_chain][PARAMETR.ABI],
            )
            data = await Web3Client.get_data(
                contract=contract, function_of_contract="depositEth", args=()
            )
        else:
            contract = self.acc.w3.eth.contract(
                address=config.TESTNET_BRIDGES.PARAMS[to_chain][PARAMETR.CONTRACT],
                abi=config.TESTNET_BRIDGES.PARAMS[config.Network.BASE][PARAMETR.ABI],
            )
            extraData = random.choice(
                config.TESTNET_BRIDGES.PARAMS[to_chain][PARAMETR.DEXES]
            )
            data = await Web3Client.get_data(
                contract=contract,
                function_of_contract="bridgeETHTo",
                args=(self.acc.address, 20000, extraData),
            )
        if not data:
            logger.error("FAIL GET DATA")
        return await self._send_transaction(
            data=data,
            from_token=from_token,
            to_address=contract.address,
            value=amount_to_send,
        )

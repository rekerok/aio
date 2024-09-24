import random
from loguru import logger
import config
from typing import Union

from modules.web3Bridger import Web3Bridger
from modules.web3Client import Web3Client

from utils.enums import (
    NETWORK_FIELDS,
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info
import eth_utils


class Testnet_Bridge_Layerzero(Web3Bridger):
    NAME = "TESTNET_BRIDGE_LAYERZERO"

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
        self.contract = self.acc.w3.eth.contract(
            address=config.TESTNET_BRIDGE_LAYERZERO.CONTRACTS.get(
                self.acc.network.get(NETWORK_FIELDS.NAME)
            ),
            abi=config.TESTNET_BRIDGE_LAYERZERO.ABI,
        )

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
    ):
        data = await Web3Client.get_data(
            contract=self.contract,
            function_of_contract="swapAndBridge",
            args=(
                amount_to_send.WEI,
                int(amount_to_send.WEI * random.uniform(1000, 5000)),
                161,
                self.acc.address,
                self.acc.address,
                eth_utils.address.to_checksum_address(
                    "0x0000000000000000000000000000000000000000"
                ),
                b"",
            ),
        )

        value_to_send = Token_Amount(
            amount=amount_to_send.WEI + 5627000000000, wei=True
        )

        return await self._send_transaction(
            data=data,
            from_token=from_token,
            to_address=self.contract.address,
            value=value_to_send,
        )

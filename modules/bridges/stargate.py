import random
import eth_utils
from loguru import logger
import config
from typing import Union
from modules.account import Account
from modules.web3Bridger import Web3Bridger
from modules.web3Client import Web3Client
from settings import Client_Networks
from utils.enums import (
    NETWORK_FIELDS,
    PARAMETR,
    RESULT_TRANSACTION,
    TYPES_OF_TRANSACTION,
)
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Stargate(Web3Bridger):
    NAME = "STARGATE"

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

    async def _get_lz_fee(
        self,
        contract,
        dst_address: str,
        to_chain_id: int,
    ) -> Token_Amount:
        try:
            if dst_address == "":
                dst_address = "0x"
            else:
                dst_address = eth_utils.address.to_checksum_address(dst_address)
            data = (
                await contract.functions.quoteLayerZeroFee(
                    to_chain_id,  # destination chainId
                    1,  # function type (1 - swap)
                    dst_address,  # destination of tokens
                    "0x",  # payload, using abi.encode()
                    [
                        0,  # extra gas, if calling smart contract
                        0,  # amount of dust dropped in destination wallet
                        "0x",  # destination wallet for dust
                    ],
                ).call(),
            )
            return Token_Amount(amount=data[0][0], wei=True)
        except Exception as error:
            logger.error(error)
            return None

    async def _get_pool_id(self, chain: config.Network, token: Token_Info):
        try:
            token_address = token.address.lower()
            for network, addresses in config.STARGATE.POOL_IDS.items():
                for address, data in addresses.items():
                    if address.lower() == token_address:
                        return data[PARAMETR.ID]
        except Exception as error:
            return None

    # https://teletype.in/@cppmyk/stargate-bridger
    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token_address: str = "",
    ):
        to_token = await self._get_to_token(
            to_chain=to_chain, to_token_address=to_token_address
        )
        from_pool_id = await self._get_pool_id(chain=self.acc.network, token=from_token)
        to_pool_id = await self._get_pool_id(chain=to_chain, token=to_token)
        if any(v is None for v in (to_token, from_pool_id, to_pool_id)):
            logger.error("FAIL GET INFO")
            return RESULT_TRANSACTION.FAIL
        to_chain_id = config.GENERAL.LAYERZERO_CHAINS_ID.get(to_chain)
        contract = self.acc.w3.eth.contract(
            address=config.STARGATE.ROUTER_CONTRACTS.get(
                self.acc.network.get(NETWORK_FIELDS.NAME)
            ),
            abi=config.STARGATE.ROUTER_ABI,
        )

        fee = await self._get_lz_fee(
            contract=contract,
            dst_address=to_token.address,
            to_chain_id=to_chain_id,
        )
        if fee is None:
            logger.error("DON'T GET FEE LAYERZERO")
            return RESULT_TRANSACTION.FAIL
        logger.info(
            f"FEE {fee.ETHER} {self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN)}"
        )
        min_received_amount = Token_Amount(
            amount=amount_to_send.ETHER * (1 - self.slippage / 100),
            decimals=amount_to_send.DECIMAL,
        )
        if from_token.symbol == "ETH":
            contract = self.acc.w3.eth.contract(
                address=config.STARGATE.ROUTER_CONTRACTS_ETH.get(
                    self.acc.network.get(NETWORK_FIELDS.NAME)
                ),
                abi=config.STARGATE.ROUTER_ABI_ETH,
            )
            args = (
                to_chain_id,
                self.acc.address,
                self.acc.address,
                amount_to_send.WEI,
                min_received_amount.WEI,
            )
            data = await Web3Client.get_data(
                contract=contract, function_of_contract="swapETH", args=args
            )
            if data is None:
                logger.error("DON'T GET DATA FOR BRIDGE")
                return RESULT_TRANSACTION.FAIL
            return await self._send_transaction(
                data=data,
                from_token=from_token,
                to_address=contract.address,
                amount_to_send=Token_Amount(
                    amount=amount_to_send.WEI + fee.WEI * 1.05,
                    decimals=amount_to_send.DECIMAL,
                    wei=True,
                ),
            )
        else:
            args = (
                to_chain_id,  # destination chainId
                from_pool_id,  # source poolId
                to_pool_id,  # destination poolId
                self.acc.address,  # refund address. extra gas (if any) is returned to this address
                amount_to_send.WEI,  # quantity to swap
                min_received_amount.WEI,  # the min qty you would accept on the destination
                [
                    0,  # extra gas, if calling smart contract
                    0,  # amount of dust dropped in destination wallet
                    "0x",  # destination wallet for dust
                ],
                self.acc.address,  # the address to send the tokens to on the destination
                "0x",  # "fee" is the native gas to pay for the cross chain message fee
            )

            data = await Web3Client.get_data(
                contract=contract, function_of_contract="swap", args=args
            )
            if data is None:
                logger.error("DON'T GET DATA FOR BRIDGE")
                return RESULT_TRANSACTION.FAIL
            return await self._send_transaction(
                data=data,
                from_token=from_token,
                to_address=contract.address,
                amount_to_send=amount_to_send,
                value=fee,
            )

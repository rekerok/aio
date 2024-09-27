import eth_utils
from loguru import logger
import config
from typing import Union
from modules.account import Account
from modules.web3Bridger import Web3Bridger
from modules.web3Client import Web3Client
from settings import Client_Networks
import utils
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION, TYPES_OF_TRANSACTION
from utils.token_amount import Token_Amount
from utils.token_info import Token_Info


class Hyperlane(Web3Bridger):
    NAME = "HYPERLANE"

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
        self.contract = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.HYPERLANE.CONTRACTS_BRIDGE_ETH[
                    self.acc.network.get(NETWORK_FIELDS.NAME)
                ]
            ),
            abi=config.HYPERLANE.ABI_TOKEN_BRIDGE,
        )

    @staticmethod
    async def get_fee(contract, to_chain_id: int, amount_to_send: Token_Amount):
        try:
            return Token_Amount(
                amount=await contract.functions.quoteBridge(
                    to_chain_id, amount_to_send.wei
                ).call(),
                wei=True,
            )
        except Exception as error:
            # logger.error(error)
            return None

    async def _perform_bridge(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_chain: config.Network,
        to_token: Token_Info = None,
    ):
        if from_token.symbol != "ETH" and to_token.symbol != "ETH":
            logger.error(f"NOT ETH TOKENS")
            return RESULT_TRANSACTION.FAIL
        to_chain_id = config.GENERAL.CHAIN_IDS.get(to_chain)
        fee = await Hyperlane.get_fee(
            contract=self.contract,
            to_chain_id=to_chain_id,
            amount_to_send=amount_to_send,
        )
        if fee is None:
            logger.error("DON'T GET FEE")
            return RESULT_TRANSACTION.FAIL
        logger.info(f"FEE {fee.ether} ETH")
        data = await Web3Client.get_data(
            contract=self.contract,
            function_of_contract="bridgeETH",
            args=(to_chain_id, amount_to_send.wei),
        )
        if data is None:
            logger.error("DON'T GET DATA")
            return RESULT_TRANSACTION.FAIL

        return await self._send_transaction(
            from_token=from_token,
            to_address=self.contract.address,
            amount_to_send=Token_Amount(amount=fee.ether + amount_to_send.ether),
            data=data,
        )

    @staticmethod
    async def check_fees():
        wallets = await utils.files.read_file_lines(
            path="files/wallets.txt",
        )
        wallet = wallets[0]
        networks = [
            Client_Networks.arbitrum,
            Client_Networks.base,
            Client_Networks.optimism,
            Client_Networks.scroll,
            # Client_Networks.bsc,
            # Client_Networks.polygon,
        ]
        for network in networks:
            acc = Account(private_key=wallet, network=network)
            for check_network in networks:
                contract = acc.w3.eth.contract(
                    address=eth_utils.address.to_checksum_address(
                        config.HYPERLANE.CONTRACTS_BRIDGE_ETH[
                            acc.network.get(NETWORK_FIELDS.NAME)
                        ]
                    ),
                    abi=config.HYPERLANE.ABI_TOKEN_BRIDGE,
                )
                fee = await Hyperlane.get_fee(
                    contract=contract,
                    to_chain_id=config.GENERAL.CHAIN_IDS.get(
                        check_network[NETWORK_FIELDS.NAME]
                    ),
                    amount_to_send=Token_Amount(amount=0.00510943),
                )
                if fee is None:
                    continue
                logger.info(
                    f"{network[NETWORK_FIELDS.NAME]} -> {check_network[NETWORK_FIELDS.NAME]} = {fee.ether:.5f} ETH"
                )
            print()

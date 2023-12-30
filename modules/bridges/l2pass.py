from modules.web3Swapper import Web3Swapper
import utils
import config
import random
import eth_utils
from loguru import logger
from utils import Token_Amount
from config import L2PASS, MERKLY, GENERAL
from modules.account import Account
from eth_abi.packed import encode_packed
from utils.enums import NETWORK_FIELDS, PARAMETR, RESULT_TRANSACTION


class L2Pass:
    NAME = "L2PASS"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
    ) -> None:
        if private_key and network:
            self.acc = Account(private_key=private_key, network=network)
        if network:
            self.contract_l2pass = self.acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(
                    L2PASS.CONTRACT.value.get(self.acc.network.get(NETWORK_FIELDS.NAME))
                ),
                abi=L2PASS.ABI.value,
            )

    async def refuel(self, amount_to_get: tuple, to_chain):
        amount_to_get: Token_Amount = Token_Amount(
            amount=random.uniform(*amount_to_get)
        )
        to_chain_id = GENERAL.LAYERZERO_CHAINS_ID.value.get(to_chain)
        logger.warning(self.NAME)
        logger.info(f"WALLET {self.acc.address}")
        logger.info(
            f"{self.acc.network.get(NETWORK_FIELDS.NAME)} -> {to_chain}"
        )
        try:
            fee = await self.contract_l2pass.functions.estimateGasRefuelFee(
                to_chain_id, amount_to_get.WEI, self.acc.address, False
            ).call()
            if fee is None:
                logger.error("FAIL GET GAS")
                return RESULT_TRANSACTION.FAIL
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        try:
            data = self.contract_l2pass.encodeABI(
                "gasRefuel",
                args=(
                    to_chain_id,
                    config.GENERAL.ZERO_ADDRESS.value,
                    amount_to_get.WEI,
                    self.acc.address,
                ),
            )
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        value = Token_Amount(amount=fee[0], wei=True)
        logger.info(
            f"SEND {value.ETHER} {self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN)}"
        )
        return await self.acc.send_transaction(
            to_address=self.contract_l2pass.address,
            data=data,
            value=value,
        )

    @staticmethod
    async def get_fees(from_chains: list[dict]):
        to_chains = GENERAL.LAYERZERO_CHAINS_ID.value
        fees = {}
        logger.debug("COLLEC INFORMATION")
        for from_chain in from_chains:
            acc = Account(network=from_chain)
            contract_l2pass = acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(
                    L2PASS.CONTRACT.value.get(acc.network.get(NETWORK_FIELDS.NAME))
                ),
                abi=config.L2PASS.ABI.value,
            )
            fees_for_network = list()
            for to_chain_name, to_chain_id in to_chains.items():
                if from_chain.get(NETWORK_FIELDS.NAME) == to_chain_name:
                    continue
                try:
                    fee = await contract_l2pass.functions.estimateGasRefuelFee(
                        to_chain_id, 0, config.GENERAL.ZERO_ADDRESS.value, False
                    ).call()
                    fee = Token_Amount(
                        amount=fee[0],
                        decimals=18,
                        wei=True,
                    )
                    fees_for_network.append({"name": to_chain_name, "fee": fee})
                except Exception as error:
                    continue
            fees.update({from_chain.get(NETWORK_FIELDS.NAME): fees_for_network})
        fees = {
            key: sorted(value, key=lambda x: x["fee"].ETHER)
            for key, value in fees.items()
        }
        for network, list_fees in fees.items():
            for fee in list_fees:
                logger.info(f"{network} -> {fee['name']} {fee['fee'].ETHER:.10f}")

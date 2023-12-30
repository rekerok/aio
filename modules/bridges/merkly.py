import utils
import config
import random
import eth_utils
from loguru import logger
from utils import Token_Amount
from config import MERKLY, GENERAL
from modules.account import Account
from eth_abi.packed import encode_packed
from utils.enums import NETWORK_FIELDS, PARAMETR, RESULT_TRANSACTION


class Merkly:
    NAME = "MERKLY"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
    ) -> None:
        if private_key and network:
            self.acc = Account(private_key=private_key, network=network)
        if network:
            self.contract = self.acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(
                    MERKLY.CONTRACT.value.get(self.acc.network.get(NETWORK_FIELDS.NAME))
                ),
                abi=MERKLY.ABI.value,
            )

    async def refuel(self, amount_to_get: tuple, to_chain):
        amount_to_get: Token_Amount = Token_Amount(
            amount=random.uniform(*amount_to_get)
        )
        logger.warning(self.NAME)
        logger.info(f"WALLET {self.acc.address}")
        to_chain_id = GENERAL.LAYERZERO_CHAINS_ID.value.get(to_chain)
        logger.info(f"{self.acc.network.get(NETWORK_FIELDS.NAME)} -> {to_chain}")
        adapter_params = await Merkly._get_adapter_params(
            contract=self.contract,
            dst_chain_id=to_chain_id,
            amount_to_get=amount_to_get,
            to_address=self.acc.address,
        )
        try:
            data = self.contract.encodeABI(
                "bridgeGas",
                args=(to_chain_id, self.acc.address, adapter_params),
            )
            estimate_send_fee = await self.contract.functions.estimateSendFee(
                to_chain_id, "0x", adapter_params
            ).call()
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        value = Token_Amount(amount=estimate_send_fee[0] * 1.01, wei=True)
        logger.info(
            f"SEND {value.ETHER} {self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN)}"
        )
        return await self.acc.send_transaction(
            to_address=self.contract.address,
            data=data,
            value=value,
        )

    @staticmethod
    async def _get_adapter_params(
        contract, dst_chain_id: int, amount_to_get: Token_Amount, to_address=None
    ):
        try:
            gas_limit = await contract.functions.minDstGasLookup(dst_chain_id, 0).call()
            address = eth_utils.address.to_checksum_address(
                to_address if to_address else contract.address
            )
            # https://layerzero.gitbook.io/docs/evm-guides/advanced/relayer-adapter-parameters#airdrop
            return encode_packed(
                ["uint16", "uint", "uint", "address"],
                [
                    2,
                    int(gas_limit * 1.5),
                    amount_to_get.WEI,
                    address,
                ],
            )
        except Exception as e:
            return None

    @staticmethod
    async def get_fees(from_chains: list[dict]):
        to_chains = GENERAL.LAYERZERO_CHAINS_ID.value
        fees_list = []
        logger.debug("COLLEC INFORMATION")
        for from_chain in from_chains:
            acc = Account(network=from_chain)
            contract_merkly = acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(
                    MERKLY.CONTRACT.value.get(acc.network.get(NETWORK_FIELDS.NAME))
                ),
                abi=config.MERKLY.ABI.value,
            )

            for to_chain_name, to_chain_id in to_chains.items():
                if from_chain.get(PARAMETR.NAME) != to_chain_name:
                    dst_chain_id = to_chain_id
                    adapter_params = await Merkly._get_adapter_params(
                        dst_chain_id=dst_chain_id,
                        contract=contract_merkly,
                        amount_to_get=Token_Amount(amount=0),
                    )
                    if not adapter_params:
                        continue
                    try:
                        estimate_send_fee = (
                            await contract_merkly.functions.estimateSendFee(
                                to_chain_id, "0x", adapter_params
                            ).call()
                        )
                        price = Token_Amount(
                            amount=estimate_send_fee[0], decimals=18, wei=True
                        )
                        fees_list.append(
                            {
                                "from_chain": from_chain.get(NETWORK_FIELDS.NAME),
                                "to_chain": to_chain_name,
                                "to_chain_id": to_chain_id,
                                "price": price,
                            }
                        )
                    except:
                        price = Token_Amount(amount=0)

        # Сортировка по стоимости (от самого дешевого к самому дорогому)
        fees_list = sorted(fees_list, key=lambda x: x["price"].ETHER)

        # Вывод результатов
        for fee_info in fees_list:
            logger.info(
                f"{fee_info['from_chain']} -> {fee_info['to_chain']} ({fee_info['to_chain_id']}) {fee_info['price'].ETHER:.10f}"
            )

import utils
import config
import random
import settings
import eth_utils
from loguru import logger
from utils import Token_Amount
from settings import GAS_MULTIPLAY
from settings import Client_Networks
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.middleware import async_geth_poa_middleware
from utils.annotations import retry_async
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION


class Account:
    def __init__(
        self,
        private_key: str = None,
        address=None,
        network: dict = None,
        timeout: int = 60,
    ) -> None:
        self.timeout = timeout
        self.request_kwargs = {
            "timeout": timeout,
        }
        self.request_kwargs["proxy"] = (
            utils.files.get_random_proxy() if settings.USE_PROXY else None
        )
        self.network = network
        self.w3 = AsyncWeb3(
            AsyncHTTPProvider(
                endpoint_uri=random.choice(self.network.get(NETWORK_FIELDS.RPCS)),
                request_kwargs=self.request_kwargs,
            )
        )
        self.w3.middleware_onion.inject(async_geth_poa_middleware, layer=0)
        if private_key:
            self.private_key = private_key
            self.acc = self.w3.eth.account.from_key(self.private_key)
            self.address = self.acc.address
        elif address:
            self.address = eth_utils.address.to_checksum_address(address)

    async def get_balance(self, token_address: str = None) -> Token_Amount:
        try:
            if not token_address or token_address == "":
                value = await self.w3.eth.get_balance(
                    eth_utils.address.to_checksum_address(self.address)
                )
                return Token_Amount(amount=value, wei=True)
            else:
                contract_token = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(token_address),
                    abi=config.GENERAL.ERC20_ABI,
                )
                value = await contract_token.functions.balanceOf(self.address).call()
                return Token_Amount(
                    amount=value,
                    decimals=await contract_token.functions.decimals().call(),
                    wei=True,
                )
        except Exception as error:
            # logger.error(error)
            return None

    async def change_connection(self, change_rpc=True):
        self.request_kwargs = {
            "timeout": self.timeout,
        }
        self.request_kwargs["proxy"] = (
            utils.files.get_random_proxy() if settings.USE_PROXY else None
        )
        self.network = self.network
        self.w3 = AsyncWeb3(
            AsyncHTTPProvider(
                endpoint_uri=random.choice(self.network.get(NETWORK_FIELDS.RPCS)),
                request_kwargs=self.request_kwargs,
            )
        )
        self.w3.middleware_onion.inject(async_geth_poa_middleware, layer=0)
        logger.warning("CHANGE_RPC")

    async def transfer(
        self, to_address: str, amount: Token_Amount, token_address: str = None
    ):
        if token_address is None or token_address == "":
            return await self.send_transaction(to_address=to_address, value=amount)
        else:
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address),
                abi=config.GENERAL.ERC20_ABI,
            )
            # await self.approve(
            #     token_address=token_address, spender=to_address, amount=amount
            # )
            data = contract.encodeABI(
                "transfer", args=(self.w3.to_checksum_address(to_address), amount.wei)
            )
            return await self.send_transaction(
                data=data, to_address=token_address, value=0
            )

    async def deploy_contract(self, bytecode: str):
        return await self.send_transaction(data=bytecode)

    async def _get_allowance(
        self, token_address: str, owner: str, spender: str
    ) -> Token_Amount:
        try:
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address),
                abi=config.GENERAL.ERC20_ABI,
            )
            amount_allowance = await contract.functions.allowance(
                self.w3.to_checksum_address(owner), self.w3.to_checksum_address(spender)
            ).call()
            amount_allowance = Token_Amount(
                amount=amount_allowance,
                decimals=await contract.functions.decimals().call(),
                wei=True,
            )
            return amount_allowance
        except Exception as error:
            logger.error(f"{error}")
            return Token_Amount(amount=0)

    async def approve(
        self,
        token_address: str,
        spender: str,
        amount: Token_Amount,
        check_approve: bool = True,
    ):
        contract = self.w3.eth.contract(
            address=self.w3.to_checksum_address(token_address),
            abi=config.GENERAL.ERC20_ABI,
        )
        if check_approve:
            logger.info(f"Check approve")
            allowanced: Token_Amount = await self._get_allowance(
                token_address=token_address, owner=self.address, spender=spender
            )

            if allowanced.ether > amount.ether:
                logger.info(f"Approve not need")
                return
            else:
                logger.info(f"Apptove need")

                value_approove = Token_Amount(
                    amount=amount.wei + amount.wei * random.uniform(0.01, 0.05),
                    decimals=amount.decimal,
                    wei=True,
                )
                logger.info(f"Make approve for {value_approove.ether}")
                result_approve = await self.send_transaction(
                    to_address=token_address,
                    data=contract.encodeABI(
                        "approve",
                        args=(
                            self.w3.to_checksum_address(spender),
                            int(value_approove.wei),
                        ),
                    ),
                )
                if result_approve == RESULT_TRANSACTION.SUCCESS:
                    await utils.time.sleep_view(settings.SLEEP_AFTER_APPROOVE)
                else:
                    return RESULT_TRANSACTION.FAIL
        else:
            return await self.send_transaction(
                to_address=token_address,
                data=contract.encodeABI(
                    "approve",
                    args=(
                        self.w3.to_checksum_address(spender),
                        int(amount.wei),
                    ),
                ),
            )

    async def _get_eip1559_tx(self, tx_params: dict, increase_gas: float = 1.0):
        last_block = await self.w3.eth.get_block("latest")
        base_fee = int(last_block["baseFeePerGas"] * increase_gas)
        max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
        tx_params["maxFeePerGas"] = int(base_fee + max_priority_fee_per_gas)
        tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
        return tx_params

    @retry_async(attempts=3)
    async def prepare_transaction(
        self,
        to_address: str = None,
        data: str = None,
        value: Token_Amount = None,
    ):
        try:
            logger.info("Begin transaction")
            tx_params = {
                "from": self.address,
                "chainId": await self.w3.eth.chain_id,
                "nonce": await self.w3.eth.get_transaction_count(self.address),
            }

            if to_address:
                tx_params["to"] = self.w3.to_checksum_address(to_address)
            if data:
                tx_params["data"] = data

            if value is None or value == 0:
                tx_params["value"] = 0
            else:
                tx_params["value"] = value.wei
            increase_gas = random.uniform(GAS_MULTIPLAY[0], GAS_MULTIPLAY[1])
            logger.info(f"GAS MULTIPLAY IS {increase_gas}")
            if self.network[NETWORK_FIELDS.EIP1559]:
                tx_params = await self._get_eip1559_tx(
                    tx_params=tx_params, increase_gas=increase_gas
                )

            else:
                tx_params["gasPrice"] = int(await self.w3.eth.gas_price * increase_gas)

            tx_params["gas"] = int(await self.w3.eth.estimate_gas(tx_params))

            return tx_params
        except Exception as error:
            logger.error(error)
            return None

    async def sign_transaction(self, tx: dict):
        try:
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            raw_tx_hash = await self.w3.eth.send_raw_transaction(
                signed_tx.rawTransaction
            )
            tx_hash = self.w3.to_hex(raw_tx_hash)
            return tx_hash
        except Exception as error:
            logger.error(error)
            return None

    async def verifi_tx(self, tx_hash):
        try:
            data = await self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=400)
            if "status" in data and data["status"] == 1:
                logger.success(
                    f"LINK {self.network[NETWORK_FIELDS.EXPLORER]}tx/{tx_hash}"
                )
                return RESULT_TRANSACTION.SUCCESS
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL
        logger.error(f"LINK {self.network[NETWORK_FIELDS.EXPLORER]}tx/{tx_hash}")
        return RESULT_TRANSACTION.FAIL

    @retry_async(attempts=3)
    async def send_transaction(
        self,
        to_address: str = None,
        data: str = None,
        value: Token_Amount = None,
    ):
        try:
            logger.info("Begin transactction")
            tx_params = {
                "from": self.address,
                "chainId": await self.w3.eth.chain_id,
                "nonce": await self.w3.eth.get_transaction_count(self.address),
            }

            if to_address:
                tx_params["to"] = self.w3.to_checksum_address(to_address)
            if data:
                tx_params["data"] = data

            if value is None or value == 0:
                tx_params["value"] = 0
            else:
                tx_params["value"] = value.wei
            increase_gas = random.uniform(GAS_MULTIPLAY[0], GAS_MULTIPLAY[1])
            logger.info(f"GAS MULTIPLAY IS {increase_gas}")
            if self.network[NETWORK_FIELDS.EIP1559]:
                tx_params = await self._get_eip1559_tx(
                    tx_params=tx_params, increase_gas=increase_gas
                )

            else:
                tx_params["gasPrice"] = int(await self.w3.eth.gas_price * increase_gas)

            tx_params["gas"] = int(await self.w3.eth.estimate_gas(tx_params))

            tx_hash = await self.sign_transaction(tx=tx_params)
            verify = await self.verifi_tx(tx_hash=tx_hash)
            if verify:
                return RESULT_TRANSACTION.SUCCESS
            else:
                return RESULT_TRANSACTION.FAIL
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL

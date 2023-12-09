from networks import Networks
import utils
import config
import random
from typing import Union
from web3 import AsyncWeb3, AsyncHTTPProvider
from helpers import Token_Amount
from loguru import logger
from web3.middleware import async_geth_poa_middleware
from helpers.decorators import check_gas
from settings import GAS_MULTIPLAY


class Account:
    def __init__(
        self,
        private_key: str = None,
        address=None,
        network: dict = None,
        proxies: list[str] = None,
        timeout=60,
    ) -> None:
        self.timeout = timeout
        self.request_kwargs = {
            "timeout": timeout,
        }
        self.proxies = proxies if proxies else None
        self.request_kwargs["proxy"] = (
            random.choice(self.proxies) if self.proxies else None
        )
        self.network = network
        self.rpcs: list[str] = network.get("rpc")
        self.w3 = AsyncWeb3(
            AsyncHTTPProvider(
                endpoint_uri=random.choice(self.rpcs),
                request_kwargs=self.request_kwargs,
            )
        )
        self.w3.middleware_onion.inject(async_geth_poa_middleware, layer=0)
        if private_key:
            self.private_key = private_key
            self.acc = self.w3.eth.account.from_key(self.private_key)
            self.address = self.acc.address
        else:
            self.address = address

    async def get_balance(self, token_address: str = None) -> Token_Amount:
        try:
            if not token_address or token_address == "":
                value = await self.w3.eth.get_balance(self.address)
                return Token_Amount(amount=value, wei=True)
            else:
                contract_token = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(token_address),
                    abi=config.ERC20_ABI,
                )
                value = await contract_token.functions.balanceOf(self.address).call()
                return Token_Amount(
                    amount=value,
                    decimals=await contract_token.functions.decimals().call(),
                    wei=True,
                )
        except:
            return None

    async def change_connection(self, change_proxy=True, change_rpc=True):
        self.request_kwargs = {
            "timeout": self.timeout,
        }
        if change_proxy and self.proxies:
            self.request_kwargs["proxy"] = random.choice(self.proxies)
            self.w3 = AsyncWeb3(
                AsyncHTTPProvider(
                    endpoint_uri=random.choice(self.rpcs),
                    request_kwargs=self.request_kwargs,
                )
            )

    async def get_eip1559_tx(self, tx_params: dict, increase_gas: float = 1.0):
        last_block = await self.w3.eth.get_block("latest")
        base_fee = int(last_block["baseFeePerGas"] * increase_gas)
        max_priority_fee_per_gas = await self.w3.eth.max_priority_fee
        tx_params["maxFeePerGas"] = int(base_fee + max_priority_fee_per_gas)
        tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
        return tx_params

    async def verifi_tx(self, tx_hash):
        try:
            data = await self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=400)
            if "status" in data and data["status"] == 1:
                return True
            else:
                return False
        except Exception as error:
            print(error)
            return False

    async def get_allowance(
        self, token_address: str, owner: str, spender: str
    ) -> Token_Amount:
        try:
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address), abi=config.ERC20_ABI
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

    async def approve(self, token_address: str, spender: str, amount: Token_Amount):
        logger.info(f"Check approve")
        allowanced: Token_Amount = await self.get_allowance(
            token_address=token_address, owner=self.address, spender=spender
        )

        if allowanced.ETHER > amount.ETHER:
            logger.info(f"Approve not need")
            return
        else:
            logger.info(f"Apptove need")
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address), abi=config.ERC20_ABI
            )
            logger.info(
                f"Make approve for {amount.ETHER + amount.ETHER * random.uniform(0.01,0.05)}"
            )
            await self.send_transaction(
                to_address=token_address,
                data=contract.encodeABI(
                    "approve",
                    args=(
                        self.w3.to_checksum_address(spender),
                        int(amount.WEI + amount.WEI * 0.1),
                    ),
                ),
            )
            await utils.time.sleep_view((30, 60))

    async def transfer(
        self, to_address: str, amount: Token_Amount, token_address: str = None
    ):
        logger.info("START TRANSFER MODULE")
        logger.info(f"WILL SEND {amount} to {to_address}")
        if token_address is None or token_address == "":
            await self.send_transaction(to_address=to_address, value=amount.WEI)
        else:
            contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address),
                abi=config.ERC20_ABI,
            )
            await self.approve(
                token_address=token_address, spender=to_address, amount=amount.WEI
            )
            data = contract.encodeABI(
                "transfer", args=(self.w3.to_checksum_address(to_address), amount.WEI)
            )
            await self.send_transaction(data=data, to_address=token_address, value=0)

    # @check_gas
    async def deploy_contract(self, bytecode: str):
        await self.send_transaction(data=bytecode)

    async def send_transaction(
        self,
        to_address: str = None,
        data: str = None,
        value: Token_Amount = None,
    ):
        allow_transaction = True
        if self.network.get("check_gas"):
            allow_transaction = await utils.time.wait_gas(
                AsyncWeb3(
                    AsyncHTTPProvider(
                        endpoint_uri=random.choice(Networks.ethereum.get("rpc")),
                        request_kwargs=self.request_kwargs,
                    )
                )
            )

        if allow_transaction:
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
                    tx_params["value"] = value.WEI

                if self.network["eip1559"]:
                    tx_params = await self.get_eip1559_tx(tx_params=tx_params)
                else:
                    tx_params["gasPrice"] = await self.w3.eth.gas_price

                tx_params["gas"] = int(
                    await self.w3.eth.estimate_gas(tx_params) * GAS_MULTIPLAY
                )

                tx_hash = await self.sign_transaction(tx=tx_params)
                verify = await self.verifi_tx(tx_hash=tx_hash)
                if verify:
                    logger.success(f"LINK {self.network['scan']}tx/{tx_hash}")
                else:
                    logger.error(f"LINK {self.network['scan']['scan']}tx/{tx_hash}")
            except Exception as error:
                logger.error(error)

    async def sign_transaction(self, tx: dict):
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        raw_tx_hash = await self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = self.w3.to_hex(raw_tx_hash)
        return tx_hash

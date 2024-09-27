import config
import random
import settings
import eth_utils
from loguru import logger
from web3 import AsyncHTTPProvider, AsyncWeb3
from modules.account import Account
import utils
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION
from utils.token_info import Token_Info
from utils.token_amount import Token_Amount


class Web3Client:
    NAME = ""

    def __init__(
        self,
        private_key: str,
        network: dict,
    ) -> None:
        self.acc = Account(private_key=private_key, network=network)

    async def _send_transaction(
        self,
        from_token: Token_Info,
        to_address: str,
        amount_to_send: Token_Amount = None,
        data: str = None,
        value=None,
    ):
        if not await Token_Info.is_native_token(
            network=self.acc.network, token=from_token
        ):
            await self.acc.approve(
                token_address=from_token.address,
                spender=to_address,
                amount=amount_to_send,
            )
        else:
            if not value:
                value = amount_to_send
        tx_params = await self.acc.prepare_transaction(
            to_address=eth_utils.address.to_checksum_address(to_address),
            data=data,
            value=value,
        )
        if tx_params is None:
            return RESULT_TRANSACTION.FAIL
        tx_hash = await self.acc.sign_transaction(tx_params)
        return await self.acc.verifi_tx(tx_hash=tx_hash)
        # return await self.acc.send_transaction(
        #     to_address=eth_utils.address.to_checksum_address(to_address),
        #     data=data,
        #     value=value,
        # )

    async def choice_type_transaction(): ...

    @staticmethod
    async def check_min_balance(
        acc: Account,
        min_balance: float,
        token: config.Token = config.Token(address=""),
    ):
        while True:
            balance = await acc.get_balance(token_address=token.address)
            token_info = await Token_Info.get_info_token(
                acc=acc, token_address=token.address
            )
            if balance is not None and token_info is not None:
                break
            # logger.error("kekkkkkk")
            await acc.change_connection()
        if balance.ether > min_balance:
            return True, balance, token_info
        else:
            return False, balance, token_info

    @staticmethod
    async def wait_gas(acc):
        if acc.network.get(NETWORK_FIELDS.CHECK_GAS):
            network_name = acc.network.get(NETWORK_FIELDS.NAME)
            valid_networks = [
                config.Network.SCROLL,
                config.Network.BASE,
            ]

            if network_name in valid_networks:
                endpoint_uri = random.choice(acc.network.get(NETWORK_FIELDS.RPCS))
                limit = acc.network.get(NETWORK_FIELDS.LIMIT_GAS)
            else:
                endpoint_uri = random.choice(
                    settings.Client_Networks.ethereum.get(NETWORK_FIELDS.RPCS)
                )
                limit = settings.LIMIT_GWEI

            w3 = AsyncWeb3(AsyncHTTPProvider(endpoint_uri=endpoint_uri))
            return await utils.time.wait_gas(w3=w3, LIMIT_GWEI=limit)
        else:
            return True

    @staticmethod
    async def get_data(contract, function_of_contract: str, args: tuple = None):
        try:
            return contract.encodeABI(
                function_of_contract,
                args=args,
            )
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    async def get_value_and_allowance(amount: Token_Amount, from_native_token: bool):
        if from_native_token:
            value = amount
            value_approve = None
        else:
            value = None
            value_approve = amount
        return value, value_approve

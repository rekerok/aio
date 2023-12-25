import time
import config
import eth_abi
from loguru import logger
from typing import Union
from helpers import contracts
from helpers import Web3Swapper, Token_Amount, Token_Info
from utils import TYPE_OF_TRANSACTION


class SyncSwap(Web3Swapper):
    NAME = "SYNCSWAP"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPE_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
        min_balance: float = 0,
        slippage: float = 5.0,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            type_transfer=type_transfer,
            value=value,
            min_balance=min_balance,
            slippage=slippage,
        )

        self.contract_pool_factory = self.acc.w3.eth.contract(
            address=contracts.SYNCSWAP.get(self.acc.network.get("name")).get(
                "pool_factory"
            ),
            abi=config.SYNCSWAP_ABI.get("pool_factory"),
        )

        self.contract_router = self.acc.w3.eth.contract(
            address=contracts.SYNCSWAP.get(self.acc.network.get("name")).get("router"),
            abi=config.SYNCSWAP_ABI.get("router"),
        )

    async def _get_pool_address(self, from_token: Token_Info, to_token: Token_Info):
        try:
            pool_address = await self.contract_pool_factory.functions.getPool(
                from_token.address, to_token.address
            ).call()
            return pool_address
        except Exception as error:
            logger.error(error)
            return None

    async def _get_reserve(self, contract):
        try:
            reserve = await contract.functions.getReserves().call()
            return reserve
        except Exception as error:
            logger.error(error)
            return None

    async def _get_amount_out(
        self, contract, token_in: Token_Info, amount_in: Token_Amount, sender: str
    ):
        try:
            reserve = await contract.functions.getAmountOut(
                token_in.address, amount_in.WEI, sender
            ).call()
            return reserve
        except Exception as error:
            logger.error(error)
            return None

    # https://syncswap.gitbook.io/api-documentation/guides/request-swap-with-router/swap-eth-for-dai
    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        from_token, to_token = await Token_Info.to_wrapped_token(
            from_token=from_token,
            to_token=to_token,
            name_network=self.acc.network.get("name"),
        )
        pool_address = await self._get_pool_address(
            from_token=from_token, to_token=to_token
        )
        if pool_address == contracts.ZERO_ADDRESS or None:
            logger.error(f"Pool not exists")
            return
        contract_pool = self.acc.w3.eth.contract(
            address=pool_address, abi=config.SYNCSWAP_ABI.get("pool")
        )
        amount_in = await self._get_amount_out(
            contract=contract_pool,
            token_in=from_token,
            amount_in=amount_to_send,
            sender=self.acc.address,
        )
        amount_in = Token_Amount(
            amount=int(amount_in - amount_in * self.slippage / 100),
            decimals=to_token.decimals,
            wei=True,
        )

        swapData = eth_abi.encode(
            ["address", "address", "uint8"], [from_token.address, self.acc.address, 1]
        )

        steps = [
            {
                "pool": pool_address,
                "data": swapData,
                "callback": contracts.ZERO_ADDRESS,
                "callbackData": "0x",
            }
        ]

        paths = [
            {
                "steps": steps,
                "tokenIn": contracts.ZERO_ADDRESS
                if from_token.symbol == "ETH"
                else from_token.address,
                "amountIn": amount_to_send.WEI,
            }
        ]
        deadline = int(time.time()) + 1000000
        data = await self._get_data(
            contract=self.contract_router,
            function_of_contract="swap",
            args=(
                paths,  # path
                amount_in.WEI,  # amountOutMin
                deadline,  # deadline 30 min
            ),
        )
        value_approve = (
            None
            if from_token.address
            == self.acc.w3.to_checksum_address(
                contracts.WETH_CONTRACTS.get(self.acc.network.get("name"))
            )
            else amount_to_send
        )
        value = (
            None
            if from_token.address
            != self.acc.w3.to_checksum_address(
                contracts.WETH_CONTRACTS.get(self.acc.network.get("name"))
            )
            else amount_to_send
        )
        return await self._send_swap_transaction(
            data=data,
            from_token=from_token,
            to_address=self.contract_router.address,
            value_approove=value_approve,
            value=value,
        )

import time
import config
import eth_utils
from typing import Union
from loguru import logger
from hexbytes import HexBytes
from utils import TYPES_OF_TRANSACTION
from modules.web3Client import Web3Client
from utils import Token_Amount, Token_Info
from modules.web3Swapper import Web3Swapper
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION


class IzumiSwap(Web3Swapper):
    NAME = "IZUMI"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPES_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
        min_balance: float = 0,
        max_balance: float = 100,
        slippage: float = 1.0,
    ) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
            type_transfer=type_transfer,
            value=value,
            min_balance=min_balance,
            max_balance=max_balance,
            slippage=slippage,
        )
        self.contract_quoter = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.IZUMI.CONTRACTS.get(
                    self.acc.network.get(NETWORK_FIELDS.NAME)
                ).get("quoter")
            ),
            abi=config.IZUMI.ABI_QUOTER,
        )
        self.contract_router = self.acc.w3.eth.contract(
            address=eth_utils.address.to_checksum_address(
                config.IZUMI.CONTRACTS.get(
                    self.acc.network.get(NETWORK_FIELDS.NAME)
                ).get("router")
            ),
            abi=config.IZUMI.ABI_ROUTER,
        )

    # async def _get_path(self, from_token: Token_Info, to_token: Token_Info, fee: int):
    #     return f"{from_token.address[2:]}{fee:x}{to_token.address[2:]}"

    async def _get_pool_fee(self, from_token: Token_Info, to_token: Token_Info):
        pairs = (
            f"{from_token.symbol}/{to_token.symbol}",
            f"{to_token.symbol}/{from_token.symbol}",
        )
        fees = config.IZUMI.CONTRACTS.get(
            self.acc.network.get(NETWORK_FIELDS.NAME)
        ).get("pairs")
        fee = None
        for pair in pairs:
            fee = fees.get(pair)
            if fee is not None:
                break
        return fee

    async def _get_usdc_address(self):
        if self.acc.network.get(NETWORK_FIELDS.NAME) == config.Network.ZKSYNC:
            return eth_utils.address.to_checksum_address(
                "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4"
            )
        elif self.acc.network.get(NETWORK_FIELDS.NAME) == config.Network.LINEA:
            return eth_utils.address.to_checksum_address(
                "0x176211869cA2b568f2A7D4EE941E073a821EE1ff"
            )
        else:
            return eth_utils.address.to_checksum_address(
                "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4"
            )

    async def _get_path(self, from_token: Token_Info, to_token: Token_Info):
        usdc = (
            "USDC"
            if self.acc.network.get(NETWORK_FIELDS.NAME) != config.Network.ZKSYNC
            else "USDC.E"
        )
        if not (from_token.symbol == "USDT" or to_token.symbol == "USDT"):
            try:
                fee = await self._get_pool_fee(from_token=from_token, to_token=to_token)
                if fee is None:
                    return None
                from_token_bytes = HexBytes(from_token.address).rjust(20, b"\0")
                to_token_bytes = HexBytes(to_token.address).rjust(20, b"\0")
                fee_bytes = fee.to_bytes(3, "big")
                return from_token_bytes + fee_bytes + to_token_bytes
            except Exception as error:
                logger.error(error)
                return None
        elif usdc in [from_token.symbol, to_token.symbol] and usdc in [
            from_token.symbol,
            to_token.symbol,
        ]:
            from_token_bytes = HexBytes(from_token.address).rjust(20, b"\0")
            fee = await self._get_pool_fee(from_token=from_token, to_token=to_token)
            if fee is None:
                return None
            from_token_bytes = HexBytes(from_token.address).rjust(20, b"\0")
            to_token_bytes = HexBytes(to_token.address).rjust(20, b"\0")
            fee_bytes = fee.to_bytes(3, "big")
            return from_token_bytes + fee_bytes + to_token_bytes
        else:
            try:
                from_token_bytes = HexBytes(from_token.address).rjust(20, b"\0")
                fee1 = await self._get_pool_fee(
                    from_token=from_token,
                    to_token=Token_Info(address="", symbol=usdc, decimals=6),
                )
                fee_bytes_1 = fee1.to_bytes(3, "big")
                middle_token_bytes = HexBytes(await self._get_usdc_address()).rjust(
                    20, b"\0"
                )
                fee2 = await self._get_pool_fee(
                    from_token=Token_Info(address="", symbol=usdc, decimals=6),
                    to_token=to_token,
                )
                fee_bytes_2 = fee2.to_bytes(3, "big")
                to_token_bytes = HexBytes(to_token.address).rjust(20, b"\0")
                return (
                    from_token_bytes
                    + fee_bytes_1
                    + middle_token_bytes
                    + fee_bytes_2
                    + to_token_bytes
                )

            except Exception as error:
                logger.error(error)
                return None

    async def _get_amount_in(self, path: str, amount_to_send: Token_Amount):
        try:
            min_amount_out, _ = await self.contract_quoter.functions.swapAmount(
                amount_to_send.wei, path
            ).call()
            return int(min_amount_out - (min_amount_out / 100 * self.slippage))
        except Exception as error:
            logger.error(error)
            return None

    # https://developer.izumi.finance/
    async def _perform_swap(
        self,
        amount_to_send: Token_Amount,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        from_token, to_token = await Token_Info.to_wrapped_token(
            network=self.acc.network, from_token=from_token, to_token=to_token
        )
        path = await self._get_path(from_token=from_token, to_token=to_token)
        if not path:
            logger.error("FAIL GET PATH")
            return RESULT_TRANSACTION.FAIL
        amount_in = await self._get_amount_in(path=path, amount_to_send=amount_to_send)
        if not amount_in:
            return RESULT_TRANSACTION.FAIL
        if amount_in:
            amount_in = Token_Amount(
                amount=amount_in, decimals=to_token.decimals, wei=True
            )
        else:
            return RESULT_TRANSACTION.FAIL
        recipient = (
            self.acc.address
            if not await Token_Info.is_native_token(
                network=self.acc.network, token=to_token
            )
            else config.GENERAL.ZERO_ADDRESS
        )
        deadline = int(time.time()) + 10000

        data_swapAmount = await Web3Client.get_data(
            self.contract_router,
            "swapAmount",
            args=[
                (
                    path,  # path
                    recipient,  # recipient
                    amount_to_send.wei,  # amount
                    amount_in.wei,  # minAcquired
                    deadline,  # deadline
                )
            ],
        )

        if await Token_Info.is_native_token(network=self.acc.network, token=from_token):
            data_refund = await Web3Client.get_data(
                contract=self.contract_router,
                function_of_contract="refundETH",
                args=[],
            )

            data_multicall = await Web3Client.get_data(
                contract=self.contract_router,
                function_of_contract="multicall",
                args=[
                    [
                        data_swapAmount,
                        data_refund,
                    ]
                ],
            )
        elif await Token_Info.is_native_token(network=self.acc.network, token=to_token):
            data_unwrup = await Web3Client.get_data(
                contract=self.contract_router,
                function_of_contract="unwrapWETH9",
                args=[amount_in.wei, self.acc.address],
            )
            data_multicall = await Web3Client.get_data(
                contract=self.contract_router,
                function_of_contract="multicall",
                args=[
                    [
                        data_swapAmount,
                        data_unwrup,
                    ]
                ],
            )
        else:
            data_multicall = await Web3Client.get_data(
                contract=self.contract_router,
                function_of_contract="multicall",
                args=[
                    [
                        data_swapAmount,
                    ]
                ],
            )

        return await self._send_transaction(
            data=data_multicall,
            from_token=from_token,
            to_address=self.contract_router.address,
            amount_to_send=amount_to_send,
        )

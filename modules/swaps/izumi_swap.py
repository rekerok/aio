import time
import eth_utils
import config
from typing import Union
from utils import aiohttp
from helpers import contracts
from helpers import Token_Info, Token_Amount, Web3Swapper
from utils import TYPE_OF_TRANSACTION


class IzumiSwap(Web3Swapper):
    NAME = "IZUMI"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
        type_transfer: TYPE_OF_TRANSACTION = None,
        value: tuple[Union[int, float]] = None,
        min_balance: float = 0,
        slippage: float = 1.0,
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
                contracts.IZUMI_SWAP.get(self.acc.network.get("name"))
            ),
            abi=config.IZUMISWAP_ABI,
        )

    # async def _get_path(self, from_token: Token_Info, to_token: Token_Info, fee: int):
    #     return f"{from_token.address[2:]}{fee:x}{to_token.address[2:]}"

    async def _get_path(self, from_token: Token_Info, to_token: Token_Info, fee: int):
        hex_str = from_token.address
        hex_str += self.fee_2_hex(fee=fee)
        hex_str += to_token.address
        return hex_str.replace("0x", "")

    def fee_2_hex(self, fee: int):
        n0 = fee % 16
        n1 = (fee // 16) % 16
        n2 = (fee // 256) % 16
        n3 = (fee // 4096) % 16
        n4 = 0
        n5 = 0
        return (
            "0x"
            + self.num_2_hex(n5)
            + self.num_2_hex(n4)
            + self.num_2_hex(n3)
            + self.num_2_hex(n2)
            + self.num_2_hex(n1)
            + self.num_2_hex(n0)
        )

    def num_2_hex(self, num: int):
        if num < 10:
            return str(num)
        strs = "ABCDEF"
        return strs[num - 10]

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
        price_token_from = await aiohttp.get_json_aiohttp(
            f"https://api.izumi.finance/api/v1/token_info/price_info/{from_token.symbol}/?format=json"
        )
        price_token_to = await aiohttp.get_json_aiohttp(
            f"https://api.izumi.finance/api/v1/token_info/price_info/{to_token.symbol}/?format=json"
        )
        price_token_from, price_token_to = float(price_token_from.get("data")), float(
            price_token_to.get("data")
        )
        amount_in = Token_Amount(
            # amount_to_send.ETHER * price_token_from / price_token_to
            amount=(amount_to_send.ETHER * price_token_from / price_token_to)
            - (amount_to_send.ETHER * price_token_from / price_token_to)
            * self.slippage
            / 100,
            decimals=to_token.decimals,
        )

        deadline = int(time.time()) + 1000000
        fee = 500

        path = await self._get_path(from_token=from_token, to_token=to_token, fee=fee)

        recipient = (
            self.acc.address
            if to_token.symbol != self.acc.network.get("token").upper()
            else contracts.ZERO_ADDRESS
        )
        data_swapAmount = await self._get_data(
            self.contract,
            "swapAmount",
            args=[
                [
                    eth_utils.conversions.to_bytes(hexstr=path),  # path
                    recipient,  # recipient
                    amount_to_send.WEI,  # amount
                    amount_in.WEI,  # minAcquired
                    deadline,  # deadline
                ]
            ],
        )
        if from_token.symbol == self.acc.network.get("token").upper():
            data_refund = await self._get_data(
                contract=self.contract,
                function_of_contract="refundETH",
                args=[],
            )
            data_multicall = await self._get_data(
                contract=self.contract,
                function_of_contract="multicall",
                args=[
                    [
                        data_swapAmount,
                        eth_utils.conversions.to_bytes(hexstr=data_refund),
                    ]
                ],
            )
        else:
            data_unwrup = await self._get_data(
                contract=self.contract,
                function_of_contract="unwrapWETH9",
                args=[amount_in.WEI, self.acc.address],
            )
            data_multicall = await self._get_data(
                contract=self.contract,
                function_of_contract="multicall",
                args=[
                    [
                        data_swapAmount,
                        data_unwrup,
                    ]
                ],
            )
        value = (
            amount_to_send
            if from_token.symbol == self.acc.network.get("token").upper()
            else None
        )
        value_approove = (
            None
            if from_token.symbol == self.acc.network.get("token").upper()
            else amount_to_send
        )
        await self._send_swap_transaction(
            data=data_multicall,
            from_token=from_token,
            to_address=self.contract.address,
            value=value,
            value_approove=value_approove,
        )

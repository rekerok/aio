import utils
import config
import eth_utils
from typing import Union
from loguru import logger
from modules.account import Account
from utils.token_info import Token_Info
from utils.token_amount import Token_Amount
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION


class Across:
    NAME = "ACROSS"

    def __init__(
        self,
        private_key: str = None,
        network: dict = None,
    ) -> None:
        self.acc = Account(private_key=private_key, network=network)

    async def _get_info(
        self,
        from_token: Token_Info,
        to_chain_id: int,
        amount_to_send: Token_Amount,
        from_chain_id: int,
    ):
        url = "https://across.to/api/suggested-fees"
        params = {
            "token": from_token.address,
            "destinationChainId": to_chain_id,
            "amount": amount_to_send.WEI,
            "originChainId": from_chain_id,
        }
        response = await utils.aiohttp.get_json_aiohttp(url=url, params=params)
        if not response:
            return None
        return response

    async def _get_limits(self, to_chain_id: int, from_token: Token_Info):
        url = "https://across.to/api/limits"

        params = {
            "token": from_token.address,
            "destinationChainId": to_chain_id,
            "originChainId": await self.acc.w3.eth.chain_id,
        }

        response = await utils.aiohttp.get_json_aiohttp(url=url, params=params)
        if not response:
            return None
        return response

    async def _check_route(
        self,
        from_chain_id: int,
        to_chain_id: int,
        from_token: Token_Info,
        to_token: Token_Info,
    ):
        url = "https://across.to/api/available-routes"

        params = {
            "originChainId": from_chain_id,
            "destinationChainId": to_chain_id,
            "originToken": from_token.address,
            "destinationToken": to_token.address,
        }

        response = await utils.aiohttp.get_json_aiohttp(url=url, params=params)
        if not response:
            return None
        return response

    # https://docs.across.to/v/developer-docs/developers/across-api
    async def bridge(
        self,
        from_token_address: str = "",
        to_token_address: str = "",
        to_chain: config.Network = None,
        amount_to_get: Union[int, float] = 0.0001,
        amount_to_send: Union[int, float] = 1,
    ):
        from_chain_id = await self.acc.w3.eth.chain_id
        to_chain_id: int = config.GENERAL.CHAIN_IDS.value.get(to_chain)
        from_token: Token_Info = await Token_Info.get_info_token(
            acc=self.acc, token_address=from_token_address
        )
        from_token = (
            await Token_Info.to_wrapped_token(
                network=self.acc.network, from_token=from_token
            )
        )[0]

        if to_token_address == "":
            to_token: Token_Info = Token_Info(
                address=config.GENERAL.WETH.value.get(to_chain),
                symbol="WETH",
                decimals=18,
            )
        else:
            to_token: Token_Info = Token_Info(
                address=to_token_address,
                symbol=from_token.symbol,
                decimals=from_token.decimals,
            )
        amount_to_send: Token_Amount = Token_Amount(
            amount=amount_to_send, decimals=from_token.decimals
        )

        info = await self._get_info(
            from_token=from_token,
            to_chain_id=to_chain_id,
            amount_to_send=amount_to_send,
            from_chain_id=from_chain_id,
        )
        if info is None:
            logger.error("FAIL GET INFO")
            return RESULT_TRANSACTION.FAIL

        limits = await self._get_limits(to_chain_id=to_chain_id, from_token=from_token)
        if not limits:
            logger.error("DON'T GET LIMITS FOR BRIDGE")
        if not (
            int(limits.get("minDeposit"))
            <= amount_to_send.WEI
            <= int(limits.get("maxDeposit"))
        ):
            logger.error("FAIL LIMITS")
            return RESULT_TRANSACTION.FAIL

        if (
            await self._check_route(
                from_chain_id=await self.acc.w3.eth.chain_id,
                to_chain_id=to_chain_id,
                from_token=from_token,
                to_token=to_token,
            )
            is None
            or []
        ):
            logger.error("INVALID DATA")
            return RESULT_TRANSACTION.FAIL

        args = [
            self.acc.address,
            from_token.address,
            amount_to_send.WEI,
            to_chain_id,
            int(info.get("relayFeePct")),
            int(info.get("timestamp")),
            bytes(),
            2**256 - 1,
        ]
        pool_address = eth_utils.address.to_checksum_address(
            info.get("spokePoolAddress")
        )

        try:
            if from_chain_id == 324:
                contract_across = self.acc.w3.eth.contract(
                    address=pool_address, abi=config.ACROSS.ABI_POOL.value
                )
                data = contract_across.encodeABI(
                    "deposit",
                    args=(*args,),
                )
            else:
                if await Token_Info.is_native_token(
                    network=self.acc.network, token=from_token
                ):
                    args.insert(0, pool_address)
                    contract_across = self.acc.w3.eth.contract(
                        address=eth_utils.address.to_checksum_address(
                            config.ACROSS.CONTRACTS.value.get(
                                self.acc.network.get(NETWORK_FIELDS.NAME)
                            )
                        ),
                        abi=config.ACROSS.ABI_ROUTER.value,
                    )
                    data = contract_across.encodeABI(
                        "deposit",
                        args=(*args,),
                    )
                else:
                    contract_across = self.acc.w3.eth.contract(
                        address=pool_address,
                        abi=config.ACROSS.ABI_POOL.value,
                    )
                    data = contract_across.encodeABI(
                        "deposit",
                        args=(*args,),
                    )
                    data = contract_across.encodeABI(
                        "multicall",
                        args=[[data]],
                    )

            if not (
                await Token_Info.is_native_token(self.acc.network, token=from_token)
            ):
                await self.acc.approve(
                    token_address=from_token.address,
                    spender=contract_across.address,
                    amount=amount_to_send,
                )
                return await self.acc.send_transaction(
                    to_address=contract_across.address,
                    data=data,
                    value=0,
                )
            else:
                return await self.acc.send_transaction(
                    to_address=contract_across.address,
                    data=data,
                    value=amount_to_send,
                )

        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL

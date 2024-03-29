import config
import eth_utils
from loguru import logger
from utils.enums import NETWORK_FIELDS


class Token_Info:
    address: str
    symbol: str
    decimals: int

    def __init__(self, address, symbol, decimals):
        self.address: str = address
        self.symbol: str = symbol
        self.decimals: int = decimals

    @staticmethod
    async def get_info_token(acc, token_address: str = None):
        try:
            if not token_address or token_address == "":
                name: str = acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN)
                return Token_Info(address="", symbol=name.upper(), decimals=18)
            else:
                token_address = acc.w3.to_checksum_address(token_address)
                contract = acc.w3.eth.contract(
                    address=token_address, abi=config.GENERAL.ERC20_ABI
                )
                symbol = await contract.functions.symbol().call()
                return Token_Info(
                    address=token_address,
                    symbol=symbol.upper(),
                    decimals=await contract.functions.decimals().call(),
                )
        except Exception as error:
            logger.error(error)
            return None

    @staticmethod
    async def is_native_token(network: dict, token: "Token_Info"):
        return (
            True if token.symbol == network.get(NETWORK_FIELDS.NATIVE_TOKEN) else False
        )

    @staticmethod
    async def to_wrapped_token(
        network: config.Network,
        from_token: "Token_Info" = None,
        to_token: "Token_Info" = None,
    ):
        if from_token:
            if from_token.address == "":
                from_token.address = eth_utils.address.to_checksum_address(
                    config.GENERAL.WETH.get(network.get(NETWORK_FIELDS.NAME))
                )
        if to_token:
            if to_token.address == "":
                to_token.address = eth_utils.address.to_checksum_address(
                    config.GENERAL.WETH.get(network.get(NETWORK_FIELDS.NAME))
                )
        return from_token, to_token

    @staticmethod
    async def to_native_token(
        from_token: "Token_Info" = None,
        to_token: "Token_Info" = None,
    ):
        if from_token:
            if from_token.address == "":
                from_token.address = eth_utils.address.to_checksum_address(
                    config.GENERAL.NATIVE_TOKEN
                )
        if to_token:
            if to_token.address == "":
                to_token.address = eth_utils.address.to_checksum_address(
                    config.GENERAL.NATIVE_TOKEN
                )
        return from_token, to_token

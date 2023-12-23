import eth_utils
import config
from helpers import contracts
from modules.account import Account


class Token_Info:
    address: str
    symbol: str
    decimals: int

    def __init__(self, address, symbol, decimals):
        self.address: str = address
        self.symbol: str = symbol
        self.decimals: int = decimals

    @staticmethod
    async def get_info_token(acc: Account, token_address: str = None):
        if not token_address or token_address == "":
            name: str = acc.network["token"]
            return Token_Info(address="", symbol=name.upper(), decimals=18)
        else:
            token_address = acc.w3.to_checksum_address(token_address)
            contract = acc.w3.eth.contract(address=token_address, abi=config.ERC20_ABI)
            symbol = await contract.functions.symbol().call()
        return Token_Info(
            address=token_address,
            symbol=symbol.upper(),
            decimals=await contract.functions.decimals().call(),
        )

    @staticmethod
    async def to_wrapped_token(
        name_network: str,
        from_token: "Token_Info" = None,
        to_token: "Token_Info" = None,
    ):
        if from_token:
            if from_token.address == "":
                from_token.address = eth_utils.address.to_checksum_address(
                    contracts.WETH_CONTRACTS.get(name_network)
                )
        if to_token:
            if to_token.address == "":
                to_token.address = eth_utils.address.to_checksum_address(
                    contracts.WETH_CONTRACTS.get(name_network)
                )
        return from_token, to_token

    @staticmethod
    async def to_native_token(from_token: "Token_Info", to_token: "Token_Info"):
        if from_token.address == "":
            from_token.address = eth_utils.address.to_checksum_address(
                contracts.NATIVE_TOKEN
            )
        if to_token.address == "":
            to_token.address = eth_utils.address.to_checksum_address(
                contracts.NATIVE_TOKEN
            )
        return from_token, to_token

import config
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

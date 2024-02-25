import eth_utils
from loguru import logger
from modules.web3Nft import Web3Nft
import config
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION
from utils.token_amount import Token_Amount


class L2pass_NFT(Web3Nft):
    NAME = "L2PASS NFT"

    def __init__(self, private_key: str, network: dict) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
        )

    async def _perform_mint(self, nft_contract_address: str):
        try:
            contract = self.acc.w3.eth.contract(
                address=nft_contract_address, abi=config.L2PASS.ABI_NFT
            )
            mint_price = Token_Amount(
                await contract.functions.mintPrice().call(), wei=True
            )
            logger.info(
                f"MINT PRICE = {mint_price.ETHER} {self.acc.network.get(NETWORK_FIELDS.NATIVE_TOKEN)}"
            )
            data = await self.get_data(
                contract=contract, function_of_contract="mint", args=(1,)
            )
            if data is None:
                logger.error("FAIL GET DATA")
                return RESULT_TRANSACTION.FAIL
            return await self.acc.send_transaction(
                to_address=contract.address, data=data, value=mint_price
            )
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL

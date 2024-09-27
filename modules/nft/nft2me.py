import eth_utils
from loguru import logger
from modules.web3Nft import Web3Nft
import config
from utils.enums import NETWORK_FIELDS, RESULT_TRANSACTION
from utils.token_amount import Token_Amount


class NFT2ME(Web3Nft):
    NAME = "NFT2ME"

    def __init__(self, private_key: str, network: dict) -> None:
        super().__init__(
            private_key=private_key,
            network=network,
        )

    async def _perform_mint(self, nft_contract_address: str):
        try:
            contract = self.acc.w3.eth.contract(
                address=eth_utils.address.to_checksum_address(nft_contract_address),
                abi=config.NFT2ME.ABI,
            )
            name_nft = await contract.functions.name().call()
            mint_price = Token_Amount(
                amount=await contract.functions.mintPrice().call(), decimals=18, wei=True
            )
            logger.info(f'NAME NFT "{name_nft}"')
            logger.info(f"PRICE {mint_price.ether} ETH")
            data = await self.get_data(contract=contract, function_of_contract="mint")
            if data is None:
                logger.error("FAIL GET DATA")
                return RESULT_TRANSACTION.FAIL
            return await self.acc.send_transaction(
                to_address=contract.address, data=data, value=mint_price
            )
        except Exception as error:
            logger.error(error)
            return RESULT_TRANSACTION.FAIL

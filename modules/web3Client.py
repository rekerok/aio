from loguru import logger
from modules.account import Account
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

    async def _send_transaction(
        self,
        data,
        from_token: Token_Info,
        to_address: str,
        amount_to_send: Token_Amount,
        value=None,
    ):
        if value is None:
            value, value_approve = await Web3Client.get_value_and_allowance(
                amount=amount_to_send,
                from_native_token=await Token_Info.is_native_token(
                    self.acc.network, token=from_token
                ),
            )
            if value_approve:
                await self.acc.approve(
                    token_address=from_token.address,
                    spender=to_address,
                    amount=value_approve,
                )
        if not await Token_Info.is_native_token(self.acc.network, token=from_token):
            await self.acc.approve(
                token_address=from_token.address,
                spender=to_address,
                amount=amount_to_send,
            )
        return await self.acc.send_transaction(
            to_address=to_address, data=data, value=value
        )

    @staticmethod
    async def get_value_and_allowance(amount: Token_Amount, from_native_token: bool):
        if from_native_token:
            value = amount
            value_approve = None
        else:
            value = None
            value_approve = amount
        return value, value_approve

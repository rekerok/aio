from typing import Union


class Token_Amount:
    def __init__(
        self, amount: Union[float, int], decimals: int = 18, wei: bool = False
    ) -> None:
        if wei:
            self.wei = int(amount)
            self.ether = float(amount / pow(10, decimals))
        else:
            self.wei = int(amount * pow(10, decimals))
            self.ether = float(amount)
        self.decimal = decimals

"""Value objects for the cart module."""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass
class Money:
    """Value object para representar um valor monetário."""

    amount: Decimal
    currency: str = 'BRL'

    def __init__(
        self, amount: Decimal | float | int | str, currency: str = 'BRL'
    ):
        """Initialize a Money object.

        Args:
            amount: The amount of money.
            currency: The currency of the money.

        """
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))

        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        object.__setattr__(self, 'amount', amount)
        object.__setattr__(self, 'currency', currency)

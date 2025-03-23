"""Value objects for the cart module."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal


@dataclass(frozen=True)
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

    def __str__(self) -> str:
        """Representação de string formatada como moeda."""
        if self.currency == 'BRL':
            return f'R$ {self.amount:.2f}'
        return f'{self.currency} {self.amount:.2f}'

    def __repr__(self) -> str:
        """Representação para debugging."""
        return f"Money({self.amount}, '{self.currency}')"

    def __add__(self, other: Money) -> Money:
        """Soma dois valores monetários.

        Args:
            other: Outro objeto Money

        Returns:
            Novo objeto Money com a soma

        Raises:
            ValueError: Se as moedas forem diferentes
            TypeError: Se não for um objeto Money

        """
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(self._get_incompatible_currency_message(other))

        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        """Subtrai dois valores monetários.

        Args:
            other: Outro objeto Money

        Returns:
            Novo objeto Money com a subtração

        Raises:
            ValueError: Se as moedas forem diferentes
            TypeError: Se não for um objeto Money

        """
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(self._get_incompatible_currency_message(other))

        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, other: int | float | Decimal) -> Money:
        """Multiplica o valor monetário por um escalar.

        Args:
            other: Valor escalar (int, float ou Decimal)

        Returns:
            Novo objeto Money com o resultado da multiplicação

        Raises:
            TypeError: Se o multiplicador não for um número

        """
        # if not isinstance(other, (int, float, Decimal)):
        #     return NotImplemented

        if isinstance(other, float):
            other = Decimal(str(other))
        elif isinstance(other, int):
            other = Decimal(other)

        return Money(self.amount * other, self.currency)

    def __truediv__(self, other: int | float | Decimal) -> Money:
        """Divide o valor monetário por um escalar.

        Args:
            other: Valor escalar (int, float ou Decimal)

        Returns:
            Novo objeto Money com o resultado da divisão

        Raises:
            TypeError: Se o divisor não for um número
            ZeroDivisionError: Se o divisor for zero

        """
        # if not isinstance(other, (int, float, Decimal)):
        #     return NotImplemented

        if other == 0:
            raise ZeroDivisionError('Divisão por zero')

        if isinstance(other, float):
            other = Decimal(str(other))
        elif isinstance(other, int):
            other = Decimal(other)

        return Money(self.amount / other, self.currency)

    def __eq__(self, other: object) -> bool:
        """Verifica se dois valores monetários são iguais.

        Args:
            other: Outro objeto para comparação

        Returns:
            True se forem iguais, False caso contrário

        """
        if not isinstance(other, Money):
            return NotImplemented

        return self.currency == other.currency and self.amount == other.amount

    def __lt__(self, other: Money) -> bool:
        """Verifica se este valor é menor que outro.

        Args:
            other: Outro objeto Money para comparação

        Returns:
            True se este valor for menor, False caso contrário

        Raises:
            ValueError: Se as moedas forem diferentes

        """
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(self._get_incompatible_currency_message(other))

        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        """Verifica se este valor é menor ou igual a outro.

        Args:
            other: Outro objeto Money para comparação

        Returns:
            True se este valor for menor ou igual, False caso contrário

        Raises:
            ValueError: Se as moedas forem diferentes

        """
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(self._get_incompatible_currency_message(other))

        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        """Verifica se este valor é maior que outro.

        Args:
            other: Outro objeto Money para comparação

        Returns:
            True se este valor for maior, False caso contrário

        Raises:
            ValueError: Se as moedas forem diferentes

        """
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(self._get_incompatible_currency_message(other))

        return self.amount > other.amount

    def __ge__(self, other: Money) -> bool:
        """Verifica se este valor é maior ou igual a outro.

        Args:
            other: Outro objeto Money para comparação

        Returns:
            True se este valor for maior ou igual, False caso contrário

        Raises:
            ValueError: Se as moedas forem diferentes

        """
        if not isinstance(other, Money):
            return NotImplemented

        if self.currency != other.currency:
            raise ValueError(self._get_incompatible_currency_message(other))

        return self.amount >= other.amount

    def is_zero(self) -> bool:
        """Verifica se o valor é zero.

        Returns:
            True se o valor for zero, False caso contrário

        """
        return self.amount == Decimal('0')

    def is_positive(self) -> bool:
        """Verifica se o valor é positivo.

        Returns:
            True se o valor for positivo, False caso contrário

        """
        return self.amount > Decimal('0')

    def is_negative(self) -> bool:
        """Verificar se o valor é negativo.

        Returns:
            True se o valor for negativo, False caso contrário

        """
        return self.amount < Decimal('0')

    def to_dict(self) -> dict:
        """Converta o objeto para um dicionário.

        Returns:
            Dicionário com os dados do objeto

        """
        return {
            'amount': float(
                self.amount
            ),  # Converter para float para serialização
            'currency': self.currency,
        }

    def _get_incompatible_currency_message(self, other: Money) -> str:
        return (
            f'Não é possível comparar moedas diferentes: '
            f'{self.currency} e {other.currency}'
        )

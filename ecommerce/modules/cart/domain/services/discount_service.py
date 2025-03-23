"""Services for the discount entity."""

from datetime import datetime
from uuid import UUID

from ..entities import Discount, DiscountType
from ..repositories.discount_repository import (
    DiscountRepository,
)
from ..value_objects import Money


class DiscountService:
    """Service for the discount entity."""

    def __init__(self, discount_repository: DiscountRepository):
        """Initialize the discount service."""
        self.discount_repository = discount_repository

    async def apply_discount_to_cart(
        self,
        cart_total: Money,
        discount_id: UUID,
    ) -> Money | None:
        """Aplica um desconto a um valor de carrinho.

        Args:
            cart_total: Valor total do carrinho.
            discount_id: ID do desconto a ser aplicado.

        Returns:
            Valor total do carrinho com o desconto aplicado.

        """
        discount = await self.discount_repository.get_by_id(discount_id)

        if not discount:
            raise ValueError('Desconto não encontrado')

        if not discount.is_valid(cart_total):
            raise ValueError('Desconto inválido')

        discount_value = discount.apply_to(cart_total)

        discount.use()
        await self.discount_repository.save(discount)

        return discount_value

    async def validate_coupon_code(
        self, code: str, order_value: Money
    ) -> Discount | None:
        """Valida um código de cupom para determinado valor de pedido.

        Args:
            code: Código do cupom.
            order_value: Valor total da ordem.

        Returns:
            Desconto valido ou None se o cupom não for valido.

        """
        discount = await self.discount_repository.get_by_code(code)

        if not discount:
            return None

        if not discount.is_valid(order_value):
            return None

        return discount

    async def create_percentage_discount(
        self,
        percentage: float,
        code: str,
        description: str,
        minimum_order_value: Money | None = None,
        valid_until: datetime | None = None,
        max_usage_count: int | None = None,
    ) -> Discount:
        """Cria um novo desconto percentual.

        Args:
            percentage: Valor do percentual (ex: 10 para 10%)
            code: Código do cupom/desconto
            description: Descrição do desconto
            minimum_order_value: Valor mínimo do pedido
            valid_until: Data de expiração
            max_usage_count: Número máximo de usos

        Returns:
            O desconto criado e persistido

        Raises:
            ValueError: Se o percentual for inválido

        """
        if percentage <= 0 or percentage > 100:
            raise ValueError('Percentual deve estar entre 0 e 100')

        discount = Discount(
            type=DiscountType.PERCENTAGE,
            value=percentage,
            code=code,
            description=description,
            minimum_order_value=minimum_order_value,
            valid_until=valid_until,
            max_usage_count=max_usage_count,
        )

        return await self.discount_repository.save(discount)

    async def create_fixed_amount_discount(
        self,
        amount: Money,
        code: str,
        description: str,
        minimum_order_value: Money | None = None,
        valid_until: datetime | None = None,
        max_usage_count: int | None = None,
    ) -> Discount:
        """Cria um novo desconto de valor fixo.

        Args:
            amount: Valor fixo do desconto
            code: Código do cupom/desconto
            description: Descrição do desconto
            minimum_order_value: Valor mínimo do pedido
            valid_until: Data de expiração
            max_usage_count: Número máximo de usos

        Returns:
            O desconto criado e persistido

        Raises:
            ValueError: Se o valor for negativo

        """
        if not amount.is_positive():
            raise ValueError('Valor do desconto deve ser positivo')

        discount = Discount(
            type=DiscountType.FIXED_AMOUNT,
            value=amount.amount,  # Convertemos Money para valor numérico
            code=code,
            description=description,
            minimum_order_value=minimum_order_value,
            valid_until=valid_until,
            max_usage_count=max_usage_count,
        )

        return await self.discount_repository.save(discount)

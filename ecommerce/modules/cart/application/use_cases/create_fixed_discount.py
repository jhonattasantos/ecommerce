"""Caso de uso para criação de desconto de valor fixo."""

from datetime import datetime

from ...domain.entities.discount import Discount
from ...domain.services.discount_service import DiscountService
from ...domain.value_objects.money import Money


class CreateFixedDiscountUseCase:
    """Caso de uso para criar um desconto de valor fixo."""

    def __init__(self, discount_service: DiscountService):
        """Inicializa o caso de uso com o serviço de desconto.

        Args:
            discount_service: Serviço que gerencia operações com descontos

        """
        self.discount_service = discount_service

    async def execute(
        self,
        amount: float,
        code: str,
        description: str,
        currency: str = 'BRL',
        minimum_order_value: float = 0,
        valid_until: datetime | None = None,
        max_usage_count: int | None = None,
    ) -> Discount:
        """Executa o caso de uso para criar um desconto de valor fixo.

        Args:
            amount: Valor do desconto
            code: Código do cupom
            description: Descrição do desconto
            currency: Moeda (padrão BRL)
            minimum_order_value: Valor mínimo de pedido para aplicar o desconto
            valid_until: Data de expiração do desconto
            max_usage_count: Número máximo de usos

        Returns:
            O desconto criado

        Raises:
            ValueError: Se os parâmetros forem inválidos

        """
        # Validação de parâmetros
        if amount <= 0:
            raise ValueError('Valor do desconto deve ser maior que zero')

        if not code:
            raise ValueError('Código do cupom é obrigatório')

        # Converter valores para objetos de domínio
        discount_amount = Money(amount, currency)
        min_order = Money(minimum_order_value, currency)

        # Delegar a criação ao serviço de domínio
        return await self.discount_service.create_fixed_amount_discount(
            amount=discount_amount,
            code=code,
            description=description,
            minimum_order_value=min_order,
            valid_until=valid_until,
            max_usage_count=max_usage_count,
        )

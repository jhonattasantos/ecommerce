"""Entities for the cart module."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from uuid import UUID, uuid4

from ecommerce.modules.cart.domain.value_objects import Money


class DiscountType(Enum):
    """Enum for the type of discount."""

    PERCENTAGE = auto()
    FIXED_AMOUNT = auto()
    COUPON = auto()


@dataclass
class Discount:
    """Entity for the discount."""

    type: DiscountType
    value: float
    id: UUID = field(default_factory=uuid4)
    code: str | None = None
    description: str = ''
    minimum_order_value: Money = field(default_factory=lambda: Money(0))
    maximum_discount_amount: Money = field(default_factory=lambda: Money(0))
    valid_from: datetime = field(default_factory=datetime.now)
    valid_until: datetime | None = None
    max_usage_count: int | None = None
    current_usage_count: int = 0

    def is_valid(self, order_value: Money) -> bool:
        """
        Verifica se o desconto é válido para o pedido atual.
        
        Args:
            order_value: Valor do pedido a ser verificado
            
        Returns:
            True se o desconto for válido, False caso contrário
        """
        now = datetime.now()
        
        # Verificar validade temporal
        if now < self.valid_from:
            return False
            
        if self.valid_until and now > self.valid_until:
            return False
            
        # Verificar limite de uso
        if self.max_usage_count and self.current_usage_count >= self.max_usage_count:
            return False
            
        # Verificar valor mínimo do pedido
        if order_value < self.minimum_order_value:
            return False
            
        return True

    def apply_to(self, order_value: Money) -> Money:
        """
        Apply the discount to the order value.
        """
        
        if not self.is_valid(order_value):
            return Money(0)
        
        if self.type == DiscountType.PERCENTAGE:
            # Calcular desconto percentual
            total_discount = order_value.amount * (self.value / 100)
            discount_value = order_value.amount - total_discount

            if self.maximum_discount_amount.amount > 0 and total_discount > self.maximum_discount_amount.amount:
                discount_value = order_value.amount - self.maximum_discount_amount.amount
            
            return Money(discount_value)
            
        elif self.type == DiscountType.FIXED_AMOUNT:
            # Retornar valor fixo, limitado ao valor do pedido
            fixed_amount = min(self.value.amount, order_value.amount)
            discount_value = order_value.amount - fixed_amount
            return Money(discount_value)
            
        elif self.type == DiscountType.COUPON:
            # Lógica para cupons especiais pode ser mais complexa
            # Por simplicidade, tratamos como um desconto fixo
            return Money(min(self.value.amount, order_value.amount))
            
        return Money(0)
    
    def use(self) -> None:
        """
        Registra o uso do desconto, incrementando o contador de uso.
        """
        self.current_usage_count += 1
        


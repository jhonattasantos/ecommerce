import pytest
from decimal import Decimal

from ecommerce.modules.cart.domain.entities.discount import Discount, DiscountType
from ecommerce.modules.cart.domain.value_objects.money import Money

class TestDiscount:
    def test_percentage_discount_calculation(self):
        """Testa cálculo de desconto percentual."""
        # Arrange
        original_price = Money(Decimal("100.00"))
        discount = Discount(type=DiscountType.PERCENTAGE, value=Decimal("10"))
        
        # Act
        discounted_price = discount.apply_to(original_price)
        
        # Assert
        assert discounted_price.amount == Decimal("90.00")
    
    def test_fixed_discount_calculation(self):
        """Testa cálculo de desconto de valor fixo."""
        # Arrange
        original_price = Money(Decimal("100.00"))
        discount = Discount(type=DiscountType.FIXED_AMOUNT,value=Money(Decimal("15.00")))
        
        # Act
        discounted_price = discount.apply_to(original_price)
        
        # Assert
        assert discounted_price.amount == Decimal("85.00")
    
    def test_discount_cannot_result_in_negative_price(self):
        """Testa que um desconto não pode resultar em preço negativo."""
        # Arrange
        original_price = Money(Decimal("50.00"))
        discount = Discount(type=DiscountType.FIXED_AMOUNT,value=Money(Decimal("75.00")))
        
        # Act
        discounted_price = discount.apply_to(original_price)
        
        # Assert
        assert discounted_price.amount == Decimal("0.00")
    
    def test_discount_with_minimum_purchase(self):
        """Testa desconto com valor mínimo de compra."""
        # Arrange
        discount = Discount(
            type=DiscountType.PERCENTAGE,
            value=Decimal("20"),
            minimum_order_value=Money(Decimal("100.00"))
        )
        
        # Act & Assert - Abaixo do mínimo
        small_purchase = Money(Decimal("50.00"))
        result = discount.apply_to(small_purchase)

        assert result.amount == Decimal("50.00")
        
        # Act & Assert - Acima do mínimo
        large_purchase = Money(Decimal("200.00"))
        result = discount.apply_to(large_purchase)
        assert result.amount == Decimal("160.00")
    
    def test_discount_with_maximum_amount(self):
        """Testa desconto com valor máximo limitado."""
        # Arrange
        discount = Discount(
            type=DiscountType.PERCENTAGE,
            value=Decimal("30"),
            maximum_discount_amount=Money(Decimal("50.00"))
        )
        
        # Act & Assert - Desconto normal
        purchase = Money(Decimal("100.00"))
        result = discount.apply_to(purchase)
        
        assert result.amount == Decimal("70.00")  # 30% de desconto
        
        # Act & Assert - Desconto limitado
        large_purchase = Money(Decimal("500.00"))
        result = discount.apply_to(large_purchase)
        assert result.amount == Decimal("450.00")  # Limitado a 50 de desconto
    
    def test_discount_validity_period(self):
        """Testa desconto com período de validade."""
        from datetime import datetime, timedelta
        
        # Arrange
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        tomorrow = now + timedelta(days=1)
        
        # Desconto válido
        valid_discount = Discount(
            type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            valid_from=yesterday,
            valid_until=tomorrow
        )
        
        # Desconto expirado
        expired_discount = Discount(
            type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            valid_from=yesterday - timedelta(days=10),
            valid_until=yesterday
        )
        
        # Desconto futuro
        future_discount = Discount(
            type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            valid_from=tomorrow,
            valid_until=tomorrow + timedelta(days=10)
        )
        
        original_price = Money(Decimal("100.00"))
        
        # Act & Assert
        assert valid_discount.is_valid(original_price) is True
        assert valid_discount.apply_to(original_price).amount == Decimal("90.00")
        
        assert expired_discount.is_valid(original_price) is False
        assert expired_discount.apply_to(original_price).amount == Decimal("100.00")
        
        assert future_discount.is_valid(original_price) is False
        assert future_discount.apply_to(original_price).amount == Decimal("100.00") 

    def test_discount_usage_limit(self):
        """Testa desconto com limite de uso."""
        # Arrange
        discount = Discount(
            type=DiscountType.PERCENTAGE,
            value=Decimal("10"),
            max_usage_count=2
        )
        
        # Act & Assert - Primeiro uso
        original_price = Money(Decimal("100.00"))
        result = discount.apply_to(original_price)

        assert result.amount == Decimal("90.00")

        # Act & Assert - Segundo uso
        result = discount.apply_to(original_price)
        assert result.amount == Decimal("90.00")

        # Act & Assert - Terceiro uso
        result = discount.apply_to(original_price)
        assert result.amount == Decimal("100.00")
        
        
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
        discounted_price = discount.calculate(original_price)
        
        # Assert
        assert discounted_price.amount == Decimal("90.00")
    
    # def test_fixed_discount_calculation(self):
    #     """Testa cálculo de desconto de valor fixo."""
    #     # Arrange
    #     original_price = Money(Decimal("100.00"))
    #     discount = Discount(fixed_amount=Money(Decimal("15.00")))
        
    #     # Act
    #     discounted_price = discount.apply_to(original_price)
        
    #     # Assert
    #     assert discounted_price.amount == Decimal("85.00")
    
    # def test_discount_cannot_result_in_negative_price(self):
    #     """Testa que um desconto não pode resultar em preço negativo."""
    #     # Arrange
    #     original_price = Money(Decimal("50.00"))
    #     discount = Discount(fixed_amount=Money(Decimal("75.00")))
        
    #     # Act
    #     discounted_price = discount.apply_to(original_price)
        
    #     # Assert
    #     assert discounted_price.amount == Decimal("0.00")
    
    # def test_discount_with_minimum_purchase(self):
    #     """Testa desconto com valor mínimo de compra."""
    #     # Arrange
    #     discount = Discount(
    #         percentage=Decimal("20"),
    #         minimum_purchase_amount=Money(Decimal("100.00"))
    #     )
        
    #     # Act & Assert - Abaixo do mínimo
    #     small_purchase = Money(Decimal("50.00"))
    #     result = discount.apply_to(small_purchase)
    #     assert result.amount == small_purchase.amount
        
    #     # Act & Assert - Acima do mínimo
    #     large_purchase = Money(Decimal("200.00"))
    #     result = discount.apply_to(large_purchase)
    #     assert result.amount == Decimal("160.00")
    
    # def test_discount_with_maximum_amount(self):
    #     """Testa desconto com valor máximo limitado."""
    #     # Arrange
    #     discount = Discount(
    #         percentage=Decimal("30"),
    #         maximum_discount_amount=Money(Decimal("50.00"))
    #     )
        
    #     # Act & Assert - Desconto normal
    #     purchase = Money(Decimal("100.00"))
    #     result = discount.apply_to(purchase)
    #     assert result.amount == Decimal("70.00")  # 30% de desconto
        
    #     # Act & Assert - Desconto limitado
    #     large_purchase = Money(Decimal("500.00"))
    #     result = discount.apply_to(large_purchase)
    #     assert result.amount == Decimal("450.00")  # Limitado a 50 de desconto
    
    # def test_discount_validity_period(self):
    #     """Testa desconto com período de validade."""
    #     from datetime import datetime, timedelta
        
    #     # Arrange
    #     now = datetime.now()
    #     yesterday = now - timedelta(days=1)
    #     tomorrow = now + timedelta(days=1)
        
    #     # Desconto válido
    #     valid_discount = Discount(
    #         percentage=Decimal("10"),
    #         start_date=yesterday,
    #         end_date=tomorrow
    #     )
        
    #     # Desconto expirado
    #     expired_discount = Discount(
    #         percentage=Decimal("10"),
    #         start_date=yesterday - timedelta(days=10),
    #         end_date=yesterday
    #     )
        
    #     # Desconto futuro
    #     future_discount = Discount(
    #         percentage=Decimal("10"),
    #         start_date=tomorrow,
    #         end_date=tomorrow + timedelta(days=10)
    #     )
        
    #     original_price = Money(Decimal("100.00"))
        
    #     # Act & Assert
    #     assert valid_discount.is_valid() is True
    #     assert valid_discount.apply_to(original_price).amount == Decimal("90.00")
        
    #     assert expired_discount.is_valid() is False
    #     assert expired_discount.apply_to(original_price).amount == Decimal("100.00")
        
    #     assert future_discount.is_valid() is False
    #     assert future_discount.apply_to(original_price).amount == Decimal("100.00") 
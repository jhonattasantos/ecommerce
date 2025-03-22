"""Entities for the cart module."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class CartItem:
    """Entity for the cart item."""

    id: UUID = field(default_factory=uuid4)
    cart_id: UUID
    product_id: UUID
    quantity: int
    price: float = 0.0
    added_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

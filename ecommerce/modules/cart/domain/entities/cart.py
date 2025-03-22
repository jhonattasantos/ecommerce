"""Entities for the cart module."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from .cart_item import CartItem
from .discount import Discount


@dataclass
class Cart:
    """Entity for the cart."""

    id: UUID = field(default_factory=uuid4)
    user_id: UUID | None = None
    items: list[CartItem] = field(default_factory=list)
    discounts: list[Discount] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    session_id: str | None = None

    def add_item(self, item: CartItem):
        """Add an item to the cart."""
        self.items.append(item)

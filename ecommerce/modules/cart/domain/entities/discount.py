"""Entities for the cart module."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from uuid import UUID, uuid4

from ..value_objects import Money


class DiscountType(Enum):
    """Enum for the type of discount."""

    PERCENTAGE = auto()
    FIXED_AMOUNT = auto()
    COUPON = auto()


@dataclass
class Discount:
    """Entity for the discount."""

    id: UUID = field(default_factory=uuid4)
    type: DiscountType
    code: str | None = None
    description: str = ''
    minimum_order_value: Money = field(default_factory=lambda: Money(0))
    valid_from: datetime = field(default_factory=datetime.now)
    valid_until: datetime | None = None
    max_usage_count: int | None = None
    current_usage_count: int = 0

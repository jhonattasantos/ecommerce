"""Modelo ORM para desconto usando SQLAlchemy."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PgUUID

from .base import Base


class DiscountModel(Base):
    """Modelo ORM para a entidade Discount."""

    __tablename__ = 'discounts'

    id = Column(PgUUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String, nullable=False)  # PERCENTAGE, FIXED_AMOUNT, COUPON
    value = Column(Float, nullable=False)
    code = Column(String, unique=True, nullable=True, index=True)
    description = Column(String, nullable=True)
    minimum_order_value = Column(Float, default=0.0)
    currency = Column(String, default='BRL')
    valid_from = Column(DateTime, default=datetime.now)
    valid_until = Column(DateTime, nullable=True)
    max_usage_count = Column(Integer, nullable=True)
    current_usage_count = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

"""Interface do repositório de descontos."""

from typing import Protocol
from uuid import UUID

from ..entities.discount import Discount


class DiscountRepository(Protocol):
    """Repository for the discount entity."""

    async def get_by_id(self, discount_id: UUID) -> Discount | None:
        """Retorna um desconto pelo seu ID."""
        ...

    async def get_by_code(self, code: str) -> Discount | None:
        """Retorna um desconto pelo seu código."""
        ...

    async def save(self, discount: Discount) -> None:
        """Salva um desconto."""
        ...

    async def delete(self, discount_id: UUID) -> None:
        """Exclui um desconto pelo seu ID."""
        ...

    async def list(self) -> list[Discount]:
        """Lista todos os descontos."""
        ...

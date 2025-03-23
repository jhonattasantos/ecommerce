"""Implementação concreta do repositório de descontos usando SQLAlchemy."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities.discount import Discount, DiscountType
from ....domain.value_objects.money import Money
from ..models.discount_model import DiscountModel


class SQLDiscountRepository:
    """Implementação do repositório de descontos usando SQLAlchemy.

    Esta classe implementa a interface DiscountRepository usando
    SQLAlchemy para persistência em banco de dados SQL.
    """

    def __init__(self, session: AsyncSession):
        """Inicializa o repositório com uma sessão do SQLAlchemy.

        Args:
            session: Sessão assíncrona do SQLAlchemy

        """
        self.session = session

    async def get_by_id(self, discount_id: UUID) -> Discount | None:
        """Busca um desconto pelo seu ID.

        Args:
            discount_id: ID único do desconto

        Returns:
            O desconto encontrado ou None se não existir

        """
        stmt = select(DiscountModel).where(DiscountModel.id == discount_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._map_model_to_entity(model)

    async def get_by_code(self, code: str) -> Discount | None:
        """Busca um desconto pelo seu código (para cupons).

        Args:
            code: Código do cupom/desconto

        Returns:
            O desconto encontrado ou None se não existir

        """
        stmt = select(DiscountModel).where(DiscountModel.code == code)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._map_model_to_entity(model)

    async def save(self, discount: Discount) -> Discount:
        """Persista um desconto no repositório.

        Args:
            discount: Objeto desconto a ser salvo

        Returns:
            O desconto salvo (possivelmente com ID atualizado)

        """
        # Verificar se é uma atualização ou nova inserção
        existing_model = None
        if discount.id:
            stmt = select(DiscountModel).where(DiscountModel.id == discount.id)
            result = await self.session.execute(stmt)
            existing_model = result.scalar_one_or_none()

        if existing_model:
            # Atualizar modelo existente
            existing_model.type = discount.type.name
            existing_model.value = discount.value
            existing_model.code = discount.code
            existing_model.description = discount.description
            existing_model.minimum_order_value = (
                discount.minimum_order_value.amount
            )
            existing_model.currency = discount.minimum_order_value.currency
            existing_model.valid_from = discount.valid_from
            existing_model.valid_until = discount.valid_until
            existing_model.max_usage_count = discount.max_usage_count
            existing_model.current_usage_count = discount.current_usage_count

            await self.session.flush()
            return discount
        else:
            # Criar novo modelo
            model = DiscountModel(
                id=discount.id,
                type=discount.type.name,
                value=discount.value,
                code=discount.code,
                description=discount.description,
                minimum_order_value=discount.minimum_order_value.amount,
                currency=discount.minimum_order_value.currency,
                valid_from=discount.valid_from,
                valid_until=discount.valid_until,
                max_usage_count=discount.max_usage_count,
                current_usage_count=discount.current_usage_count,
            )

            self.session.add(model)
            await self.session.flush()

            # Garantir que o ID do modelo seja propagado para a entidade
            # (relevante somente para novas entidades)
            return discount

    async def delete(self, discount_id: UUID) -> None:
        """Remove um desconto do repositório.

        Args:
            discount_id: ID do desconto a ser removido

        """
        stmt = select(DiscountModel).where(DiscountModel.id == discount_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.flush()

    def _map_model_to_entity(self, model: DiscountModel) -> Discount:
        """Mapeia um modelo ORM para uma entidade de domínio.

        Args:
            model: Modelo ORM do desconto

        Returns:
            Entidade de domínio Discount

        """
        return Discount(
            id=model.id,
            type=DiscountType[model.type],  # Converter string para enum
            value=model.value,
            code=model.code,
            description=model.description,
            minimum_order_value=Money(
                model.minimum_order_value, model.currency
            ),
            valid_from=model.valid_from,
            valid_until=model.valid_until,
            max_usage_count=model.max_usage_count,
            current_usage_count=model.current_usage_count,
        )

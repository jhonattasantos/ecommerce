"""Implementação em memória do repositório de descontos para testes e prototipagem."""  # noqa: D205 E501

from uuid import UUID

from ....domain.entities.discount import Discount


class InMemoryDiscountRepository:
    """Implementação em memória do repositório de descontos.

    Útil para testes unitários, prototipagem ou ambientes de desenvolvimento.
    """

    def __init__(self):
        """Inicializa o repositório com um dicionário em memória."""
        self.discounts: dict[UUID, Discount] = {}
        self.code_index: dict[str, UUID] = {}  # Índice para busca por código

    async def get_by_id(self, discount_id: UUID) -> Discount | None:
        """Busca um desconto pelo seu ID.

        Args:
            discount_id: ID único do desconto

        Returns:
            O desconto encontrado ou None se não existir

        """
        return self.discounts.get(discount_id)

    async def get_by_code(self, code: str) -> Discount | None:
        """Busca um desconto pelo seu código (para cupons).

        Args:
            code: Código do cupom/desconto

        Returns:
            O desconto encontrado ou None se não existir

        """
        discount_id = self.code_index.get(code)
        if discount_id:
            return self.discounts.get(discount_id)
        return None

    async def save(self, discount: Discount) -> Discount:
        """Persista um desconto no repositório.

        Args:
            discount: Objeto desconto a ser salvo

        Returns:
            O desconto salvo

        """
        # Copiar para evitar referências compartilhadas (importante em testes)
        # Em um ambiente real com SQLAlchemy, isso não seria necessário
        import copy

        saved_discount = copy.deepcopy(discount)

        self.discounts[saved_discount.id] = saved_discount

        # Manter índice de códigos atualizado
        if saved_discount.code:
            self.code_index[saved_discount.code] = saved_discount.id

        return saved_discount

    async def delete(self, discount_id: UUID) -> None:
        """Remove um desconto do repositório.

        Args:
            discount_id: ID do desconto a ser removido

        """
        if discount_id in self.discounts:
            discount = self.discounts[discount_id]

            # Remover do índice de códigos
            if discount.code and discount.code in self.code_index:
                del self.code_index[discount.code]

            # Remover do dicionário principal
            del self.discounts[discount_id]

"""Script principal para testar o sistema de descontos via CLI."""

import asyncio
import os
import sys

# Adicionar o diretório raiz ao PYTHONPATH para permitir imports relativos
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from ecommerce.modules.cart.application.use_cases.create_fixed_discount import (  # noqa: E501
    CreateFixedDiscountUseCase,
)
from ecommerce.modules.cart.domain.services.discount_service import (  # noqa: E501
    DiscountService,
)
from ecommerce.modules.cart.infrastructure.db.repositories.memory_discount_repository import (  # noqa: E501
    InMemoryDiscountRepository,
)
from ecommerce.modules.cart.interfaces.cli.discount_cli import DiscountCLI


async def main():
    """Função principal que configura e inicia o programa."""
    # Criar o repositório (usando implementação em memória para este exemplo)
    discount_repository = InMemoryDiscountRepository()

    # Criar o serviço de desconto
    discount_service = DiscountService(discount_repository)

    # Criar o caso de uso
    create_fixed_discount_use_case = CreateFixedDiscountUseCase(
        discount_service
    )

    # Criar a interface de linha de comando
    discount_cli = DiscountCLI(create_fixed_discount_use_case)

    # Executar a CLI
    await discount_cli.run()


if __name__ == '__main__':
    # Executar o loop de eventos asyncio
    asyncio.run(main())

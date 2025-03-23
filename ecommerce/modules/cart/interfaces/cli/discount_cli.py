"""Interface de linha de comando para manipulação de descontos."""

from datetime import datetime, timedelta

from ...application.use_cases.create_fixed_discount import (
    CreateFixedDiscountUseCase,
)
from ...domain.entities.discount import Discount


class DiscountCLI:
    """Interface de linha de comando para interação com descontos."""

    def __init__(
        self, create_fixed_discount_use_case: CreateFixedDiscountUseCase
    ):
        """Inicializa a CLI com os casos de uso necessários.

        Args:
            create_fixed_discount_use_case: Caso de uso para
            criar desconto fixo

        """
        self.create_fixed_discount_use_case = create_fixed_discount_use_case

    async def create_fixed_discount_interactive(self) -> Discount | None:
        """Interface interativa para criar um desconto de valor fixo.

        Returns:
            O desconto criado ou None se cancelado

        """
        print('\n==== Criar Novo Desconto de Valor Fixo ====\n')

        try:
            # Coletar dados do usuário
            code = input('Código do desconto (ex: DESCONTO50): ').strip()

            # Validar código
            if not code:
                print('Erro: Código não pode estar vazio.')
                return None

            # Coletar valor do desconto
            amount_str = input('Valor do desconto (ex: 50.00): ').strip()
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print('Erro: Valor deve ser maior que zero.')
                    return None
            except ValueError:
                print('Erro: Valor inválido. Insira um número válido.')
                return None

            # Descrição
            description = input('Descrição do desconto: ').strip()
            if not description:
                description = f'Desconto de R$ {amount:.2f}'

            # Moeda
            currency = input('Moeda [BRL]: ').strip()
            if not currency:
                currency = 'BRL'

            # Valor mínimo do pedido
            min_value_str = input('Valor mínimo do pedido [0.00]: ').strip()
            min_value = 0.0
            if min_value_str:
                try:
                    min_value = float(min_value_str)
                    if min_value < 0:
                        print('Erro: Valor mínimo não pode ser negativo.')
                        return None
                except ValueError:
                    print('Erro: Valor mínimo inválido. Usando 0.00.')

            # Validade
            days_valid_str = input('Dias de validade [30]: ').strip()
            days_valid = 30
            if days_valid_str:
                try:
                    days_valid = int(days_valid_str)
                except ValueError:
                    print('Erro: Número de dias inválido. Usando 30 dias.')

            valid_until = datetime.now() + timedelta(days=days_valid)

            # Limite de uso
            max_usage_str = input(
                'Limite de uso (deixe em branco para ilimitado): '
            ).strip()
            max_usage = None
            if max_usage_str:
                try:
                    max_usage = int(max_usage_str)
                    if max_usage <= 0:
                        print(
                            'Erro: Limite de uso deve ser maior que zero. '
                            'Usando ilimitado.'
                        )
                        max_usage = None
                except ValueError:
                    print('Erro: Limite de uso inválido. Usando ilimitado.')

            # Confirmar criação
            print('\n---- Resumo do Desconto ----')
            print(f'Código: {code}')
            print(f'Valor: {currency} {amount:.2f}')
            print(f'Descrição: {description}')
            print(f'Valor mínimo do pedido: {currency} {min_value:.2f}')
            print(f'Válido até: {valid_until.strftime("%d/%m/%Y")}')
            print(
                f'Limite de uso: {"Ilimitado" if max_usage is None else max_usage}'  # noqa: E501
            )

            confirm = (
                input('\nConfirma a criação deste desconto? (s/n): ')
                .strip()
                .lower()
            )
            if confirm != 's':
                print('Operação cancelada pelo usuário.')
                return None

            # Criar o desconto usando o caso de uso
            discount = await self.create_fixed_discount_use_case.execute(
                amount=amount,
                code=code,
                description=description,
                currency=currency,
                minimum_order_value=min_value,
                valid_until=valid_until,
                max_usage_count=max_usage,
            )

            print(f'\nDesconto criado com sucesso! ID: {discount.id}')
            return discount

        except ValueError as e:
            print(f'Erro de validação: {str(e)}')
            return None
        except Exception as e:
            print(f'Erro ao criar desconto: {str(e)}')
            return None

    async def run(self):
        """Executa o menu principal da CLI."""
        while True:
            print('\n==== Menu de Descontos ====')
            print('1. Criar novo desconto de valor fixo')
            print('0. Sair')

            choice = input('\nEscolha uma opção: ').strip()

            if choice == '1':
                await self.create_fixed_discount_interactive()
            elif choice == '0':
                print('Saindo do sistema de descontos...')
                break
            else:
                print('Opção inválida. Tente novamente.')

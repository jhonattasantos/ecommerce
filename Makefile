.PHONY: setup run clean test lint format install update

# Define a variável para o Python da versão do Poetry
PYTHON = poetry run python
APP_NAME = ecommerce
RUFF = poetry run ruff

# Configuração inicial do projeto
setup:
	@echo "Configurando o projeto..."
	poetry install
	@echo "Configuração concluída!"

# Limpar arquivos temporários
clean:
	@echo "Limpando arquivos temporários..."
	rm -rf __pycache__
	rm -rf ${APP_NAME}/__pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	@echo "Limpeza concluída!"

# Executar testes
test:
	@echo "Executando testes..."
	poetry run pytest

test-cov:
	@echo "Executando testes com cobertura..."
	$(PYTHON) -m pytest --cov=${APP_NAME} --cov-report=term --cov-report=html
	@echo "Relatório de cobertura gerado em htmlcov/index.html"

# Verificar qualidade do código
format:
	@echo "Formatando código..."
	$(RUFF) format $(APP_NAME)
	$(RUFF) check --fix $(APP_NAME)
	@echo "Formatação concluída!"

lint:
	@echo "Verificando código..."
	$(RUFF) check $(APP_NAME)
	@echo "Verificação concluída!"

# Instalar dependências de desenvolvimento
install-dev:
	@echo "Instalando dependências de desenvolvimento..."
	poetry add --group dev pytest pytest-cov pytest-mock ruff mypy autopep8
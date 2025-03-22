import pytest

def test_exemplo():
    assert 1 + 1 == 2

@pytest.mark.unit
def test_unitario():
    # Teste unitário marcado
    assert True

@pytest.mark.integration
def test_integracao():
    # Teste de integração marcado
    assert True
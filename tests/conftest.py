"""
Configuração global dos testes do Lilica Excel
"""

import os
import sys
import pytest

# Adicionar diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture(autouse=True)
def setup_test_env():
    """Fixture que configura o ambiente de teste"""
    # Configurar variáveis de ambiente para teste
    os.environ["LILICA_TEST_MODE"] = "true"
    yield
    # Limpar variáveis de ambiente após os testes
    os.environ.pop("LILICA_TEST_MODE", None)

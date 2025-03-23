"""
Testes para o módulo processador
"""

import os
import pytest
import pandas as pd
from src.core.processador import ProcessadorPlanilhas


# Fixtures
@pytest.fixture
def processador():
    """Fixture que cria uma instância do ProcessadorPlanilhas"""
    return ProcessadorPlanilhas(
        diretorio_entrada="tests/data/entrada",
        diretorio_saida="tests/data/saida",
        nome_arquivo_saida="test_output.xlsx",
    )


@pytest.fixture
def setup_test_dirs(tmp_path):
    """Fixture que cria diretórios temporários para teste"""
    entrada = tmp_path / "entrada"
    saida = tmp_path / "saida"
    entrada.mkdir()
    saida.mkdir()
    return entrada, saida


# Testes
def test_init_processador(processador):
    """Testa a inicialização do ProcessadorPlanilhas"""
    assert processador.diretorio_entrada == "tests/data/entrada"
    assert processador.diretorio_saida == "tests/data/saida"
    assert processador.nome_arquivo_saida == "test_output.xlsx"
    assert processador.dict_telefones == {}


def test_criar_diretorios_saida(setup_test_dirs):
    """Testa se os diretórios são criados corretamente"""
    entrada, saida = setup_test_dirs
    processador = ProcessadorPlanilhas(
        diretorio_entrada=str(entrada), diretorio_saida=str(saida)
    )
    assert os.path.exists(processador.diretorio_saida)


def test_extrair_clientes_arquivo_vazio(processador, tmp_path):
    """Testa extração de clientes de arquivo vazio"""
    # Criar arquivo Excel vazio para teste
    arquivo = tmp_path / "vazio.xlsx"
    pd.DataFrame().to_excel(str(arquivo), index=False)

    df, clientes = processador.extrair_clientes(str(arquivo))
    assert df is not None
    assert len(clientes) == 0


def test_processar_planilhas_sem_arquivos(processador):
    """Testa processamento sem arquivos de entrada"""
    resultado = processador.processar_planilhas([], "nao_existe.xlsx")
    assert resultado is False

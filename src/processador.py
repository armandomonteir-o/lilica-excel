#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo principal do Lilica Excel

Este módulo contém o ponto de entrada principal do programa e a configuração
dos arquivos a serem processados.
"""

import os
import sys
from typing import List

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.logger import get_logger
from src.utils.performance import monitor_performance
from src.core.processador import ProcessadorPlanilhas


@monitor_performance()
def main():
    """Função principal do programa"""
    logger = get_logger("main")
    logger.info("Iniciando processamento principal")

    # Nomes dos arquivos de entrada
    arquivos_cliente = [
        "Avec SalãoVIP - Sistema de Administração (10).xlsx",
        "Avec SalãoVIP - Sistema de Administração (11).xlsx",
        "Avec SalãoVIP - Sistema de Administração (12).xlsx",
        "Avec SalãoVIP - Sistema de Administração (13).xlsx",
        "Avec SalãoVIP - Sistema de Administração (14).xlsx",
        "Avec SalãoVIP - Sistema de Administração (15).xlsx",
    ]
    arquivo_telefones = "ClientescomTelefone.xlsx"

    # Iniciar processamento
    processador = ProcessadorPlanilhas()
    resultado = processador.processar_planilhas(arquivos_cliente, arquivo_telefones)

    if resultado:
        logger.info("Processamento concluído com sucesso")
    else:
        logger.error("Processamento concluído com falhas")

    return resultado


if __name__ == "__main__":
    main()

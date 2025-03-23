#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface de Linha de Comando (CLI) do DataFinder

Este módulo fornece uma interface de linha de comando para o DataFinder,
permitindo que os usuários executem consultas a partir do terminal.
"""

import argparse
import os
import sys
import logging
from typing import List

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.core.engine import DataFinder

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("DataFinder.CLI")


def parse_arguments() -> argparse.Namespace:
    """
    Analisa os argumentos da linha de comando

    Returns:
        Namespace com os argumentos analisados
    """
    parser = argparse.ArgumentParser(
        description="DataFinder - Ferramenta para consulta em planilhas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python -m src.interfaces.cli --source dados/grande.xlsx --query dados/consulta.xlsx --source-column "Cliente" --query-column "Nome" --output resultados.xlsx
  python -m src.interfaces.cli --source dados/vendas.csv --query dados/clientes.xlsx --source-column "ID" --query-column "Código" --operation equals --output resultados.csv
""",
    )

    # Argumentos obrigatórios
    parser.add_argument(
        "--source", required=True, help="Caminho para a planilha fonte (grande)"
    )
    parser.add_argument(
        "--query", required=True, help="Caminho para a planilha de consulta (pequena)"
    )
    parser.add_argument(
        "--source-column",
        required=True,
        help="Nome da coluna na planilha fonte a ser consultada",
    )
    parser.add_argument(
        "--query-column",
        required=True,
        help="Nome da coluna na planilha de consulta que contém os valores de busca",
    )
    parser.add_argument(
        "--output", required=True, help="Caminho para o arquivo de saída (resultados)"
    )

    # Argumentos opcionais
    parser.add_argument(
        "--operation",
        choices=["equals", "contains", "startswith"],
        default="contains",
        help="Tipo de operação para a consulta (default: contains)",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Comparação considera maiúsculas/minúsculas",
    )
    parser.add_argument(
        "--source-sheet",
        help="Nome da planilha na planilha fonte (para arquivos Excel)",
    )
    parser.add_argument(
        "--query-sheet",
        help="Nome da planilha na planilha de consulta (para arquivos Excel)",
    )
    parser.add_argument(
        "--columns",
        help="Lista de colunas a incluir no resultado (separadas por vírgula)",
    )
    parser.add_argument(
        "--use-xml",
        action="store_true",
        help="Usar extração via XML para planilhas corrompidas",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Mostrar mensagens detalhadas durante a execução",
    )

    return parser.parse_args()


def main():
    """Função principal da interface de linha de comando"""
    # Analisar argumentos da linha de comando
    args = parse_arguments()

    # Configurar nível de logging
    if args.verbose:
        logging.getLogger("DataFinder").setLevel(logging.DEBUG)

    # Criar uma instância do DataFinder
    finder = DataFinder()

    # Carregar dados fonte
    if not finder.load_source_data(
        args.source, sheet_name=args.source_sheet, use_xml_extraction=args.use_xml
    ):
        logger.error(f"Falha ao carregar dados fonte de {args.source}")
        return 1

    # Carregar dados de consulta
    if not finder.load_query_data(args.query, sheet_name=args.query_sheet):
        logger.error(f"Falha ao carregar dados de consulta de {args.query}")
        return 1

    # Adicionar critério de consulta
    finder.add_criteria(
        query_column=args.query_column,
        source_column=args.source_column,
        operation=args.operation,
        case_sensitive=args.case_sensitive,
    )

    # Colunas a incluir no resultado
    columns_to_include = None
    if args.columns:
        columns_to_include = [col.strip() for col in args.columns.split(",")]

    # Executar consulta
    if not finder.execute_query(columns_to_include=columns_to_include):
        logger.error("Falha ao executar consulta")
        return 1

    # Exportar resultados
    if not finder.export_results(args.output):
        logger.error(f"Falha ao exportar resultados para {args.output}")
        return 1

    # Exibir resumo
    summary = finder.get_summary()
    print("\n--- Resumo da Consulta ---")
    print(f"Planilha fonte: {args.source} ({summary['source_data']['rows']} linhas)")
    print(
        f"Planilha de consulta: {args.query} ({summary['query_data']['rows']} linhas)"
    )
    print(f"Coluna fonte: {args.source_column}")
    print(f"Coluna de consulta: {args.query_column}")
    print(f"Operação: {args.operation}")
    print(f"Resultados encontrados: {summary['results']['rows']}")
    print(f"Arquivo de saída: {args.output}")
    print("-------------------------")

    return 0


if __name__ == "__main__":
    sys.exit(main())

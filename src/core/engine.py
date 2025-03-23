#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Motor principal do DataFinder

Este módulo contém a classe principal DataFinder que implementa toda a lógica
de carregamento, consulta e exportação de dados.
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Union, Any, Tuple

# Importando o novo sistema de logs
from src.utils.logger import get_logger

# Obtendo o logger para este módulo
logger = get_logger("core.engine")


class DataFinder:
    """
    Classe principal para consulta de dados em planilhas

    Esta classe implementa a funcionalidade principal do DataFinder, permitindo
    carregar planilhas, definir critérios de consulta e exportar resultados.
    """

    def __init__(self, config: Dict = None):
        """
        Inicializa o DataFinder

        Args:
            config: Dicionário opcional com configurações do DataFinder
        """
        self.config = config or {}
        self.source_data = None  # DataFrame com os dados fonte (planilha grande)
        self.query_data = (
            None  # DataFrame com os critérios de consulta (planilha pequena)
        )
        self.results = None  # DataFrame com os resultados da consulta
        self.criteria = []  # Lista de critérios de consulta
        logger.info("DataFinder inicializado")

    def load_source_data(
        self,
        file_path: str,
        sheet_name: Optional[str] = None,
        use_xml_extraction: bool = False,
    ) -> bool:
        """
        Carrega os dados da planilha fonte (grande)

        Args:
            file_path: Caminho para o arquivo da planilha fonte
            sheet_name: Nome da planilha (sheet) a ser carregada
            use_xml_extraction: Se True, usa extração via XML para planilhas corrompidas

        Returns:
            True se o carregamento foi bem-sucedido, False caso contrário
        """
        try:
            logger.info(f"Carregando dados fonte de {file_path}")

            if not os.path.exists(file_path):
                logger.error(f"Arquivo não encontrado: {file_path}")
                return False

            if use_xml_extraction:
                # TODO: Implementar método para extração via XML
                logger.info("Usando extração via XML")
                # self.source_data = self._extract_from_xml(file_path, sheet_name)
                pass
            else:
                # Identificar o tipo de arquivo pela extensão
                _, ext = os.path.splitext(file_path)
                ext = ext.lower()

                if ext == ".csv":
                    self.source_data = pd.read_csv(file_path)
                elif ext in [".xlsx", ".xls"]:
                    # Verificar se sheet_name é None e tratar adequadamente
                    if sheet_name is None:
                        # Se sheet_name for None, ler apenas a primeira planilha
                        result = pd.read_excel(file_path, sheet_name=0)
                        self.source_data = result
                    else:
                        # Se sheet_name for especificado, ler essa planilha específica
                        result = pd.read_excel(file_path, sheet_name=sheet_name)
                        self.source_data = result
                else:
                    logger.error(f"Formato de arquivo não suportado: {ext}")
                    return False

            logger.info(
                f"Dados fonte carregados: {len(self.source_data)} linhas, "
                f"{len(self.source_data.columns)} colunas"
            )
            return True

        except Exception as e:
            logger.error(f"Erro ao carregar dados fonte: {str(e)}")
            return False

    def load_query_data(self, file_path: str, sheet_name: Optional[str] = None) -> bool:
        """
        Carrega os dados da planilha de consulta (pequena)

        Args:
            file_path: Caminho para o arquivo da planilha de consulta
            sheet_name: Nome da planilha (sheet) a ser carregada

        Returns:
            True se o carregamento foi bem-sucedido, False caso contrário
        """
        try:
            logger.info(f"Carregando dados de consulta de {file_path}")

            if not os.path.exists(file_path):
                logger.error(f"Arquivo não encontrado: {file_path}")
                return False

            # Identificar o tipo de arquivo pela extensão
            _, ext = os.path.splitext(file_path)
            ext = ext.lower()

            if ext == ".csv":
                self.query_data = pd.read_csv(file_path)
            elif ext in [".xlsx", ".xls"]:
                # Verificar se sheet_name é None e tratar adequadamente
                if sheet_name is None:
                    # Se sheet_name for None, ler apenas a primeira planilha
                    result = pd.read_excel(file_path, sheet_name=0)
                    self.query_data = result
                else:
                    # Se sheet_name for especificado, ler essa planilha específica
                    result = pd.read_excel(file_path, sheet_name=sheet_name)
                    self.query_data = result
            else:
                logger.error(f"Formato de arquivo não suportado: {ext}")
                return False

            logger.info(
                f"Dados de consulta carregados: {len(self.query_data)} linhas, "
                f"{len(self.query_data.columns)} colunas"
            )
            return True

        except Exception as e:
            logger.error(f"Erro ao carregar dados de consulta: {str(e)}")
            return False

    def add_criteria(
        self,
        query_column: str,
        source_column: str,
        operation: str = "equals",
        case_sensitive: bool = False,
    ) -> None:
        """
        Adiciona um critério de consulta

        Args:
            query_column: Nome da coluna na planilha de consulta
            source_column: Nome da coluna correspondente na planilha fonte
            operation: Tipo de operação ('equals', 'contains', 'startswith', etc.)
            case_sensitive: Se a comparação deve considerar maiúsculas/minúsculas
        """
        self.criteria.append(
            {
                "query_column": query_column,
                "source_column": source_column,
                "operation": operation,
                "case_sensitive": case_sensitive,
            }
        )
        logger.info(f"Critério adicionado: {query_column} {operation} {source_column}")

    def execute_query(self, columns_to_include: List[str] = None) -> bool:
        """
        Executa a consulta com base nos critérios definidos

        Args:
            columns_to_include: Lista de colunas a incluir no resultado (todas se None)

        Returns:
            True se a consulta foi bem-sucedida, False caso contrário
        """
        if self.source_data is None or self.query_data is None:
            logger.error("Dados fonte ou dados de consulta não carregados")
            return False

        if not self.criteria:
            logger.error("Nenhum critério de consulta definido")
            return False

        try:
            logger.info("Executando consulta...")

            # Criar um DataFrame vazio para os resultados
            self.results = pd.DataFrame()

            # Para cada valor na planilha de consulta, buscar correspondências
            for _, query_row in self.query_data.iterrows():
                # Criar uma máscara vazia (todos False) para a planilha fonte
                mask = pd.Series(True, index=self.source_data.index)

                # Aplicar cada critério de consulta
                for criterion in self.criteria:
                    query_value = query_row[criterion["query_column"]]
                    operation = criterion["operation"]
                    source_column = criterion["source_column"]
                    case_sensitive = criterion["case_sensitive"]

                    # Pular critérios com valores vazios
                    if pd.isna(query_value):
                        continue

                    # Converter para string para operações de texto
                    if isinstance(query_value, (int, float)):
                        query_value = str(query_value)

                    # Aplicar a operação adequada
                    if operation == "equals":
                        if case_sensitive:
                            curr_mask = self.source_data[source_column] == query_value
                        else:
                            curr_mask = (
                                self.source_data[source_column].str.lower()
                                == str(query_value).lower()
                            )
                    elif operation == "contains":
                        if case_sensitive:
                            curr_mask = self.source_data[source_column].str.contains(
                                query_value, na=False
                            )
                        else:
                            curr_mask = self.source_data[source_column].str.contains(
                                query_value, case=False, na=False
                            )
                    elif operation == "startswith":
                        if case_sensitive:
                            curr_mask = self.source_data[source_column].str.startswith(
                                query_value, na=False
                            )
                        else:
                            curr_mask = (
                                self.source_data[source_column]
                                .str.lower()
                                .str.startswith(str(query_value).lower(), na=False)
                            )
                    else:
                        logger.warning(f"Operação não implementada: {operation}")
                        continue

                    # Combinar com a máscara existente (AND lógico)
                    mask = mask & curr_mask

                # Adicionar as linhas que correspondem a todos os critérios
                matching_rows = self.source_data[mask]
                self.results = pd.concat([self.results, matching_rows])

            # Remover duplicatas
            self.results = self.results.drop_duplicates().reset_index(drop=True)

            # Filtrar colunas se especificado
            if columns_to_include:
                columns_to_include = [
                    col for col in columns_to_include if col in self.results.columns
                ]
                self.results = self.results[columns_to_include]

            logger.info(
                f"Consulta concluída: {len(self.results)} resultados encontrados"
            )
            return True

        except Exception as e:
            logger.error(f"Erro ao executar consulta: {str(e)}")
            return False

    def export_results(self, output_path: str, format: str = "xlsx") -> bool:
        """
        Exporta os resultados da consulta para um arquivo

        Args:
            output_path: Caminho para o arquivo de saída
            format: Formato de saída ('xlsx', 'csv', etc.)

        Returns:
            True se a exportação foi bem-sucedida, False caso contrário
        """
        if self.results is None or len(self.results) == 0:
            logger.warning("Nenhum resultado para exportar")
            return False

        try:
            logger.info(f"Exportando {len(self.results)} resultados para {output_path}")

            # Criar o diretório de saída se não existir
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # Exportar no formato especificado
            format = format.lower()
            if format == "xlsx":
                self.results.to_excel(output_path, index=False)
            elif format == "csv":
                self.results.to_csv(output_path, index=False)
            else:
                logger.error(f"Formato de exportação não suportado: {format}")
                return False

            logger.info(f"Resultados exportados com sucesso para {output_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao exportar resultados: {str(e)}")
            return False

    def get_summary(self) -> Dict[str, Any]:
        """
        Retorna um resumo dos dados e resultados

        Returns:
            Dicionário com informações resumidas sobre os dados e resultados
        """
        summary = {
            "source_data": {
                "loaded": self.source_data is not None,
                "rows": len(self.source_data) if self.source_data is not None else 0,
                "columns": (
                    list(self.source_data.columns)
                    if self.source_data is not None
                    else []
                ),
            },
            "query_data": {
                "loaded": self.query_data is not None,
                "rows": len(self.query_data) if self.query_data is not None else 0,
                "columns": (
                    list(self.query_data.columns) if self.query_data is not None else []
                ),
            },
            "criteria": self.criteria,
            "results": {
                "available": self.results is not None,
                "rows": len(self.results) if self.results is not None else 0,
                "columns": (
                    list(self.results.columns) if self.results is not None else []
                ),
            },
        }
        return summary


if __name__ == "__main__":
    # Exemplo de uso da classe DataFinder
    finder = DataFinder()

    # Carregar dados fonte e de consulta
    finder.load_source_data("dados/exemplos/grande.xlsx")
    finder.load_query_data("dados/exemplos/consulta.xlsx")

    # Definir critérios de consulta
    finder.add_criteria(
        query_column="Nome", source_column="Cliente", operation="contains"
    )

    # Executar consulta e exportar resultados
    if finder.execute_query():
        finder.export_results("dados/saida/resultados.xlsx")

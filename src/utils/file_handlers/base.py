#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manipulador de Arquivo Base do DataFinder

Este módulo contém a classe base para manipulação de diferentes formatos de arquivo.
"""

import os
import pandas as pd
from typing import Optional, Union

from src.utils.logger import get_logger

# Obtendo o logger para este módulo
logger = get_logger("utils.file_handlers.base")


class FileHandler:
    """Classe base para manipulação de arquivos"""

    @staticmethod
    def detect_file_type(file_path: str) -> str:
        """
        Detecta o tipo de arquivo com base na extensão

        Args:
            file_path: Caminho para o arquivo

        Returns:
            Tipo de arquivo ('xlsx', 'csv', etc.)
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower().lstrip(".")

    @staticmethod
    def read_file(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Lê um arquivo e retorna um DataFrame

        Args:
            file_path: Caminho para o arquivo
            sheet_name: Nome da planilha (para arquivos Excel)

        Returns:
            DataFrame com os dados do arquivo

        Raises:
            ValueError: Se o formato do arquivo não for suportado
            FileNotFoundError: Se o arquivo não for encontrado
        """
        if not os.path.exists(file_path):
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        file_type = FileHandler.detect_file_type(file_path)
        logger.info(f"Lendo arquivo {file_path} do tipo {file_type}")

        try:
            if file_type == "csv":
                return pd.read_csv(file_path)
            elif file_type in ["xlsx", "xls"]:
                return pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                logger.error(f"Formato de arquivo não suportado: {file_type}")
                raise ValueError(f"Formato de arquivo não suportado: {file_type}")
        except Exception as e:
            logger.error(f"Erro ao ler arquivo {file_path}: {str(e)}")
            raise

    @staticmethod
    def write_file(
        df: pd.DataFrame, output_path: str, sheet_name: Optional[str] = None
    ) -> bool:
        """
        Escreve um DataFrame em um arquivo

        Args:
            df: DataFrame a ser escrito
            output_path: Caminho para o arquivo de saída
            sheet_name: Nome da planilha (para arquivos Excel)

        Returns:
            True se a escrita foi bem-sucedida, False caso contrário
        """
        try:
            # Criar o diretório de saída se não existir
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            file_type = FileHandler.detect_file_type(output_path)
            logger.info(f"Escrevendo arquivo {output_path} do tipo {file_type}")

            if file_type == "csv":
                df.to_csv(output_path, index=False)
            elif file_type in ["xlsx", "xls"]:
                with pd.ExcelWriter(output_path) as writer:
                    df.to_excel(writer, sheet_name=sheet_name or "Sheet1", index=False)
            else:
                logger.error(
                    f"Formato de arquivo não suportado para escrita: {file_type}"
                )
                return False

            logger.info(f"Arquivo {output_path} escrito com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao escrever arquivo {output_path}: {str(e)}")
            return False

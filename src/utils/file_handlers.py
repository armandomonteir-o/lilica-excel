#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Manipuladores de Arquivo do DataFinder

Este módulo contém classes e funções para lidar com diferentes formatos
de arquivo, incluindo a extração de dados de arquivos XML.
"""

import os
import pandas as pd
import zipfile
import shutil
import re
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

# Configuração de logging
logger = logging.getLogger("DataFinder.FileHandlers")


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
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        file_type = FileHandler.detect_file_type(file_path)

        if file_type == "csv":
            return pd.read_csv(file_path)
        elif file_type in ["xlsx", "xls"]:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {file_type}")

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

            return True
        except Exception as e:
            logger.error(f"Erro ao escrever arquivo: {str(e)}")
            return False


class XMLExtractor:
    """Classe para extrair dados de planilhas via XML"""

    def __init__(self):
        """Inicializa o extrator XML"""
        self.temp_dir = "xlsx_extraido"

    def extract_data_from_xlsx(
        self, file_path: str, sheet_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Extrai dados de um arquivo XLSX via XML

        Args:
            file_path: Caminho para o arquivo XLSX
            sheet_name: Nome da planilha (se None, usa a primeira)

        Returns:
            DataFrame com os dados extraídos
        """
        logger.info(f"Extraindo dados de {file_path} via XML")

        # Limpar diretório temporário
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

        try:
            # Extrair conteúdo do XLSX
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(self.temp_dir)

            # Ler o workbook.xml para obter informações sobre as sheets
            workbook_path = os.path.join(self.temp_dir, "xl", "workbook.xml")
            sheet_id = 1  # Default para primeira sheet

            if os.path.exists(workbook_path):
                with open(workbook_path, "r", encoding="utf-8") as f:
                    workbook_content = f.read()

                # Encontrar todas as sheets
                sheet_matches = re.findall(
                    r'<sheet name="([^"]+)"[^>]*sheetId="(\d+)"', workbook_content
                )

                # Se sheet_name foi especificado, encontrar o id correspondente
                if sheet_name and sheet_matches:
                    for name, id in sheet_matches:
                        if name == sheet_name:
                            sheet_id = int(id)
                            break

            # Ler o arquivo sheet{sheet_id}.xml
            sheet_path = os.path.join(
                self.temp_dir, "xl", "worksheets", f"sheet{sheet_id}.xml"
            )

            if not os.path.exists(sheet_path):
                logger.error(f"Arquivo de planilha não encontrado: {sheet_path}")
                return pd.DataFrame()

            with open(sheet_path, "r", encoding="utf-8") as f:
                sheet_content = f.read()

            # Extrair dados usando expressões regulares
            # Encontrar cabeçalhos
            header_match = re.search(r"<row[^>]*>(.*?)</row>", sheet_content)
            headers = []

            if header_match:
                header_row = header_match.group(1)
                header_cells = re.findall(
                    r"<c[^>]*><v>(.*?)</v></c>|<c[^>]*><is><t>(.*?)</t></is></c>",
                    header_row,
                )
                headers = [h[0] or h[1] for h in header_cells]

            # Encontrar dados
            rows = []
            row_matches = re.findall(r"<row[^>]*>(.*?)</row>", sheet_content)

            for row_xml in row_matches[1:]:  # Pular o cabeçalho
                cell_values = re.findall(
                    r"<c[^>]*><v>(.*?)</v></c>|<c[^>]*><is><t>(.*?)</t></is></c>",
                    row_xml,
                )
                row_data = [c[0] or c[1] for c in cell_values]
                rows.append(row_data)

            # Limpar diretório temporário
            shutil.rmtree(self.temp_dir)

            # Criar DataFrame
            df = pd.DataFrame(rows, columns=headers)
            return df

        except Exception as e:
            logger.error(f"Erro ao extrair dados via XML: {str(e)}")
            # Limpar diretório temporário se ocorrer erro
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
            return pd.DataFrame()


# Exemplo de uso
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Exemplo de uso do FileHandler
    try:
        df = FileHandler.read_file("dados/exemplos/exemplo.xlsx")
        print(f"Arquivo lido com sucesso: {len(df)} linhas")
        FileHandler.write_file(df, "dados/saida/copia.xlsx")
    except Exception as e:
        print(f"Erro: {str(e)}")

    # Exemplo de uso do XMLExtractor
    extractor = XMLExtractor()
    df = extractor.extract_data_from_xlsx("dados/exemplos/corrompido.xlsx")
    print(f"Dados extraídos via XML: {len(df)} linhas")

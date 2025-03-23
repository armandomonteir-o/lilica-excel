#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extrator XML do DataFinder

Este módulo contém a classe para extrair dados de planilhas corrompidas via XML.
"""

import os
import re
import zipfile
import shutil
import pandas as pd
from typing import Dict, List, Optional, Tuple

from src.utils.logger import get_logger

# Obtendo o logger para este módulo
logger = get_logger("utils.file_handlers.xml_extractor")


class XMLExtractor:
    """Classe para extrair dados de planilhas via XML"""

    def __init__(self):
        """Inicializa o extrator XML"""
        self.temp_dir = "xlsx_extraido"
        logger.info("XMLExtractor inicializado")

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

                if sheet_matches:
                    logger.info(f"Planilhas encontradas: {sheet_matches}")

                # Se sheet_name foi especificado, encontrar o id correspondente
                if sheet_name and sheet_matches:
                    for name, id in sheet_matches:
                        if name == sheet_name:
                            sheet_id = int(id)
                            logger.info(
                                f"Planilha '{sheet_name}' encontrada com ID {sheet_id}"
                            )
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
                logger.info(f"Cabeçalhos encontrados: {headers}")

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

            logger.info(f"Extraídas {len(rows)} linhas de dados")

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

    def extract_phones_from_xlsx(self, file_path: str) -> Dict[str, str]:
        """
        Extrai números de telefone do arquivo Excel, acessando diretamente o XML interno

        Args:
            file_path: Caminho para o arquivo Excel com os números de telefone

        Returns:
            Dicionário mapeando nomes de clientes (em lowercase) para seus números de telefone
        """
        logger.info(f"Extraindo telefones de {file_path}...")

        # Remover diretório de extração se existir
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

        dict_telefones = {}

        try:
            # Extrair conteúdo do arquivo XLSX (que é um ZIP)
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(self.temp_dir)

            # Ler o arquivo sheet1.xml que contém os dados da planilha
            sheet_path = os.path.join(self.temp_dir, "xl", "worksheets", "sheet1.xml")

            if os.path.exists(sheet_path):
                logger.info("Lendo dados de clientes e telefones do arquivo XML...")

                # Ler o conteúdo do arquivo XML
                with open(sheet_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Padrão para encontrar linhas com dados de cliente e telefone
                pattern = r"<row>.*?<c[^>]*><is><t>(.*?)</t></is></c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>.*?<c[^>]*>(?:<is><t>.*?</t></is>|<v>.*?</v>)</c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>"

                matches = re.findall(pattern, content, re.DOTALL)
                logger.info(
                    f"Encontradas {len(matches)} linhas com dados de cliente e telefone."
                )

                for match in matches:
                    nome = match[0]
                    telefone_fixo = match[3] or match[4] or ""
                    telefone_celular = match[5] or match[6] or ""

                    # Usar o telefone celular se disponível, senão usar o fixo
                    telefone = telefone_celular if telefone_celular else telefone_fixo

                    if nome and telefone:
                        dict_telefones[nome.strip().lower()] = telefone

                logger.info(f"Extraídos {len(dict_telefones)} contatos com telefones.")

                # Se não conseguimos extrair telefones com o padrão acima, tentar um padrão mais simples
                if len(dict_telefones) == 0:
                    dict_telefones = self._extract_phones_alternative_method(content)
            else:
                logger.error(f"O arquivo {sheet_path} não existe.")

        except Exception as e:
            logger.error(f"Erro ao extrair ou analisar o arquivo: {str(e)}")

        # Limpar o diretório de extração
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        return dict_telefones

    def _extract_phones_alternative_method(self, content: str) -> Dict[str, str]:
        """
        Método alternativo para extrair telefones usando um padrão mais simples

        Args:
            content: Conteúdo XML da planilha

        Returns:
            Dicionário mapeando nomes para telefones
        """
        logger.info("Tentando um método alternativo de extração...")
        dict_telefones = {}

        # Extrair manualmente
        rows = content.split("<row>")
        for row in rows[1:]:  # Pular o primeiro elemento que é o cabeçalho XML
            try:
                # Extrair o nome (primeira coluna)
                nome_match = re.search(r"<c[^>]*><is><t>(.*?)</t></is></c>", row)
                if nome_match:
                    nome = nome_match.group(1)

                    # Extrair o telefone celular (quinta coluna)
                    celular_match = re.search(
                        r"<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>",
                        row,
                    )
                    if celular_match:
                        # Pegar o primeiro valor não nulo dos grupos
                        celular = next((g for g in celular_match.groups() if g), "")

                        if nome and celular:
                            dict_telefones[nome.strip().lower()] = celular
            except Exception as e:
                logger.debug(f"Erro ao processar linha: {str(e)}")
                continue

        logger.info(
            f"Extraídos {len(dict_telefones)} contatos com telefones após extração alternativa."
        )
        return dict_telefones

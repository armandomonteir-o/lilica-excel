#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para extração de dados de telefone de arquivos Excel via XML

Este módulo contém funções especializadas para extrair números de telefone
diretamente do conteúdo XML de arquivos Excel, mesmo quando estão corrompidos
ou apresentam problemas de leitura pelos métodos convencionais.
"""

import os
import zipfile
import shutil
import re
from typing import Dict, Optional


def extrair_telefones(arquivo_telefones: str) -> Dict[str, str]:
    """
    Extrai números de telefone do arquivo Excel, acessando diretamente o XML interno

    Args:
        arquivo_telefones: Caminho para o arquivo Excel com os números de telefone

    Returns:
        Dicionário mapeando nomes de clientes (em lowercase) para seus números de telefone
    """
    print(f"Extraindo telefones de {arquivo_telefones}...")

    # Diretório temporário para extração do conteúdo do arquivo XLSX
    diretorio_extracao = "xlsx_extraido"

    # Remover diretório de extração se existir
    if os.path.exists(diretorio_extracao):
        shutil.rmtree(diretorio_extracao)
    os.makedirs(diretorio_extracao)

    dict_telefones = {}

    try:
        # Extrair conteúdo do arquivo XLSX (que é um ZIP)
        with zipfile.ZipFile(arquivo_telefones, "r") as zip_ref:
            zip_ref.extractall(diretorio_extracao)

        # Ler o arquivo sheet1.xml que contém os dados da planilha
        sheet_path = os.path.join(diretorio_extracao, "xl", "worksheets", "sheet1.xml")

        if os.path.exists(sheet_path):
            print("Lendo dados de clientes e telefones do arquivo XML...")

            # Ler o conteúdo do arquivo XML
            with open(sheet_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Padrão para encontrar linhas com dados de cliente e telefone
            pattern = r"<row>.*?<c[^>]*><is><t>(.*?)</t></is></c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>.*?<c[^>]*>(?:<is><t>.*?</t></is>|<v>.*?</v>)</c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>.*?<c[^>]*>(?:<is><t>(.*?)</t></is>|<v>(.*?)</v>)</c>"

            matches = re.findall(pattern, content, re.DOTALL)
            print(f"Encontradas {len(matches)} linhas com dados de cliente e telefone.")

            for match in matches:
                nome = match[0]
                telefone_fixo = match[3] or match[4] or ""
                telefone_celular = match[5] or match[6] or ""

                # Usar o telefone celular se disponível, senão usar o fixo
                telefone = telefone_celular if telefone_celular else telefone_fixo

                if nome and telefone:
                    dict_telefones[nome.strip().lower()] = telefone

            print(f"Extraídos {len(dict_telefones)} contatos com telefones.")

            # Se não conseguimos extrair telefones com o padrão acima, tentar um padrão mais simples
            if len(dict_telefones) == 0:
                dict_telefones = _extrair_telefones_metodo_alternativo(content)
        else:
            print(f"O arquivo {sheet_path} não existe.")

    except Exception as e:
        print(f"Erro ao extrair ou analisar o arquivo: {e}")

    # Limpar o diretório de extração
    if os.path.exists(diretorio_extracao):
        shutil.rmtree(diretorio_extracao)

    return dict_telefones


def _extrair_telefones_metodo_alternativo(content: str) -> Dict[str, str]:
    """
    Método alternativo para extrair telefones usando um padrão mais simples

    Args:
        content: Conteúdo XML da planilha

    Returns:
        Dicionário mapeando nomes para telefones
    """
    print("Tentando um método alternativo de extração...")
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
        except Exception:
            continue

    print(
        f"Extraídos {len(dict_telefones)} contatos com telefones após extração alternativa."
    )
    return dict_telefones

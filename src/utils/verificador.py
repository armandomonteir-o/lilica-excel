#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para verificação e validação de planilhas Excel

Este módulo contém funções para verificar o conteúdo de planilhas Excel,
validar os dados extraídos e gerar relatórios de validação.
"""

import os
import pandas as pd
from typing import Dict, List, Tuple, Optional


def verificar_planilha(
    arquivo: str, mostrar_linhas: int = 5, verificar_telefones: bool = True
) -> Dict:
    """
    Verifica o conteúdo de uma planilha Excel e retorna informações sobre ela

    Args:
        arquivo: Caminho para o arquivo Excel
        mostrar_linhas: Número de linhas a serem mostradas no relatório
        verificar_telefones: Se deve verificar a coluna de telefones

    Returns:
        Dicionário com informações sobre a planilha
    """
    resultados = {
        "arquivo": arquivo,
        "existe": False,
        "erro": None,
        "planilhas": [],
        "dados": {},
    }

    if not os.path.exists(arquivo):
        resultados["erro"] = f"Arquivo {arquivo} não encontrado"
        return resultados

    resultados["existe"] = True

    try:
        # Abrir o arquivo Excel
        xls = pd.ExcelFile(arquivo)
        resultados["planilhas"] = xls.sheet_names

        # Para cada planilha, mostrar informações
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(arquivo, sheet_name=sheet_name)

            info_planilha = {
                "linhas": len(df),
                "colunas": df.columns.tolist(),
                "primeiras_linhas": df.head(mostrar_linhas).to_dict(orient="records"),
            }

            # Verificar quantas linhas têm telefone preenchido
            if verificar_telefones and "Telefone" in df.columns:
                telefones_preenchidos = df["Telefone"].notna().sum()
                info_planilha["telefones_preenchidos"] = telefones_preenchidos
                info_planilha["percentual_preenchido"] = (
                    (telefones_preenchidos / len(df)) * 100 if len(df) > 0 else 0
                )

            resultados["dados"][sheet_name] = info_planilha

    except Exception as e:
        resultados["erro"] = str(e)

    return resultados


def gerar_relatorio_verificacao(
    arquivo: str, diretorio_saida: str = "dados/saida"
) -> str:
    """
    Gera um relatório de verificação em formato texto

    Args:
        arquivo: Caminho para o arquivo Excel a ser verificado
        diretorio_saida: Diretório onde o relatório será salvo

    Returns:
        Caminho para o arquivo de relatório gerado
    """
    resultados = verificar_planilha(arquivo)

    # Garantir que o diretório de saída existe
    os.makedirs(diretorio_saida, exist_ok=True)

    # Nome do arquivo de relatório
    nome_base = os.path.basename(arquivo)
    nome_sem_extensao = os.path.splitext(nome_base)[0]
    arquivo_relatorio = os.path.join(
        diretorio_saida, f"{nome_sem_extensao}_relatorio.txt"
    )

    with open(arquivo_relatorio, "w", encoding="utf-8") as f:
        f.write(f"RELATÓRIO DE VERIFICAÇÃO: {nome_base}\n")
        f.write("=" * 80 + "\n\n")

        if not resultados["existe"]:
            f.write(f"ERRO: {resultados['erro']}\n")
            return arquivo_relatorio

        if resultados["erro"]:
            f.write(
                f"AVISO: Ocorreu um erro durante a verificação: {resultados['erro']}\n\n"
            )

        f.write(f"Planilhas encontradas: {', '.join(resultados['planilhas'])}\n\n")

        for sheet_name, info in resultados["dados"].items():
            f.write(f"PLANILHA: {sheet_name}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de linhas: {info['linhas']}\n")
            f.write(f"Colunas: {', '.join(info['colunas'])}\n")

            if "telefones_preenchidos" in info:
                f.write(
                    f"Telefones preenchidos: {info['telefones_preenchidos']} de {info['linhas']} "
                )
                f.write(f"({info['percentual_preenchido']:.1f}%)\n")

            f.write("\nPrimeiras linhas:\n")
            for i, linha in enumerate(info["primeiras_linhas"]):
                f.write(f"{i+1}. {linha}\n")

            f.write("\n")

    print(f"Relatório de verificação gerado em {arquivo_relatorio}")
    return arquivo_relatorio


if __name__ == "__main__":
    # Exemplo de uso
    arquivo_para_verificar = "dados/saida/Clientes_Com_Telefones.xlsx"
    if os.path.exists(arquivo_para_verificar):
        gerar_relatorio_verificacao(arquivo_para_verificar)
    else:
        print(f"Arquivo {arquivo_para_verificar} não encontrado para verificação.")

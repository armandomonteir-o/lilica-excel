#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gerador de Exemplos para o DataFinder

Este script gera planilhas de exemplo para demonstrar o uso do DataFinder.
"""

import os
import pandas as pd
import numpy as np


def criar_dados_exemplo():
    """
    Cria planilhas de exemplo para demonstração do DataFinder
    """
    print("Gerando planilhas de exemplo...")

    # Garantir que o diretório existe
    os.makedirs("dados/exemplos", exist_ok=True)

    # 1. Planilha grande (fonte)
    # Criar dados fictícios de clientes para uma grande planilha
    np.random.seed(42)  # Para reprodutibilidade

    num_clientes = 1000
    dados_clientes = {
        "ID": range(1, num_clientes + 1),
        "Nome": [f"Cliente {i}" for i in range(1, num_clientes + 1)],
        "Email": [f"cliente{i}@exemplo.com" for i in range(1, num_clientes + 1)],
        "Telefone": [
            f"(99) 9{np.random.randint(1000, 10000)}-{np.random.randint(1000, 10000)}"
            for _ in range(num_clientes)
        ],
        "Cidade": np.random.choice(
            [
                "São Paulo",
                "Rio de Janeiro",
                "Belo Horizonte",
                "Salvador",
                "Brasília",
                "Recife",
                "Fortaleza",
                "Porto Alegre",
            ],
            num_clientes,
        ),
        "UF": np.random.choice(
            ["SP", "RJ", "MG", "BA", "DF", "PE", "CE", "RS"], num_clientes
        ),
        "Valor_Compras": np.random.uniform(100, 5000, num_clientes).round(2),
        "Última_Compra": pd.date_range(
            start="2023-01-01", end="2023-12-31", periods=num_clientes
        )
        .strftime("%Y-%m-%d")
        .tolist(),
        "Status": np.random.choice(
            ["Ativo", "Inativo", "Pendente"], num_clientes, p=[0.7, 0.2, 0.1]
        ),
    }

    df_grande = pd.DataFrame(dados_clientes)
    df_grande.to_excel("dados/exemplos/clientes_grande.xlsx", index=False)

    # 2. Planilha pequena (consulta)
    # Selecionar alguns clientes aleatoriamente para a planilha de consulta
    indices = np.random.choice(range(num_clientes), size=20, replace=False)
    df_consulta = pd.DataFrame(
        {
            "Nome": df_grande.iloc[indices]["Nome"].values,
            "Observação": [
                f"Consulta para o cliente {i+1}" for i in range(len(indices))
            ],
        }
    )
    df_consulta.to_excel("dados/exemplos/consulta_nomes.xlsx", index=False)

    # 3. Outra planilha de consulta por ID
    df_consulta_id = pd.DataFrame(
        {
            "ID": df_grande.iloc[indices]["ID"].values,
            "Prioridade": np.random.choice(
                ["Alta", "Média", "Baixa"], size=len(indices)
            ),
        }
    )
    df_consulta_id.to_excel("dados/exemplos/consulta_ids.xlsx", index=False)

    # 4. Planilha de vendas (exemplo para análise financeira)
    num_vendas = 5000

    # Criar IDs de cliente que existem na planilha grande
    cliente_ids = np.random.choice(df_grande["ID"].values, num_vendas)

    dados_vendas = {
        "Venda_ID": range(1, num_vendas + 1),
        "Cliente_ID": cliente_ids,
        "Produto": np.random.choice(
            ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E"],
            num_vendas,
        ),
        "Quantidade": np.random.randint(1, 10, num_vendas),
        "Valor_Unitario": np.random.uniform(10, 500, num_vendas).round(2),
        "Valor_Total": np.zeros(num_vendas),
        "Data_Venda": pd.date_range(
            start="2023-01-01", end="2023-12-31", periods=num_vendas
        )
        .strftime("%Y-%m-%d")
        .tolist(),
        "Forma_Pagamento": np.random.choice(
            ["Crédito", "Débito", "Boleto", "Pix"], num_vendas
        ),
        "Status_Pagamento": np.random.choice(
            ["Pago", "Pendente", "Cancelado"], num_vendas, p=[0.8, 0.15, 0.05]
        ),
    }

    # Calcular valor total
    for i in range(num_vendas):
        dados_vendas["Valor_Total"][i] = (
            dados_vendas["Quantidade"][i] * dados_vendas["Valor_Unitario"][i]
        )

    df_vendas = pd.DataFrame(dados_vendas)
    df_vendas.to_excel("dados/exemplos/vendas.xlsx", index=False)

    # 5. Planilha de consulta de vendas específicas
    vendas_consulta = np.random.choice(df_vendas["Venda_ID"].values, 30)
    df_consulta_vendas = pd.DataFrame(
        {
            "ID_Venda": vendas_consulta,
            "Motivo": ["Auditoria" for _ in range(len(vendas_consulta))],
        }
    )
    df_consulta_vendas.to_excel("dados/exemplos/consulta_vendas.xlsx", index=False)

    print("Planilhas de exemplo geradas em 'dados/exemplos/':")
    print("- clientes_grande.xlsx: Base com 1.000 clientes")
    print("- consulta_nomes.xlsx: Lista com 20 nomes para consulta")
    print("- consulta_ids.xlsx: Lista com 20 IDs para consulta")
    print("- vendas.xlsx: Base com 5.000 vendas")
    print("- consulta_vendas.xlsx: Lista com 30 IDs de vendas para consulta")
    print("\nVocê pode usar essas planilhas para testar o DataFinder!")


if __name__ == "__main__":
    criar_dados_exemplo()

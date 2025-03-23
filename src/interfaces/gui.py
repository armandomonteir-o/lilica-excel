#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface Gráfica (GUI) do DataFinder usando Streamlit

Este módulo fornece uma interface gráfica web para o DataFinder,
permitindo que os usuários realizem consultas através de um navegador.

Para executar: streamlit run src/interfaces/gui.py
"""

import os
import sys
import io
import pandas as pd
import streamlit as st

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.core.engine import DataFinder

# Configuração da página
st.set_page_config(
    page_title="DataFinder",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inicializar estado da sessão se não existir
if "finder" not in st.session_state:
    st.session_state["finder"] = DataFinder()
    st.session_state["source_data_loaded"] = False
    st.session_state["query_data_loaded"] = False
    st.session_state["results_available"] = False
    st.session_state["operations"] = ["equals", "contains", "startswith"]

finder = st.session_state["finder"]


def main():
    """Função principal da interface gráfica"""
    # Título e descrição
    st.title("🔍 DataFinder")
    st.markdown(
        """
    **Uma ferramenta poderosa para consulta em planilhas**
    
    Carregue suas planilhas, defina critérios de busca e encontre os dados que precisa.
    """
    )

    # Sidebar para configurações
    with st.sidebar:
        st.header("Configurações")
        st.markdown("### Carregar Dados")

        # Upload da planilha fonte
        source_file = st.file_uploader(
            "Carregue a planilha fonte (grande)",
            type=["xlsx", "xls", "csv"],
            key="source_uploader",
        )

        # Upload da planilha de consulta
        query_file = st.file_uploader(
            "Carregue a planilha de consulta (pequena)",
            type=["xlsx", "xls", "csv"],
            key="query_uploader",
        )

        # Opção para usar extração XML
        use_xml = st.checkbox(
            "Usar extração XML (para planilhas corrompidas)", value=False
        )

        # Botão para carregar os dados
        if st.button("Carregar Dados"):
            # Carregar planilha fonte
            if source_file:
                with st.spinner("Carregando planilha fonte..."):
                    # Salvar o arquivo temporariamente
                    source_path = f"dados/entrada/{source_file.name}"
                    os.makedirs(os.path.dirname(source_path), exist_ok=True)
                    with open(source_path, "wb") as f:
                        f.write(source_file.getbuffer())

                    # Carregar no DataFinder
                    success = finder.load_source_data(
                        source_path, use_xml_extraction=use_xml
                    )
                    if success:
                        st.session_state["source_data_loaded"] = True
                        st.success(
                            f"Planilha fonte carregada! ({len(finder.source_data)} linhas)"
                        )
                    else:
                        st.error("Erro ao carregar planilha fonte.")
            else:
                st.warning("Por favor, carregue a planilha fonte.")

            # Carregar planilha de consulta
            if query_file:
                with st.spinner("Carregando planilha de consulta..."):
                    # Salvar o arquivo temporariamente
                    query_path = f"dados/entrada/{query_file.name}"
                    os.makedirs(os.path.dirname(query_path), exist_ok=True)
                    with open(query_path, "wb") as f:
                        f.write(query_file.getbuffer())

                    # Carregar no DataFinder
                    success = finder.load_query_data(query_path)
                    if success:
                        st.session_state["query_data_loaded"] = True
                        st.success(
                            f"Planilha de consulta carregada! ({len(finder.query_data)} linhas)"
                        )
                    else:
                        st.error("Erro ao carregar planilha de consulta.")
            else:
                st.warning("Por favor, carregue a planilha de consulta.")

    # Seção principal
    if st.session_state["source_data_loaded"] and st.session_state["query_data_loaded"]:
        col1, col2 = st.columns(2)

        # Coluna 1: Dados fonte
        with col1:
            st.subheader("Planilha Fonte")
            st.dataframe(finder.source_data.head(10))
            st.text(f"Exibindo 10 de {len(finder.source_data)} linhas")

            # Mostrar colunas disponíveis
            source_columns = list(finder.source_data.columns)
            st.markdown("**Colunas disponíveis:**")
            st.write(", ".join(source_columns))

        # Coluna 2: Dados de consulta
        with col2:
            st.subheader("Planilha de Consulta")
            st.dataframe(finder.query_data.head(10))
            st.text(f"Exibindo 10 de {len(finder.query_data)} linhas")

            # Mostrar colunas disponíveis
            query_columns = list(finder.query_data.columns)
            st.markdown("**Colunas disponíveis:**")
            st.write(", ".join(query_columns))

        # Seção de definição de critérios
        st.header("Definição de Critérios")

        # Formulário para definir critérios
        with st.form(key="criteria_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                query_column = st.selectbox(
                    "Coluna na planilha de consulta:",
                    options=query_columns,
                    help="Coluna que contém os valores a serem buscados",
                )

            with col2:
                operation = st.selectbox(
                    "Operação:",
                    options=st.session_state["operations"],
                    help="Tipo de comparação a ser realizada",
                )

            with col3:
                source_column = st.selectbox(
                    "Coluna na planilha fonte:",
                    options=source_columns,
                    help="Coluna onde os valores serão buscados",
                )

            # Opções adicionais
            col1, col2 = st.columns(2)

            with col1:
                case_sensitive = st.checkbox(
                    "Considerar maiúsculas/minúsculas",
                    value=False,
                    help="Se marcado, 'NOME' será diferente de 'nome'",
                )

            with col2:
                columns_str = st.text_input(
                    "Colunas a incluir no resultado (separadas por vírgula, vazio = todas):",
                    help="Lista de colunas a serem incluídas nos resultados",
                )

            # Botão para executar consulta
            submit_button = st.form_submit_button(label="Executar Consulta")

            if submit_button:
                # Limpar critérios anteriores
                finder.criteria = []

                # Adicionar novo critério
                finder.add_criteria(
                    query_column=query_column,
                    source_column=source_column,
                    operation=operation,
                    case_sensitive=case_sensitive,
                )

                # Colunas a incluir
                columns_to_include = None
                if columns_str:
                    columns_to_include = [col.strip() for col in columns_str.split(",")]

                # Executar consulta
                with st.spinner("Executando consulta..."):
                    success = finder.execute_query(
                        columns_to_include=columns_to_include
                    )

                    if success:
                        st.session_state["results_available"] = True
                        st.success(
                            f"Consulta executada com sucesso! {len(finder.results)} resultados encontrados."
                        )
                    else:
                        st.error("Erro ao executar consulta.")

        # Seção de resultados
        if st.session_state["results_available"]:
            st.header("Resultados")

            # Exibir resultados
            st.dataframe(finder.results)
            st.text(f"Encontrados {len(finder.results)} resultados")

            # Opções para exportar
            col1, col2 = st.columns(2)

            with col1:
                export_format = st.selectbox(
                    "Formato de exportação:", options=["xlsx", "csv"], index=0
                )

            with col2:
                output_name = st.text_input(
                    "Nome do arquivo de saída:", value="resultados"
                )

            # Botão para exportar
            if st.button("Exportar Resultados"):
                with st.spinner("Exportando resultados..."):
                    # Preparar o arquivo para download
                    output_file = f"{output_name}.{export_format}"
                    output_path = f"dados/saida/{output_file}"

                    # Criar o diretório se não existir
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)

                    # Exportar arquivo
                    success = finder.export_results(output_path, format=export_format)

                    if success:
                        # Preparar conteúdo para download
                        with open(output_path, "rb") as f:
                            file_content = f.read()

                        # Criar botão de download
                        st.download_button(
                            label=f"Download {output_file}",
                            data=file_content,
                            file_name=output_file,
                            mime="application/octet-stream",
                        )

                        st.success(f"Resultados exportados para {output_file}")
                    else:
                        st.error("Erro ao exportar resultados.")

    else:
        # Mensagem quando os dados não estão carregados
        st.info(
            "Por favor, carregue as planilhas fonte e de consulta na barra lateral para começar."
        )

        # Mostrar exemplos de uso
        st.subheader("Como usar o DataFinder")
        st.markdown(
            """
        1. Carregue a **planilha fonte** (grande) que contém todos os dados
        2. Carregue a **planilha de consulta** (pequena) com os valores que deseja buscar
        3. Defina os **critérios de busca** selecionando as colunas e a operação
        4. Clique em **Executar Consulta** para buscar os dados
        5. Exporte os resultados para Excel ou CSV
        
        ### Casos de Uso
        
        - **Recursos Humanos**: Encontrar dados de funcionários específicos em uma grande base de dados
        - **Vendas**: Verificar histórico de pedidos de uma lista de clientes
        - **Financeiro**: Buscar transações específicas em um extrato bancário
        - **Marketing**: Filtrar contatos específicos para campanhas direcionadas
        """
        )


if __name__ == "__main__":
    main()

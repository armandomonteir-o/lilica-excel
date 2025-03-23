#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface Simplificada do DataFinder usando Streamlit

Esta versão é otimizada para usuários não técnicos, com instruções claras
e interface simplificada.

Para executar: streamlit run src/interfaces/easy_gui.py
"""

import os
import sys
import pandas as pd
import streamlit as st

# Adicionar o diretório raiz ao path para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.core.engine import DataFinder

# Configuração da página
st.set_page_config(
    page_title="Consulta de Planilhas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/seu-usuario/datafinder",
        "Report a bug": "https://github.com/seu-usuario/datafinder/issues",
        "About": "Ferramenta para consulta e filtro de dados em planilhas",
    },
)

# Configurar tema escuro
st.markdown(
    """
    <script>
        var elements = window.parent.document.querySelectorAll('.stApp');
        elements[0].style.backgroundColor = '#0e1117';
    </script>
    """,
    unsafe_allow_html=True,
)

# Estilo personalizado
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.8rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .step-header {
        font-size: 1.6rem;
        color: #4CACFC;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        background-color: rgba(38, 39, 48, 0.7);
        padding: 12px 15px 12px 25px;
        border-radius: 8px;
        border-left: 5px solid #4CACFC;
    }
    .emoji-icon {
        margin-left: 10px;
        margin-right: 8px;
    }
    .highlight {
        background-color: rgba(38, 39, 48, 0.7);
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffb74d;
        margin-bottom: 1rem;
    }
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        transition: all 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .upload-container {
        border: 2px dashed #4CACFC;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0 20px 0;
        background-color: rgba(38, 39, 48, 0.6);
    }
    .success-box {
        background-color: rgba(0, 128, 0, 0.2);
        color: #98fb98;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 5px solid #00C851;
        margin: 12px 0;
    }
    .error-box {
        background-color: rgba(255, 0, 0, 0.2);
        color: #ffcccb;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 5px solid #ff4444;
        margin: 12px 0;
    }
    .warning-box {
        background-color: rgba(255, 193, 7, 0.2);
        color: #ffffcc;
        padding: 10px 15px;
        border-radius: 8px;
        border-left: 5px solid #ffbb33;
        margin: 12px 0;
    }
    .form-container {
        background-color: rgba(38, 39, 48, 0.5);
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0 25px 0;
        border: 1px solid rgba(66, 67, 77, 0.7);
    }
    .sidebar .stButton>button {
        width: 100%;
    }
    .stDataFrame {
        margin: 10px 0 20px 0;
    }
    .stExpander {
        margin: 10px 0;
    }
    h3 {
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        color: #e0e0e0;
    }
    .stRadio > div {
        padding: 10px 0;
    }
    .stMarkdown p {
        margin-bottom: 10px;
        color: #e0e0e0;
    }
    .streamlit-expanderHeader {
        background-color: rgba(38, 39, 48, 0.7) !important;
        color: #e0e0e0 !important;
    }
    .streamlit-expanderContent {
        background-color: rgba(38, 39, 48, 0.7) !important;
        color: #e0e0e0 !important;
    }
    footer {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .css-18e3th9 {
        padding-top: 0;
        padding-bottom: 0;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
        padding-right: 1rem;
        padding-bottom: 3.5rem;
        padding-left: 1rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Inicializar estado da sessão se não existir
if "finder" not in st.session_state:
    st.session_state["finder"] = DataFinder()
    st.session_state["source_data_loaded"] = False
    st.session_state["query_data_loaded"] = False
    st.session_state["results_available"] = False
    st.session_state["operations"] = ["contains", "equals", "startswith"]
    st.session_state["op_descriptions"] = {
        "contains": "Contém o texto (Ex: buscar 'João' encontra 'Maria João Silva')",
        "equals": "Exatamente igual (Ex: buscar 'João' encontra apenas 'João')",
        "startswith": "Começa com o texto (Ex: buscar 'João' encontra 'João Silva')",
    }

finder = st.session_state["finder"]


def main():
    """Função principal da interface gráfica simplificada"""

    # Título e introdução
    st.markdown(
        '<h1 class="main-header">📊 Consulta de Planilhas</h1>', unsafe_allow_html=True
    )

    st.markdown(
        """
    Esta ferramenta permite encontrar rapidamente informações em planilhas grandes.
    
    **Como funciona**: Você carrega uma planilha grande e uma lista do que quer buscar, 
    a ferramenta encontra todas as correspondências e gera uma nova planilha com os resultados.
    """
    )

    # Guia passo-a-passo na barra lateral
    with st.sidebar:
        st.markdown("## 📋 Guia Rápido")
        st.markdown(
            """
        1. Carregue a planilha grande com todos os dados
        2. Carregue a planilha pequena com os itens que quer buscar
        3. Defina como quer fazer a busca
        4. Veja os resultados e baixe a nova planilha
        """
        )

        st.markdown("---")
        st.markdown("### ❓ Precisa de ajuda?")
        if st.button("📚 Mostrar Instruções Detalhadas"):
            st.session_state["show_help"] = not st.session_state.get("show_help", False)

    # Instruções detalhadas
    if st.session_state.get("show_help", False):
        with st.expander("Instruções Detalhadas", expanded=True):
            st.markdown(
                """
            ### O que cada arquivo deve conter:
            
            **Planilha grande (fonte)**:
            - Todos os seus dados, com várias colunas
            - Exemplo: lista completa de clientes, produtos, etc.
            
            **Planilha pequena (consulta)**:
            - Apenas os itens que você quer encontrar
            - Exemplo: lista de 20 nomes que você quer buscar na grande
            
            ### Como funciona a busca:
            
            1. Você escolhe qual coluna na planilha pequena contém os itens a buscar
            2. Você escolhe qual coluna na planilha grande deve ser pesquisada
            3. Você decide o tipo de comparação (contém, igual, começa com)
            
            ### Dicas:
            - Para nomes, use "contém" para encontrar mesmo quando o nome está incompleto
            - Para códigos ou IDs, use "exatamente igual"
            """
            )

    # Passo 1: Carregar arquivos
    st.markdown(
        '<h2 class="step-header"><span class="emoji-icon">📂</span> Passo 1: Carregar suas planilhas</h2>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Planilha com TODOS os dados (grande)")
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        source_file = st.file_uploader(
            "Esta é sua planilha principal, com todos os registros",
            type=["xlsx", "xls", "csv"],
            key="source_uploader",
            help="Carregue o arquivo que contém todos os seus dados",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Planilha com o que você quer BUSCAR (pequena)")
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        query_file = st.file_uploader(
            "Esta é a planilha com os itens que você quer encontrar",
            type=["xlsx", "xls", "csv"],
            key="query_uploader",
            help="Carregue o arquivo que contém os itens que você quer buscar",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Botão de carregar dados
    if source_file and query_file:
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button(
                "🔄 Carregar Planilhas", type="primary", use_container_width=True
            ):
                with st.spinner("Carregando suas planilhas..."):
                    # Processar planilha fonte
                    try:
                        source_path = f"dados/entrada/{source_file.name}"
                        os.makedirs(os.path.dirname(source_path), exist_ok=True)
                        with open(source_path, "wb") as f:
                            f.write(source_file.getbuffer())

                        success = finder.load_source_data(source_path)
                        if success:
                            st.session_state["source_data_loaded"] = True
                            st.markdown(
                                f'<div class="success-box">✅ Planilha grande carregada! ({len(finder.source_data)} linhas)</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<div class="error-box">❌ Não foi possível carregar a planilha grande.</div>',
                                unsafe_allow_html=True,
                            )
                    except Exception as e:
                        st.markdown(
                            f'<div class="error-box">❌ Erro ao carregar planilha grande: {str(e)}</div>',
                            unsafe_allow_html=True,
                        )

                    # Processar planilha de consulta
                    try:
                        query_path = f"dados/entrada/{query_file.name}"
                        os.makedirs(os.path.dirname(query_path), exist_ok=True)
                        with open(query_path, "wb") as f:
                            f.write(query_file.getbuffer())

                        success = finder.load_query_data(query_path)
                        if success:
                            st.session_state["query_data_loaded"] = True
                            st.markdown(
                                f'<div class="success-box">✅ Planilha de consulta carregada! ({len(finder.query_data)} linhas)</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<div class="error-box">❌ Não foi possível carregar a planilha de consulta.</div>',
                                unsafe_allow_html=True,
                            )
                    except Exception as e:
                        st.markdown(
                            f'<div class="error-box">❌ Erro ao carregar planilha de consulta: {str(e)}</div>',
                            unsafe_allow_html=True,
                        )

    # Se os dados foram carregados, mostrar próximos passos
    if st.session_state["source_data_loaded"] and st.session_state["query_data_loaded"]:
        # Mostrar prévia das planilhas
        st.markdown(
            '<h2 class="step-header"><span class="emoji-icon">👁️</span> Passo 2: Visualizar suas planilhas</h2>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Planilha Grande (primeiras 5 linhas)")
            st.dataframe(finder.source_data.head(5), use_container_width=True)
            st.caption(
                f"Total: {len(finder.source_data)} linhas, {len(finder.source_data.columns)} colunas"
            )

        with col2:
            st.markdown("### Planilha de Consulta (primeiras 5 linhas)")
            st.dataframe(finder.query_data.head(5), use_container_width=True)
            st.caption(
                f"Total: {len(finder.query_data)} linhas, {len(finder.query_data.columns)} colunas"
            )

        # Passo 3: Configurar a consulta
        st.markdown(
            '<h2 class="step-header"><span class="emoji-icon">🔍</span> Passo 3: Configurar sua busca</h2>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        with st.form(key="search_form"):
            st.markdown(
                '<div class="highlight">Defina como você quer buscar os dados:</div>',
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Na planilha PEQUENA (de consulta)")
                query_columns = list(finder.query_data.columns)
                query_column = st.selectbox(
                    "Qual coluna contém os itens que você quer buscar?",
                    options=query_columns,
                    index=0 if query_columns else None,
                    help="Escolha a coluna que contém os valores que você quer encontrar",
                )

            with col2:
                st.markdown("### Na planilha GRANDE (fonte)")
                source_columns = list(finder.source_data.columns)
                source_column = st.selectbox(
                    "Em qual coluna você quer buscar?",
                    options=source_columns,
                    index=0 if source_columns else None,
                    help="Escolha a coluna onde os valores serão buscados",
                )

            # Tipo de busca
            st.markdown("### Como você quer buscar?")
            operation = st.radio(
                "Tipo de correspondência:",
                options=st.session_state["operations"],
                format_func=lambda x: f"{x} - {st.session_state['op_descriptions'][x]}",
                horizontal=True,
            )

            # Opções adicionais
            with st.expander("Opções avançadas (opcional)"):
                case_sensitive = st.checkbox(
                    "Diferenciar maiúsculas e minúsculas?",
                    value=False,
                    help="Se marcado, 'Maria' e 'MARIA' serão considerados diferentes",
                )

                # Seleção de colunas para resultado
                st.markdown("### Quais colunas você quer no resultado?")

                all_columns = st.checkbox("Incluir todas as colunas", value=True)

                if not all_columns:
                    selected_columns = st.multiselect(
                        "Selecione as colunas para incluir no resultado:",
                        options=source_columns,
                        default=source_columns[: min(5, len(source_columns))],
                    )
                else:
                    selected_columns = None

            # Botão para executar consulta
            submit_button = st.form_submit_button(
                label="🔎 Buscar Dados", type="primary", use_container_width=True
            )

            if submit_button:
                with st.spinner("Buscando correspondências..."):
                    # Limpar critérios anteriores
                    finder.criteria = []

                    # Adicionar critério
                    finder.add_criteria(
                        query_column=query_column,
                        source_column=source_column,
                        operation=operation,
                        case_sensitive=case_sensitive,
                    )

                    # Executar consulta
                    success = finder.execute_query(
                        columns_to_include=selected_columns if not all_columns else None
                    )

                    if success:
                        st.session_state["results_available"] = True
                        if len(finder.results) > 0:
                            st.markdown(
                                f'<div class="success-box">✅ Busca concluída! Encontrados {len(finder.results)} resultados.</div>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                f'<div class="warning-box">⚠️ Nenhum resultado encontrado. Tente mudar os critérios de busca.</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.markdown(
                            f'<div class="error-box">❌ Erro ao executar a busca.</div>',
                            unsafe_allow_html=True,
                        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Passo 4: Mostrar resultados
        if st.session_state["results_available"]:
            st.markdown(
                '<h2 class="step-header"><span class="emoji-icon">📊</span> Passo 4: Resultados da busca</h2>',
                unsafe_allow_html=True,
            )

            if len(finder.results) > 0:
                # Exibir resultados
                st.dataframe(finder.results, use_container_width=True)
                st.markdown(
                    f"**Total de resultados encontrados:** {len(finder.results)}"
                )

                # Exportar resultados
                st.markdown("### Baixar resultados")

                col1, col2 = st.columns(2)

                with col1:
                    export_format = st.selectbox(
                        "Formato do arquivo:",
                        options=["Excel (.xlsx)", "CSV (.csv)"],
                        index=0,
                        format_func=lambda x: x,
                    )

                    format_ext = "xlsx" if "Excel" in export_format else "csv"

                with col2:
                    output_name = st.text_input(
                        "Nome do arquivo de saída:", value="resultados_da_busca"
                    )

                col1, col2 = st.columns([2, 1])
                with col1:
                    if st.button(
                        "📥 Gerar arquivo para download",
                        type="primary",
                        use_container_width=True,
                    ):
                        with st.spinner("Preparando arquivo para download..."):
                            # Criar diretório de saída
                            output_file = f"{output_name}.{format_ext}"
                            output_path = f"dados/saida/{output_file}"

                            os.makedirs(os.path.dirname(output_path), exist_ok=True)

                            # Exportar arquivo
                            success = finder.export_results(
                                output_path, format=format_ext
                            )

                            if success:
                                # Preparar para download
                                with open(output_path, "rb") as f:
                                    file_content = f.read()

                                st.download_button(
                                    label=f"📥 Baixar {output_file}",
                                    data=file_content,
                                    file_name=output_file,
                                    mime="application/octet-stream",
                                    use_container_width=True,
                                )

                                st.markdown(
                                    f"<div class=\"success-box\">✅ Arquivo '{output_file}' pronto para download!</div>",
                                    unsafe_allow_html=True,
                                )
                            else:
                                st.markdown(
                                    f'<div class="error-box">❌ Erro ao criar arquivo para download.</div>',
                                    unsafe_allow_html=True,
                                )
            else:
                st.info(
                    "Nenhum resultado encontrado com os critérios atuais. Tente ajustar sua busca."
                )

    # Rodapé com exemplos
    st.markdown("---")
    if not (
        st.session_state["source_data_loaded"] and st.session_state["query_data_loaded"]
    ):
        st.markdown("### 💡 Exemplos de uso")
        st.markdown(
            """
        - **Encontrar clientes específicos** em uma grande lista de clientes
        - **Verificar informações** de produtos específicos em um catálogo
        - **Encontrar transações** específicas em um relatório financeiro
        - **Filtrar contatos** de uma lista grande para uma campanha
        """
        )

        # Opção para usar planilhas de exemplo
        st.markdown("### 🧪 Quer testar com dados de exemplo?")
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button(
                "📋 Usar planilhas de exemplo", type="primary", use_container_width=True
            ):
                try:
                    # Verificar se existem exemplos
                    example_source = "dados/exemplos/clientes_grande.xlsx"
                    example_query = "dados/exemplos/consulta_nomes.xlsx"

                    if os.path.exists(example_source) and os.path.exists(example_query):
                        # Carregar exemplos
                        if finder.load_source_data(
                            example_source
                        ) and finder.load_query_data(example_query):
                            st.session_state["source_data_loaded"] = True
                            st.session_state["query_data_loaded"] = True
                            st.markdown(
                                '<div class="success-box">✅ Planilhas de exemplo carregadas com sucesso!</div>',
                                unsafe_allow_html=True,
                            )
                            st.experimental_rerun()
                        else:
                            st.markdown(
                                '<div class="error-box">❌ Não foi possível carregar as planilhas de exemplo.</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.markdown(
                            '<div class="error-box">❌ Planilhas de exemplo não encontradas.</div>',
                            unsafe_allow_html=True,
                        )
                except Exception as e:
                    st.markdown(
                        f'<div class="error-box">❌ Erro ao carregar exemplos: {str(e)}</div>',
                        unsafe_allow_html=True,
                    )


if __name__ == "__main__":
    main()

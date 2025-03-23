"""
Processador principal do Lilica Excel

Este módulo contém a lógica principal para processar múltiplas planilhas Excel,
extrair números de telefone e mesclar dados em uma nova planilha consolidada.
"""

import os
import pandas as pd
from typing import List, Tuple, Dict, Optional

from src.utils.logger import get_logger
from src.utils.performance import monitor_performance
from src.utils.file_handlers import FileHandler, XMLExtractor


class ProcessadorPlanilhas:
    """Classe para processar planilhas Excel e adicionar telefones"""

    def __init__(
        self,
        diretorio_entrada: str = "dados/entrada",
        diretorio_saida: str = "dados/saida",
        nome_arquivo_saida: str = "Clientes_Com_Telefones.xlsx",
    ):
        """
        Inicializa o processador de planilhas

        Args:
            diretorio_entrada: Diretório onde estão as planilhas de entrada
            diretorio_saida: Diretório onde será salva a planilha processada
            nome_arquivo_saida: Nome do arquivo de saída
        """
        self.logger = get_logger("processador")
        self.logger.info("Inicializando ProcessadorPlanilhas")

        self.diretorio_entrada = diretorio_entrada
        self.diretorio_saida = diretorio_saida
        self.nome_arquivo_saida = nome_arquivo_saida
        self.xml_extractor = XMLExtractor()

        # Certificar-se de que o diretório de saída existe
        os.makedirs(self.diretorio_saida, exist_ok=True)
        self.logger.info(f"Diretório de saída verificado: {self.diretorio_saida}")

        # Dicionário para mapear nomes de clientes para telefones
        self.dict_telefones = {}

    @monitor_performance()
    def extrair_clientes(
        self, arquivo: str
    ) -> Tuple[Optional[pd.DataFrame], List[str]]:
        """
        Extrai nomes de clientes da coluna C de uma planilha

        Args:
            arquivo: Caminho para o arquivo Excel

        Returns:
            Tuple contendo o DataFrame e lista de nomes de clientes
        """
        try:
            self.logger.info(f"Extraindo clientes de {arquivo}")
            caminho_completo = os.path.join(self.diretorio_entrada, arquivo)

            # Usar o pandas diretamente para ler o arquivo Excel
            try:
                df = pd.read_excel(caminho_completo)
                self.logger.info(f"Arquivo {arquivo} lido com sucesso usando pandas")
            except Exception as e:
                self.logger.warning(f"Erro ao ler arquivo com pandas: {str(e)}")
                self.logger.info("Tentando extrair dados usando XMLExtractor...")
                # Se falhar, tenta usar o XMLExtractor para extrair os dados
                df = self.xml_extractor.extract_data_from_xlsx(caminho_completo)

                if df.empty:
                    self.logger.error(f"Não foi possível extrair dados de {arquivo}")
                    return None, []

            # Verificar se a planilha tem pelo menos 3 colunas
            if df.shape[1] < 3:
                self.logger.warning(f"A planilha {arquivo} não tem coluna C")
                return df, []

            # Extrair nomes de clientes da coluna C (índice 2)
            clientes = df.iloc[:, 2].dropna().tolist()
            self.logger.info(f"Extraídos {len(clientes)} clientes de {arquivo}")
            return df, clientes
        except Exception as e:
            self.logger.error(f"Erro ao processar {arquivo}: {str(e)}", exc_info=True)
            return None, []

    @monitor_performance()
    def processar_planilhas(
        self, arquivos_cliente: List[str], arquivo_telefones: str
    ) -> bool:
        """
        Processa as planilhas de clientes e adiciona os telefones

        Args:
            arquivos_cliente: Lista de nomes de arquivos com dados de clientes
            arquivo_telefones: Nome do arquivo com os telefones

        Returns:
            True se o processamento foi bem-sucedido, False caso contrário
        """
        self.logger.info("Iniciando processamento de planilhas")

        # Extrair telefones do arquivo de telefones
        caminho_telefones = os.path.join(self.diretorio_entrada, arquivo_telefones)
        self.logger.info(f"Extraindo telefones de {caminho_telefones}")

        try:
            # Usar o XMLExtractor para extrair os telefones
            self.dict_telefones = self.xml_extractor.extract_phones_from_xlsx(
                caminho_telefones
            )
        except Exception as e:
            self.logger.error(f"Falha ao extrair telefones: {str(e)}", exc_info=True)
            self.dict_telefones = {}

        if not self.dict_telefones:
            self.logger.error(
                "Não foi possível extrair os telefones. Encerrando processamento."
            )
            return False

        self.logger.info(f"Extraídos {len(self.dict_telefones)} contatos com telefones")

        # Processar cada planilha de cliente
        dfs_processados = []
        sheet_names = []

        for idx, arquivo in enumerate(arquivos_cliente):
            self.logger.info(f"Processando {arquivo}...")
            df, clientes = self.extrair_clientes(arquivo)

            if df is not None:
                # Adicionar coluna de telefone
                df["Telefone"] = None

                # Para cada cliente na planilha, buscar o telefone
                telefones_encontrados = 0
                for i, row in df.iterrows():
                    if pd.notna(row.iloc[2]):  # Se há um nome na coluna C
                        try:
                            nome_cliente = str(row.iloc[2]).strip().lower()
                            if nome_cliente in self.dict_telefones:
                                df.at[i, "Telefone"] = self.dict_telefones[nome_cliente]
                                telefones_encontrados += 1
                        except Exception as e:
                            self.logger.debug(f"Erro ao processar linha {i}: {str(e)}")
                            continue

                self.logger.info(
                    f"Encontrados {telefones_encontrados} telefones em {arquivo}"
                )
                dfs_processados.append(df)
                sheet_names.append(f"Planilha{idx+1}")
                self.logger.info(f"Processado {arquivo} com {len(df)} linhas")

        # Salvar as planilhas processadas
        if dfs_processados:
            caminho_saida = os.path.join(self.diretorio_saida, self.nome_arquivo_saida)
            self.logger.info(f"Salvando resultado em {caminho_saida}")

            try:
                # Criar um escritor Excel
                with pd.ExcelWriter(caminho_saida, engine="openpyxl") as writer:
                    for i, df in enumerate(dfs_processados):
                        df.to_excel(writer, sheet_name=sheet_names[i], index=False)

                self.logger.info(f"Arquivo salvo com sucesso: {caminho_saida}")
                return True
            except Exception as e:
                self.logger.error(f"Erro ao salvar arquivo: {str(e)}", exc_info=True)
                return False
        else:
            self.logger.warning("Nenhuma planilha foi processada com sucesso")
            return False

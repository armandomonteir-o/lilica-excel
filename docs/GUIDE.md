# Guia do Usuário - DataFinder

## Introdução

Este guia detalha o uso do DataFinder, uma ferramenta para consulta avançada em planilhas Excel ou CSV. O DataFinder permite buscar e filtrar dados em grandes planilhas a partir de critérios definidos em uma planilha menor de consulta.

## Casos de Uso Comuns

### 1. Consulta de Clientes

Imagine que você tem:

- Uma grande base de dados de clientes com centenas ou milhares de registros
- Uma lista menor com alguns clientes específicos que precisa consultar

O DataFinder permite realizar esta consulta automaticamente, extraindo apenas os dados relevantes.

### 2. Análise Financeira

Cenário:

- Arquivo de extrato bancário ou relatório financeiro com milhares de transações
- Lista de transações específicas que precisa verificar ou auditar

### 3. Gestão de Estoque

Cenário:

- Catálogo completo de produtos com milhares de itens
- Lista de produtos específicos para verificar preços ou disponibilidade

## Usando a Interface de Linha de Comando (CLI)

A interface de linha de comando é ideal para usuários avançados ou para integração com scripts e automações.

### Comando básico:

```bash
python -m src.interfaces.cli --source ARQUIVO_FONTE --query ARQUIVO_CONSULTA --source-column COLUNA_FONTE --query-column COLUNA_CONSULTA --output ARQUIVO_SAIDA
```

### Parâmetros:

| Parâmetro          | Descrição                                      | Obrigatório |
| ------------------ | ---------------------------------------------- | ----------- |
| `--source`         | Caminho para a planilha fonte (grande)         | Sim         |
| `--query`          | Caminho para a planilha de consulta (pequena)  | Sim         |
| `--source-column`  | Nome da coluna na planilha fonte               | Sim         |
| `--query-column`   | Nome da coluna na planilha de consulta         | Sim         |
| `--output`         | Caminho para o arquivo de saída                | Sim         |
| `--operation`      | Tipo de operação: equals, contains, startswith | Não         |
| `--case-sensitive` | Considerar maiúsculas/minúsculas               | Não         |
| `--columns`        | Lista de colunas a incluir no resultado        | Não         |
| `--use-xml`        | Usar extração XML para arquivos corrompidos    | Não         |

### Exemplos:

```bash
# Consulta básica por nome
python -m src.interfaces.cli --source dados/exemplos/clientes_grande.xlsx --query dados/exemplos/consulta_nomes.xlsx --source-column "Nome" --query-column "Nome" --output resultados.xlsx

# Consulta por ID com operação 'equals'
python -m src.interfaces.cli --source dados/exemplos/vendas.xlsx --query dados/exemplos/consulta_vendas.xlsx --source-column "Venda_ID" --query-column "ID_Venda" --operation equals --output resultados_vendas.xlsx

# Consulta com seleção de colunas específicas
python -m src.interfaces.cli --source dados/exemplos/clientes_grande.xlsx --query dados/exemplos/consulta_nomes.xlsx --source-column "Nome" --query-column "Nome" --columns "Nome,Email,Telefone,Valor_Compras" --output resultados_colunas.xlsx
```

## Usando a Interface Gráfica (Streamlit)

A interface gráfica é mais amigável para usuários não técnicos, oferecendo uma experiência visual e interativa.

### Iniciando a Interface:

```bash
streamlit run src/interfaces/gui.py
```

### Passos para Uso:

1. **Carregamento de Dados**:

   - Faça upload da planilha fonte (grande) usando o botão de upload
   - Faça upload da planilha de consulta (pequena)
   - Clique em "Carregar Dados"

2. **Definição de Critérios**:

   - Selecione a coluna na planilha de consulta que contém os valores de busca
   - Escolha a operação (equals, contains, startswith)
   - Selecione a coluna na planilha fonte onde buscar
   - Opcionalmente, marque "Considerar maiúsculas/minúsculas"
   - Opcionalmente, especifique quais colunas incluir no resultado
   - Clique em "Executar Consulta"

3. **Resultados e Exportação**:
   - Visualize os resultados na tabela
   - Selecione o formato de exportação (xlsx ou csv)
   - Digite um nome para o arquivo
   - Clique em "Exportar Resultados"
   - Use o botão de download para baixar o arquivo

## Dicas e Truques

1. **Desempenho com Grandes Planilhas**:

   - Para planilhas muito grandes (>100.000 linhas), considere usar apenas as colunas necessárias para melhorar o desempenho

2. **Planilhas Corrompidas**:

   - Use a opção `--use-xml` na CLI ou "Usar extração XML" na GUI para tentar recuperar dados de arquivos Excel corrompidos

3. **Busca Parcial**:

   - Use a operação "contains" para encontrar correspondências parciais (ex: buscar "João" e encontrar "João Silva")
   - Use "startswith" para encontrar valores que começam com um determinado texto

4. **Múltiplas Consultas**:
   - Para cenários complexos, considere realizar múltiplas consultas sequenciais, refinando os resultados a cada etapa

## Solução de Problemas

| Problema                  | Possível Solução                                                            |
| ------------------------- | --------------------------------------------------------------------------- |
| Erro ao carregar planilha | Verifique se o formato do arquivo é suportado (.xlsx, .xls, .csv)           |
| Coluna não encontrada     | Verifique se o nome da coluna está correto, inclusive maiúsculas/minúsculas |
| Resultado vazio           | Verifique se os valores na planilha de consulta existem na planilha fonte   |
| Erro "Out of Memory"      | Tente usar um arquivo CSV em vez de Excel para grandes conjuntos de dados   |

## Exemplos de Uso Avançado

### Integração em Scripts Python:

```python
from src.core.engine import DataFinder

finder = DataFinder()
finder.load_source_data("minha_planilha_grande.xlsx")
finder.load_query_data("minha_consulta.xlsx")

# Adicionar múltiplos critérios
finder.add_criteria(query_column="Nome", source_column="Cliente", operation="contains")
finder.add_criteria(query_column="Cidade", source_column="Localidade", operation="equals")

# Executar consulta e exportar
finder.execute_query(columns_to_include=["Cliente", "Endereço", "Telefone", "Valor"])
finder.export_results("resultado_consulta.xlsx")
```

### Automação de Consultas Periódicas:

Você pode criar um script que execute o DataFinder automaticamente em intervalos regulares:

```python
import schedule
import time
from src.core.engine import DataFinder

def executar_consulta():
    finder = DataFinder()
    finder.load_source_data("dados_atualizados.xlsx")
    finder.load_query_data("consulta_fixa.xlsx")
    finder.add_criteria(query_column="ID", source_column="Código", operation="equals")
    finder.execute_query()

    # Salvar com timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    finder.export_results(f"resultado_{timestamp}.xlsx")
    print(f"Consulta executada e salva em resultado_{timestamp}.xlsx")

# Executar todos os dias às 8h
schedule.every().day.at("08:00").do(executar_consulta)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Apêndice: Estrutura de Arquivos

O pacote DataFinder tem a seguinte estrutura de arquivos:

```
datafinder/
├── src/                         # Código fonte
│   ├── core/                    # Componentes principais
│   │   └── engine.py            # Motor de busca e processamento
│   ├── interfaces/              # Interfaces de usuário
│   │   ├── cli.py               # Interface de linha de comando
│   │   └── gui.py               # Interface gráfica (Streamlit)
│   └── utils/                   # Utilitários
│       └── file_handlers.py     # Manipulação de diferentes formatos
├── dados/                       # Diretório para armazenar dados
│   ├── entrada/                 # Planilhas de entrada
│   ├── exemplos/                # Exemplos de planilhas
│   └── saida/                   # Resultados das consultas
```

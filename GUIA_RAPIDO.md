# Guia Rápido para Consulta de Planilhas

Olá! Este é um guia simples para usar o programa de consulta de planilhas que eu criei para você. 💖

## Para iniciar o programa:

1. Abra o terminal (cmd)
2. Navegue até a pasta do projeto (comando: `cd caminho/para/lilica-excel`)
3. Digite o comando: `streamlit run src/interfaces/easy_gui.py`
4. O navegador vai abrir automaticamente com a interface

## Como usar:

### Passo 1: Preparar as planilhas

- Você precisará de duas planilhas:
  - **Planilha grande**: com todos os seus dados
  - **Planilha pequena**: só com os itens que você quer encontrar

### Passo 2: Carregar as planilhas

- Clique nos botões de upload para carregar as duas planilhas
- Depois clique em "Carregar Planilhas"

### Passo 3: Configurar a busca

- Escolha qual coluna na planilha pequena contém os itens a buscar
- Escolha qual coluna na planilha grande deve ser pesquisada
- Escolha o tipo de busca:
  - **Contém**: Para encontrar nomes mesmo quando incompletos
  - **Igual**: Para códigos ou IDs que precisam ser exatos
  - **Começa com**: Para prefixos (ex: buscar começo de nomes)

### Passo 4: Ver e baixar resultados

- Visualize os resultados encontrados
- Escolha o formato (Excel ou CSV)
- Escolha um nome para o arquivo
- Clique em "Gerar arquivo para download"
- Clique no botão "Baixar..." que aparecer

## Dicas:

- Use "contém" para buscar nomes de clientes
- Use "igual" para buscar códigos exatos
- Você pode usar os dados de exemplo para testar!

## Em caso de dúvidas:

- Clique no botão "Mostrar Instruções Detalhadas" na barra lateral
- Ou me chame que eu te ajudo! 😊

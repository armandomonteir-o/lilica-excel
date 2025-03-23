# Lilica Excel - Processador de Planilhas com Extração de Dados XML

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Descrição

Lilica Excel é uma solução robusta para processamento de múltiplas planilhas Excel, desenvolvida especialmente para extrair e consolidar dados de clientes e seus telefones, mesmo de arquivos corrompidos.

## 🚀 Download e Instalação

### Para Usuários

1. Acesse a [página de releases](https://github.com/seu-usuario/lilica-excel/releases)
2. Baixe a versão mais recente do executável
3. Extraia o arquivo zip baixado
4. Execute o arquivo `Lilica Excel.exe`

### Para Desenvolvedores

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/lilica-excel.git
cd lilica-excel

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o programa
python lilica_excel.py
```

## 💻 Desenvolvimento

### Estrutura do Projeto

```
lilica-excel/
├── src/                    # Código fonte
│   ├── core/              # Lógica principal
│   ├── interface/         # Interface gráfica
│   └── utils/             # Utilitários
├── tests/                 # Testes automatizados
├── dados/                 # Diretório de dados
│   ├── entrada/          # Planilhas de entrada
│   └── saida/           # Resultados processados
└── docs/                 # Documentação
```

### Comandos Úteis

```bash
# Executar testes
pytest

# Gerar executável
python build_exe.py

# Executar com interface gráfica
python lilica_excel.py
```

## 📊 Funcionalidades

- **Interface Gráfica Intuitiva**: Fácil de usar, sem necessidade de conhecimento técnico
- **Processamento Robusto**: Lida com arquivos corrompidos e diferentes formatos
- **Extração XML**: Recupera dados mesmo de arquivos com problemas
- **Mesclagem Inteligente**: Combina dados de múltiplas fontes automaticamente

## 🔧 Configuração

O programa cria automaticamente a estrutura necessária:

- `dados/entrada/`: Coloque aqui as planilhas a serem processadas
- `dados/saida/`: Os resultados serão salvos aqui

## 📝 Exemplos

Incluímos arquivos de exemplo para você testar:

- `dados/entrada/exemplo_clientes.xlsx`: Exemplo de planilha de clientes
- `dados/entrada/exemplo_telefones.xlsx`: Exemplo de planilha de telefones

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação
- Teste em diferentes sistemas operacionais

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✨ Agradecimentos

- [Pandas](https://pandas.pydata.org/) - Processamento de dados
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Manipulação de Excel
- [PyInstaller](https://www.pyinstaller.org/) - Geração de executável

## �� Suporte

Encontrou um bug? Tem uma sugestão? Por favor, abra uma [issue](https://github.com/seu-usuario/lilica-excel/issues).

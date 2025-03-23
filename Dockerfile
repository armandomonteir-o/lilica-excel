# Use a imagem base do Python com Wine
FROM cdrx/pyinstaller-windows:python3

# Copiar arquivos do projeto
COPY . /src/
WORKDIR /src

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Gerar o executável
RUN pyinstaller --clean --onefile --windowed \
    --icon=assets/icon.ico \
    --name="Lilica Excel" \
    --add-data "README.md:." \
    --add-data "Guia Rápido.md:." \
    lilica_excel.py

# O executável estará em /src/dist/ 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para gerar o executável do Lilica Excel
"""

import os
import sys
import subprocess
import shutil


def main():
    """Função principal para gerar o executável"""
    # Configurar o nome do executável
    nome_exe = "Lilica Excel.exe" if sys.platform == "win32" else "Lilica Excel"

    # Criar diretório dist se não existir
    os.makedirs("dist", exist_ok=True)

    # Configurar comando do PyInstaller
    comando = [
        "pyinstaller",
        "--name",
        "Lilica Excel",
        "--onefile",  # Criar um único arquivo executável
        "--windowed",  # Não mostrar console
        "--clean",  # Limpar cache
        "--add-data",
        "README.md:.",  # Incluir README
        "--icon",
        "assets/icon.ico",  # Ícone do executável
        "lilica_excel.py",  # Script principal
    ]

    # Executar PyInstaller
    print("Gerando executável...")
    subprocess.run(comando, check=True)

    # Criar diretório de distribuição
    dist_dir = "Lilica Excel"
    os.makedirs(dist_dir, exist_ok=True)

    # Copiar executável
    shutil.copy2(os.path.join("dist", nome_exe), os.path.join(dist_dir, nome_exe))

    # Copiar README e outros arquivos importantes
    shutil.copy2("README.md", os.path.join(dist_dir, "README.md"))

    # Criar diretórios necessários
    os.makedirs(os.path.join(dist_dir, "dados", "entrada"), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, "dados", "saida"), exist_ok=True)

    print(f"\nExecutável gerado com sucesso em: {os.path.abspath(dist_dir)}")
    print("\nConteúdo do pacote:")
    for root, dirs, files in os.walk(dist_dir):
        level = root.replace(dist_dir, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")


if __name__ == "__main__":
    main()

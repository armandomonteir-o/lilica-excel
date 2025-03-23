#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="lilica-excel",
    version="1.0.0",
    author="Armando Monteiro",
    author_email="seu.email@exemplo.com",
    description="Sistema para processamento de planilhas Excel e extração de dados de telefone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/lilica-excel",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "lilica-excel=lilica_excel:main",
        ],
    },
    package_data={
        "": ["*.md", "*.txt"],
    },
    scripts=["lilica_excel.py"],
)

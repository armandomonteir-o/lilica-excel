#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pacote de manipuladores de arquivo do DataFinder

Este pacote contém classes e funções para manipular diferentes formatos de arquivo,
incluindo Excel, CSV e XML.
"""

from src.utils.file_handlers.base import FileHandler
from src.utils.file_handlers.xml_extractor import XMLExtractor

__all__ = ["FileHandler", "XMLExtractor"]

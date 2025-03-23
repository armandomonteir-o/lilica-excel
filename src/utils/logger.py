#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de configuração de logger para o DataFinder

Este módulo implementa um sistema de logging centralizado para o projeto DataFinder,
com várias opções de configuração e rotação de logs para melhor diagnóstico de problemas.
"""

import os
import sys
import logging
import logging.handlers
import traceback
from datetime import datetime
from typing import Dict, List, Optional, Union, Any


class LoggerSetup:
    """Configuração e gestão centralizada de logging para o DataFinder"""

    DEFAULT_LOG_LEVEL = logging.INFO
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    # Níveis de log para controle mais granular
    VERBOSE = 15  # Entre INFO e DEBUG

    def __init__(self, app_name: str = "DataFinder"):
        """
        Inicializa o sistema de logging

        Args:
            app_name: Nome da aplicação para o logger raiz
        """
        self.app_name = app_name
        self.log_dir = self._create_log_dir()
        self.loggers = {}

        # Configuração inicial
        self._configure_root_logger()

        # Registrar nível personalizado VERBOSE
        logging.addLevelName(self.VERBOSE, "VERBOSE")

        # Adicionar método para nível VERBOSE a todos os loggers
        logging.Logger.verbose = lambda self, message, *args, **kwargs: self.log(
            LoggerSetup.VERBOSE, message, *args, **kwargs
        )

    def _create_log_dir(self) -> str:
        """Cria o diretório de logs se não existir"""
        log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs"
        )
        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    def _configure_root_logger(self) -> None:
        """Configura o logger raiz da aplicação"""
        # Configurar o logger raiz
        root_logger = logging.getLogger(self.app_name)
        root_logger.setLevel(self.DEFAULT_LOG_LEVEL)

        # Limpar handlers existentes
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter(self.DEFAULT_FORMAT, self.DEFAULT_DATE_FORMAT)
        )
        root_logger.addHandler(console_handler)

        # Handler para arquivo de log geral
        log_file = os.path.join(self.log_dir, f"{self.app_name.lower()}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,  # 5MB por arquivo, mantém 5 backups
        )
        file_handler.setFormatter(
            logging.Formatter(self.DEFAULT_FORMAT, self.DEFAULT_DATE_FORMAT)
        )
        root_logger.addHandler(file_handler)

        # Handler para arquivo de erros
        error_log = os.path.join(self.log_dir, f"{self.app_name.lower()}_error.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_log, maxBytes=2 * 1024 * 1024, backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(
            logging.Formatter(self.DEFAULT_FORMAT, self.DEFAULT_DATE_FORMAT)
        )
        root_logger.addHandler(error_handler)

        self.loggers[self.app_name] = root_logger

    def get_logger(self, name: str) -> logging.Logger:
        """
        Obtém um logger configurado para o módulo especificado

        Args:
            name: Nome do módulo/componente

        Returns:
            Logger configurado para o módulo
        """
        logger_name = f"{self.app_name}.{name}"

        if logger_name in self.loggers:
            return self.loggers[logger_name]

        logger = logging.getLogger(logger_name)
        self.loggers[logger_name] = logger

        return logger

    def enable_debug_mode(self) -> None:
        """Ativa o modo debug para todos os loggers"""
        root_logger = logging.getLogger(self.app_name)
        root_logger.setLevel(logging.DEBUG)

        for handler in root_logger.handlers:
            handler.setLevel(logging.DEBUG)

    def log_exception(
        self, logger: logging.Logger, message: str, exc_info=None
    ) -> None:
        """
        Registra uma exceção com rastreamento (traceback)

        Args:
            logger: Logger a ser usado
            message: Mensagem descritiva
            exc_info: Informações da exceção (opcional)
        """
        if exc_info is None:
            exc_info = sys.exc_info()

        if exc_info[0] is not None:  # Se houver exceção
            tb_lines = traceback.format_exception(*exc_info)
            logger.error(f"{message}\n{''.join(tb_lines)}")
        else:
            logger.error(message)


# Instância global para uso em todo o projeto
logger_setup = LoggerSetup()


# Funções de conveniência para uso em outros módulos
def get_logger(name: str) -> logging.Logger:
    """Obtém um logger configurado pelo nome do módulo"""
    return logger_setup.get_logger(name)


def enable_debug():
    """Ativa o modo debug para todos os loggers"""
    logger_setup.enable_debug_mode()

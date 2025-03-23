#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de monitoramento de performance para o DataFinder

Este módulo fornece ferramentas para medir e registrar o desempenho de
operações críticas no DataFinder.
"""

import time
import functools
from typing import Callable, Any, Dict, List
import pandas as pd
from datetime import datetime

from src.utils.logger import get_logger

logger = get_logger("utils.performance")


class PerformanceMonitor:
    """
    Classe para monitorar e registrar a performance de operações
    """

    def __init__(self):
        self.metrics = []

    def record_metric(
        self, operation: str, duration: float, details: Dict = None
    ) -> None:
        """
        Registra uma métrica de performance

        Args:
            operation: Nome da operação realizada
            duration: Duração em segundos
            details: Detalhes adicionais da operação (opcional)
        """
        metric = {
            "operation": operation,
            "duration": duration,
            "timestamp": datetime.now(),
            "details": details or {},
        }
        self.metrics.append(metric)

        # Log da métrica
        details_str = ", ".join(f"{k}={v}" for k, v in (details or {}).items())
        logger.info(
            f"Performance: {operation} completada em {duration:.4f}s {details_str}"
        )

    def get_metrics(self) -> List[Dict]:
        """Retorna todas as métricas registradas"""
        return self.metrics

    def get_summary(self) -> pd.DataFrame:
        """
        Retorna um resumo das métricas por operação

        Returns:
            DataFrame com médias, mín, máx e contagens de duração por operação
        """
        if not self.metrics:
            return pd.DataFrame()

        df = pd.DataFrame(self.metrics)
        summary = (
            df.groupby("operation")["duration"]
            .agg(["mean", "min", "max", "count"])
            .reset_index()
        )

        return summary


# Instância global para uso em todo o projeto
performance_monitor = PerformanceMonitor()


def monitor_performance(operation_name: str = None):
    """
    Decorador para monitorar a performance de funções

    Args:
        operation_name: Nome da operação (se None, usa o nome da função)

    Returns:
        Decorador configurado
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__

            # Preparar detalhes para registro
            details = {
                "function": func.__name__,
                "module": func.__module__,
            }

            # Adicionar detalhes dos argumentos se forem simples
            for i, arg in enumerate(args):
                if isinstance(arg, (str, int, float, bool)):
                    details[f"arg{i}"] = arg

            for k, v in kwargs.items():
                if isinstance(v, (str, int, float, bool)):
                    details[f"kwarg_{k}"] = v

            # Medir tempo de execução
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                # Medir sucesso
                details["success"] = True
                return result
            except Exception as e:
                # Medir falha
                details["success"] = False
                details["error"] = str(e)
                raise
            finally:
                duration = time.time() - start_time
                performance_monitor.record_metric(op_name, duration, details)

        return wrapper

    return decorator

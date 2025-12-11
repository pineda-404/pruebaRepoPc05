"""
Modelos simples para Release y Metrics
"""
from datetime import datetime


def create_release(version: str, commit: str, metrics: dict = None) -> dict:
    """
    Crea un dict de Release
    
    Args:
        version: Versión del release (ej: v1.0.0)
        commit: Hash del commit
        metrics: Dict con métricas (opcional)
    
    Returns:
        Dict con estructura de release
    """
    return {
        "version": version,
        "commit": commit,
        "timestamp": datetime.now().isoformat(),
        "status": "DESCONOCIDO",
        "metrics": metrics
    }


def create_metrics(error_rate: float, latency_p95: float, throughput: int) -> dict:
    """
    Crea un dict de Metrics
    
    Args:
        error_rate: Tasa de errores (0-1)
        latency_p95: Latencia P95 en ms
        throughput: Requests por segundo
    
    Returns:
        Dict con métricas
    """
    return {
        "error_rate": error_rate,
        "latency_p95": latency_p95,
        "throughput": throughput
    }
"""
Lógica de clasificación de riesgo
"""

# Umbrales hardcodeados (simple)
ERROR_RATE_THRESHOLD = 0.02  # 2%
LATENCY_THRESHOLD = 300      # ms
THROUGHPUT_MIN = 1000        # req/s


def classify_risk(metrics: dict) -> tuple[str, list[str]]:
    """
    Clasifica el riesgo de un release según sus métricas
    
    Args:
        metrics: Dict con error_rate, latency_p95, throughput
    
    Returns:
        Tupla (status, reasons)
        - status: "OK" o "RIESGOSO"
        - reasons: lista de strings con las razones
    """
    reasons = []
    
    error_rate = metrics.get("error_rate", 0)
    latency = metrics.get("latency_p95", 0)
    throughput = metrics.get("throughput", 0)
    
    # Verificar error rate
    if error_rate > ERROR_RATE_THRESHOLD:
        reasons.append(
            f"Error rate muy alto: {error_rate*100:.1f}% (umbral: {ERROR_RATE_THRESHOLD*100}%)"
        )
    
    # Verificar latencia
    if latency > LATENCY_THRESHOLD:
        reasons.append(
            f"Latencia P95 excede umbral: {latency}ms (umbral: {LATENCY_THRESHOLD}ms)"
        )
    
    # Verificar throughput
    if throughput < THROUGHPUT_MIN:
        reasons.append(
            f"Throughput bajo: {throughput} req/s (mínimo: {THROUGHPUT_MIN} req/s)"
        )
    
    # Determinar status
    if len(reasons) == 0:
        return "OK", ["Todas las métricas dentro de los umbrales aceptables"]
    else:
        return "RIESGOSO", reasons
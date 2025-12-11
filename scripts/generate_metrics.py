"""
Script para generar métricas simuladas de releases
Simula datos de error_rate, latency_p95 y throughput
"""
import json
import random
import argparse
from pathlib import Path
from datetime import datetime


def generate_metrics(version: str, quality: str = "normal") -> dict:
    """
    Genera métricas simuladas para un release
    
    Args:
        version: Versión del release (ej: v1.2.0)
        quality: Tipo de métricas a generar
                 - "normal": métricas OK
                 - "risky": métricas problemáticas
                 - "random": aleatorio
    
    Returns:
        Dict con métricas simuladas
    """
    
    if quality == "normal":
        # Métricas dentro de umbrales aceptables
        error_rate = random.uniform(0.001, 0.015)  # 0.1% - 1.5%
        latency_p95 = random.uniform(150, 280)      # 150ms - 280ms
        throughput = random.randint(1000, 2000)     # 1000-2000 req/s
    
    elif quality == "risky":
        # Métricas problemáticas (superan umbrales)
        error_rate = random.uniform(0.025, 0.08)    # 2.5% - 8%
        latency_p95 = random.uniform(350, 600)      # 350ms - 600ms
        throughput = random.randint(50, 90)         # 50-90 req/s (bajo)
    
    else:  # random
        # Puede ser bueno o malo
        if random.random() > 0.7:  # 30% probabilidad de ser riesgoso
            error_rate = random.uniform(0.025, 0.08)
            latency_p95 = random.uniform(350, 600)
            throughput = random.randint(50, 90)
        else:
            error_rate = random.uniform(0.001, 0.015)
            latency_p95 = random.uniform(150, 280)
            throughput = random.randint(1000, 2000)
    
    return {
        "error_rate": round(error_rate, 4),
        "latency_p95": round(latency_p95, 1),
        "throughput": throughput,
        "generated_at": datetime.now().isoformat()
    }


def save_metrics(version: str, metrics: dict, output_dir: str = "app/data/metrics"):
    """
    Guarda métricas en archivo JSON
    
    Args:
        version: Versión del release
        metrics: Dict con métricas
        output_dir: Directorio donde guardar
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filename = output_path / f"metrics-{version}.json"
    
    with open(filename, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Métricas generadas y guardadas en: {filename}")
    return str(filename)


def main():
    parser = argparse.ArgumentParser(
        description="Genera métricas simuladas para un release"
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Versión del release (ej: v1.2.0)"
    )
    parser.add_argument(
        "--quality",
        choices=["normal", "risky", "random"],
        default="random",
        help="Tipo de métricas: normal (OK), risky (problemáticas), random (aleatorio)"
    )
    parser.add_argument(
        "--output",
        default="app/data/metrics",
        help="Directorio de salida"
    )
    
    args = parser.parse_args()
    
    # Generar métricas
    print(f"Generando métricas para release {args.version} (quality: {args.quality})...")
    metrics = generate_metrics(args.version, args.quality)
    
    # Mostrar en consola
    print(f"\nMétricas generadas:")
    print(f"  - Error rate: {metrics['error_rate']*100:.2f}%")
    print(f"  - Latency P95: {metrics['latency_p95']}ms")
    print(f"  - Throughput: {metrics['throughput']} req/s")
    
    # Guardar
    save_metrics(args.version, metrics, args.output)
    
    # Clasificar (para feedback inmediato)
    if metrics['error_rate'] > 0.02 or metrics['latency_p95'] > 300 or metrics['throughput'] < 100:
        print(f"\nEste release sería clasificado como: RIESGOSO")
    else:
        print(f"\nEste release sería clasificado como: OK")


if __name__ == "__main__":
    main()

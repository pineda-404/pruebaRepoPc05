# tests/test_api.py
"""
Tests de los endpoints de la API (refactorizado)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app, releases_db


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    # Limpia la "DB" antes y después de cada test
    releases_db.clear()
    yield
    releases_db.clear()


@pytest.fixture
def create_release(client):
    def _create(payload):
        resp = client.post("/releases", json=payload)
        return resp

    return _create


def test_health_check(client):
    """/health devuelve status healthy"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        (
            {
                "version": "v1.0.0",
                "commit": "abc123",
                "metrics": {
                    "error_rate": 0.005,
                    "latency_p95": 220,
                    "throughput": 1200,
                },
            },
            "OK",
        ),
        (
            {
                "version": "v1.0.1",
                "commit": "def456",
                "metrics": {"error_rate": 0.05, "latency_p95": 500, "throughput": 500},
            },
            "RIESGOSO",
        ),
    ],
)
def test_create_release_varios(client, create_release, payload, expected_status):
    """Crear releases (OK y RIESGOSO) - parametrizado"""
    response = create_release(payload)
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == payload["version"]
    assert data["status"] == expected_status


def test_create_release_duplicate(client, create_release):
    """Crear release duplicado -> 409"""
    payload = {"version": "v1.0.0", "commit": "abc123"}
    response1 = create_release(payload)
    assert response1.status_code == 200
    response2 = create_release(payload)
    assert response2.status_code == 409


def test_list_and_get_release(client, create_release):
    """Listar releases y obtener uno en particular"""
    create_release({"version": "v1.0.0", "commit": "abc"})
    create_release({"version": "v1.0.1", "commit": "def"})

    # listar
    response = client.get("/releases")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # obtener específico
    response = client.get("/releases/v1.0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v1.0.0"


def test_get_release_not_found(client):
    """Obtener release inexistente -> 404"""
    response = client.get("/releases/v99.99.99")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "metrics, expected_status",
    [
        ({"error_rate": 0.05, "latency_p95": 500, "throughput": 500}, "RIESGOSO"),
    ],
)
def test_analyze_release(client, create_release, metrics, expected_status):
    """Analizar release con métricas -> devuelve status esperado"""
    payload = {"version": "v1.0.0", "commit": "abc", "metrics": metrics}
    create_release(payload)

    response = client.get("/analysis/v1.0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == expected_status
    assert len(data["reasons"]) > 0


def test_analyze_release_no_metrics(client, create_release):
    """Analizar release sin métricas -> DESCONOCIDO"""
    create_release({"version": "v1.0.0", "commit": "abc"})
    response = client.get("/analysis/v1.0.0")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DESCONOCIDO"

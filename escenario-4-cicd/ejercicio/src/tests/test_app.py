from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_index_responde_200():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    assert "mensaje" in respuesta.json()


def test_health_devuelve_healthy():
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json()["status"] == "healthy"


def test_version_tiene_formato():
    respuesta = client.get("/version")
    assert respuesta.status_code == 200
    assert "version" in respuesta.json()


def test_suma_correcta():
    respuesta = client.get("/suma/2/3")
    assert respuesta.status_code == 200
    assert respuesta.json()["resultado"] == 5


def test_suma_con_negativos():
    respuesta = client.get("/suma/-5/3")
    assert respuesta.json()["resultado"] == -2


def test_ruta_inexistente_da_404():
    respuesta = client.get("/no-existe")
    assert respuesta.status_code == 404
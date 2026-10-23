from fastapi.testclient import TestClient

from gateway.app.main import app

client = TestClient(app)


def test_inicio_gateway():
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["mensaje"] == "API Gateway de Repart funcionando"
    assert "usuarios" in datos["servicios"]
    assert "repuestos" in datos["servicios"]
    assert "ventas" in datos["servicios"]


def test_microservicio_inexistente():
    respuesta = client.get("/inventado")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Microservicio no encontrado"

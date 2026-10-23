from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from repuestos.app.main import app

client = TestClient(app)


def test_listar_repuestos():
    filas = [
        (1, "Pastillas de freno", "Bajaj", 45000.0, 20)
    ]

    with patch("repuestos.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchall.return_value = filas

        respuesta = client.get("/repuestos")

    assert respuesta.status_code == 200
    assert respuesta.json()[0]["nombre"] == "Pastillas de freno"
    assert respuesta.json()[0]["precio"] == 45000.0
    assert respuesta.json()[0]["cantidad"] == 20


def test_crear_repuesto_valido():
    fila = (2, "Filtro de aceite", "Bajaj", 25000.0, 10)

    with patch("repuestos.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = fila

        respuesta = client.post(
            "/repuestos",
            json={
                "nombre": "Filtro de aceite",
                "marca": "Bajaj",
                "precio": 25000,
                "cantidad": 10,
            },
        )

    assert respuesta.status_code == 201
    assert respuesta.json()["nombre"] == "Filtro de aceite"
    assert respuesta.json()["precio"] == 25000.0


def test_rechazar_precio_cero():
    respuesta = client.post(
        "/repuestos",
        json={
            "nombre": "Filtro",
            "marca": "Bajaj",
            "precio": 0,
            "cantidad": 10,
        },
    )

    assert respuesta.status_code == 422


def test_rechazar_cantidad_negativa():
    respuesta = client.post(
        "/repuestos",
        json={
            "nombre": "Filtro",
            "marca": "Bajaj",
            "precio": 25000,
            "cantidad": -1,
        },
    )

    assert respuesta.status_code == 422


def test_consultar_repuesto_inexistente():
    with patch("repuestos.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = None

        respuesta = client.get("/repuestos/9999")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Repuesto no encontrado"

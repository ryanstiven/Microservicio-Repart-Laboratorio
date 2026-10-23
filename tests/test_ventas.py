
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from ventas.app.main import app

client = TestClient(app)


def test_listar_ventas():
    filas = [
        (1, 1, 1, 2, 45000.0, 90000.0)
    ]

    with patch("ventas.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchall.return_value = filas

        respuesta = client.get("/ventas")

    assert respuesta.status_code == 200
    assert respuesta.json()[0]["id"] == 1
    assert respuesta.json()[0]["total"] == 90000.0


def test_crear_venta_valida():
    fila = (2, 1, 1, 3, 45000.0, 135000.0)

    with patch("ventas.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = fila

        respuesta = client.post(
            "/ventas",
            json={
                "id_usuario": 1,
                "id_repuesto": 1,
                "cantidad": 3,
                "precio_unitario": 45000,
            },
        )

    assert respuesta.status_code == 201
    assert respuesta.json()["cantidad"] == 3
    assert respuesta.json()["total"] == 135000.0


def test_rechazar_cantidad_cero():
    respuesta = client.post(
        "/ventas",
        json={
            "id_usuario": 1,
            "id_repuesto": 1,
            "cantidad": 0,
            "precio_unitario": 45000,
        },
    )

    assert respuesta.status_code == 422


def test_rechazar_precio_cero():
    respuesta = client.post(
        "/ventas",
        json={
            "id_usuario": 1,
            "id_repuesto": 1,
            "cantidad": 2,
            "precio_unitario": 0,
        },
    )

    assert respuesta.status_code == 422


def test_consultar_venta_inexistente():
    with patch("ventas.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = None

        respuesta = client.get("/ventas/9999")

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Venta no encontrada"

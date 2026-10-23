from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from usuarios.app.main import app

client = TestClient(app)


def test_listar_usuarios():
    filas = [
        (1, "Administrador Repart", "admin@repart.com", "admin")
    ]

    with patch("usuarios.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchall.return_value = filas

        respuesta = client.get("/usuarios")

    assert respuesta.status_code == 200
    assert respuesta.json()[0]["nombre"] == "Administrador Repart"
    assert respuesta.json()[0]["rol"] == "admin"


def test_crear_usuario_valido():
    fila = (2, "Vendedor Prueba", "vendedor@repart.com", "vendedor")

    with patch("usuarios.app.main.psycopg.connect") as conectar:
        conexion = MagicMock()
        cursor = MagicMock()
        conectar.return_value.__enter__.return_value = conexion
        conexion.cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = fila

        respuesta = client.post(
            "/usuarios",
            json={
                "nombre": "Vendedor Prueba",
                "correo": "vendedor@repart.com",
                "rol": "vendedor",
            },
        )

    assert respuesta.status_code == 201
    assert respuesta.json()["correo"] == "vendedor@repart.com"
    assert respuesta.json()["rol"] == "vendedor"


def test_rechazar_rol_invalido():
    respuesta = client.post(
        "/usuarios",
        json={
            "nombre": "Usuario Prueba",
            "correo": "prueba@repart.com",
            "rol": "supervisor",
        },
    )

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "El rol debe ser admin o vendedor"


def test_rechazar_nombre_corto():
    respuesta = client.post(
        "/usuarios",
        json={
            "nombre": "A",
            "correo": "prueba@repart.com",
            "rol": "vendedor",
        },
    )

    assert respuesta.status_code == 422

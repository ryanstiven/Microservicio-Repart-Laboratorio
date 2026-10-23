
import os

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Repart - Microservicio de Usuarios",
    description="Gestión de administradores y vendedores",
    version="1.0.0"
)

DATABASE_URL = os.getenv("DATABASE_URL")

class Usuario(BaseModel):
    nombre: str = Field(min_length=2)
    correo: str
    rol: str

@app.get("/")
def inicio():
    return {"mensaje": "Microservicio de usuarios de Repart funcionando"}

@app.get("/usuarios")
def listar_usuarios():
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(150) NOT NULL UNIQUE,
                    rol VARCHAR(20) NOT NULL
                )
            """)
        cur.execute("""
                SELECT id, nombre, correo, rol
                FROM usuarios
                ORDER BY id
            """)
        filas = cur.fetchall()

    return [
        {
            "id": fila[0],
            "nombre": fila[1],
            "correo": fila[2],
            "rol": fila[3]
        }
        for fila in filas
    ]

@app.post("/usuarios", status_code=201)
def crear_usuario(usuario: Usuario):
    if usuario.rol not in ["admin", "vendedor"]:
        raise HTTPException(
            status_code=400,
            detail="El rol debe ser admin o vendedor"
        )

    try:
        with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id SERIAL PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        correo VARCHAR(150) NOT NULL UNIQUE,
                        rol VARCHAR(20) NOT NULL
                    )
                """)
            cur.execute("""
                    INSERT INTO usuarios (nombre, correo, rol)
                    VALUES (%s, %s, %s)
                    RETURNING id, nombre, correo, rol
                """, (usuario.nombre, usuario.correo, usuario.rol))
            fila = cur.fetchone()

        return {
            "id": fila[0],
            "nombre": fila[1],
            "correo": fila[2],
            "rol": fila[3]
        }

    except psycopg.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese correo"
        )

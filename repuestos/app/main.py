
import os

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Repart - Microservicio de Repuestos",
    description="Gestión del inventario de repuestos para motos",
    version="1.0.0"
)

DATABASE_URL = os.getenv("DATABASE_URL")

class Repuesto(BaseModel):
    nombre: str = Field(min_length=2)
    marca: str
    precio: float = Field(gt=0)
    cantidad: int = Field(ge=0)

def crear_tabla():
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS repuestos (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    marca VARCHAR(100) NOT NULL,
                    precio NUMERIC(12, 2) NOT NULL CHECK (precio > 0),
                    cantidad INTEGER NOT NULL CHECK (cantidad >= 0)
                )
            """)

@app.on_event("startup")
def iniciar():
    crear_tabla()

@app.get("/")
def inicio():
    return {"mensaje": "Microservicio de repuestos de Repart funcionando"}

@app.get("/repuestos")
def listar_repuestos():
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                SELECT id, nombre, marca, precio, cantidad
                FROM repuestos
                ORDER BY id
            """)
        filas = cur.fetchall()

    return [
        {
            "id": fila[0],
            "nombre": fila[1],
            "marca": fila[2],
            "precio": float(fila[3]),
            "cantidad": fila[4]
        }
        for fila in filas
    ]

@app.post("/repuestos", status_code=201)
def crear_repuesto(repuesto: Repuesto):
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                INSERT INTO repuestos (nombre, marca, precio, cantidad)
                VALUES (%s, %s, %s, %s)
                RETURNING id, nombre, marca, precio, cantidad
            """, (
            repuesto.nombre,
            repuesto.marca,
            repuesto.precio,
            repuesto.cantidad
        ))
        fila = cur.fetchone()

    return {
        "id": fila[0],
        "nombre": fila[1],
        "marca": fila[2],
        "precio": float(fila[3]),
        "cantidad": fila[4]
    }

@app.get("/repuestos/{repuesto_id}")
def consultar_repuesto(repuesto_id: int):
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                SELECT id, nombre, marca, precio, cantidad
                FROM repuestos
                WHERE id = %s
            """, (repuesto_id,))
        fila = cur.fetchone()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Repuesto no encontrado"
        )

    return {
        "id": fila[0],
        "nombre": fila[1],
        "marca": fila[2],
        "precio": float(fila[3]),
        "cantidad": fila[4]
    }

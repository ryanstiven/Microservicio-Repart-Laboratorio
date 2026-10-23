
import os

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Repart - Microservicio de Ventas",
    description="Registro y consulta de ventas de repuestos para motos",
    version="1.0.0"
)

DATABASE_URL = os.getenv("DATABASE_URL")

class Venta(BaseModel):
    id_usuario: int = Field(gt=0)
    id_repuesto: int = Field(gt=0)
    cantidad: int = Field(gt=0)
    precio_unitario: float = Field(gt=0)

def crear_tabla():
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id SERIAL PRIMARY KEY,
                    id_usuario INTEGER NOT NULL,
                    id_repuesto INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
                    precio_unitario NUMERIC(12, 2) NOT NULL
                        CHECK (precio_unitario > 0),
                    total NUMERIC(12, 2) NOT NULL
                )
            """)

@app.on_event("startup")
def iniciar():
    crear_tabla()

@app.get("/")
def inicio():
    return {"mensaje": "Microservicio de ventas de Repart funcionando"}

@app.get("/ventas")
def listar_ventas():
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                SELECT id, id_usuario, id_repuesto, cantidad,
                       precio_unitario, total
                FROM ventas
                ORDER BY id
            """)
        filas = cur.fetchall()

    return [
        {
            "id": fila[0],
            "id_usuario": fila[1],
            "id_repuesto": fila[2],
            "cantidad": fila[3],
            "precio_unitario": float(fila[4]),
            "total": float(fila[5])
        }
        for fila in filas
    ]

@app.post("/ventas", status_code=201)
def crear_venta(venta: Venta):
    total = venta.cantidad * venta.precio_unitario

    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                INSERT INTO ventas (
                    id_usuario, id_repuesto, cantidad,
                    precio_unitario, total
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, id_usuario, id_repuesto, cantidad,
                          precio_unitario, total
            """, (
            venta.id_usuario,
            venta.id_repuesto,
            venta.cantidad,
            venta.precio_unitario,
            total
        ))
        fila = cur.fetchone()

    return {
        "id": fila[0],
        "id_usuario": fila[1],
        "id_repuesto": fila[2],
        "cantidad": fila[3],
        "precio_unitario": float(fila[4]),
        "total": float(fila[5])
    }

@app.get("/ventas/{venta_id}")
def consultar_venta(venta_id: int):
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        cur.execute("""
                SELECT id, id_usuario, id_repuesto, cantidad,
                       precio_unitario, total
                FROM ventas
                WHERE id = %s
            """, (venta_id,))
        fila = cur.fetchone()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )

    return {
        "id": fila[0],
        "id_usuario": fila[1],
        "id_repuesto": fila[2],
        "cantidad": fila[3],
        "precio_unitario": float(fila[4]),
        "total": float(fila[5])
    }

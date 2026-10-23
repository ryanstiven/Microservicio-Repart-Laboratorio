import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

app = FastAPI(
    title="Repart - API Gateway",
    description="Punto de entrada para los microservicios de Repart",
    version="1.0.0",
)

SERVICIOS = {
    "usuarios": os.getenv("USUARIOS_URL", "http://usuarios:8000"),
    "repuestos": os.getenv("REPUESTOS_URL", "http://repuestos:8001"),
    "ventas": os.getenv("VENTAS_URL", "http://ventas:8002"),
}


@app.get("/")
def inicio():
    return {
        "mensaje": "API Gateway de Repart funcionando",
        "servicios": list(SERVICIOS.keys()),
    }


@app.api_route(
    "/{servicio}/{ruta:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
@app.api_route(
    "/{servicio}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def reenviar(servicio: str, request: Request, ruta: str = ""):
    if servicio not in SERVICIOS:
        return JSONResponse(
            status_code=404,
            content={"detail": "Microservicio no encontrado"},
        )

    url = f"{SERVICIOS[servicio]}/{ruta}"
    if request.url.query:
        url += f"?{request.url.query}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as cliente:
            respuesta = await cliente.request(
                method=request.method,
                url=url,
                content=await request.body(),
                headers={
                    key: value
                    for key, value in request.headers.items()
                    if key.lower() not in {
                        "host",
                        "content-length",
                        "connection",
                    }
                },
            )

        return Response(
            content=respuesta.content,
            status_code=respuesta.status_code,
            headers={
                key: value
                for key, value in respuesta.headers.items()
                if key.lower() not in {
                    "content-length",
                    "transfer-encoding",
                    "connection",
                    "content-encoding",
                }
            },
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=502,
            content={"detail": f"El microservicio {servicio} no está disponible"},
        )

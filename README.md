# Repart Microservicios

Sistema backend para la gestión de usuarios, repuestos y ventas, desarrollado mediante una arquitectura de microservicios. El proyecto utiliza FastAPI para construir las API REST, PostgreSQL para almacenar la información y Docker Compose para ejecutar los servicios y sus bases de datos.

## Tabla de contenido

- [Descripción del proyecto](#descripción-del-proyecto)
- [Arquitectura](#arquitectura)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Servicios y puertos](#servicios-y-puertos)
- [Requisitos previos](#requisitos-previos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Endpoints](#endpoints)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Prueba de carga](#prueba-de-carga)
- [Evidencia](#evidencias)s

## Descripción del proyecto

Repart es una aplicación backend organizada en microservicios independientes que permite gestionar usuarios, repuestos y ventas. Un API Gateway centraliza el acceso a los servicios y facilita la comunicación con las API correspondientes.

El proyecto busca demostrar la separación de responsabilidades, la comunicación entre servicios, el uso de bases de datos independientes, la ejecución mediante contenedores y la aplicación de pruebas automatizadas y de rendimiento.

## Arquitectura

La solución está compuesta por un API Gateway, tres microservicios y tres bases de datos PostgreSQL.



### Componentes principales

- **API Gateway:** punto de entrada para las solicitudes de los clientes. Está disponible en el puerto 8080 y dirige las peticiones a los servicios correspondientes.
- **Servicio de usuarios:** gestiona la información de los usuarios y utiliza su propia base de datos.
- **Servicio de repuestos:** administra los repuestos, sus marcas, precios y cantidades disponibles.
- **Servicio de ventas:** gestiona los registros de ventas y utiliza su propia base de datos.
- **Bases de datos:** cada microservicio dispone de una base de datos PostgreSQL independiente.
- **Docker Compose:** permite levantar y administrar los contenedores de la aplicación.

## Tecnologías utilizadas

- Python
- FastAPI
- PostgreSQL
- Docker y Docker Compose
- Pytest
- Ruff
- Bandit
- Locust
- Git y GitHub

## Servicios y puertos

| Componente                 |       Puerto |
| -------------------------- | -----------: |
| API Gateway                |         8080 |
| Servicio de usuarios       |         8000 |
| Servicio de repuestos      |         8001 |
| Servicio de ventas         |         8002 |
| Interfaz web de Locust     |         8089 |
| Base de datos de usuarios  | 5432 interno |
| Base de datos de repuestos | 5432 interno |
| Base de datos de ventas    | 5432 interno |

Los puertos de PostgreSQL corresponden a los puertos internos de cada contenedor; no implica que estén publicados directamente en el equipo anfitrión.

## Requisitos previos

Antes de ejecutar el proyecto, se necesita:

- Git.
- Docker Desktop con Docker Compose.
- Ubuntu en WSL o una terminal compatible.
- Python y un entorno virtual para ejecutar las pruebas locales.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Dayanna2612/repart-microservicios.git
cd repart-microservicios
```

### 2. Iniciar los contenedores

Con Docker Desktop abierto y funcionando, ejecutar:

```bash
docker compose up -d --build
```

Si se trabaja desde Ubuntu WSL y el comando `docker` no está disponible, puede utilizarse:

```bash
docker.exe compose up -d --build
```

### 3. Verificar los contenedores

```bash
docker.exe ps
```

Los servicios y las bases de datos deben aparecer en ejecución. Las bases de datos cuentan con comprobaciones de estado de salud.

### 4. Verificar el API Gateway

```bash
curl http://localhost:8080/
```

Respuesta esperada:

```json
{
  "mensaje": "API Gateway de Repart funcionando",
  "servicios": ["usuarios", "repuestos", "ventas"]
}
```

### 5. Consultar la documentación de las API

Si cada servicio tiene habilitada la documentación automática de FastAPI, se puede acceder a:

- Gateway: [http://localhost:8080/docs](http://localhost:8080/docs)
- Usuarios: [http://localhost:8000/docs](http://localhost:8000/docs)
- Repuestos: [http://localhost:8001/docs](http://localhost:8001/docs)
- Ventas: [http://localhost:8002/docs](http://localhost:8002/docs)

### 6. Detener los contenedores

```bash
docker.exe compose down
```

Este comando detiene y elimina los contenedores creados por Compose. Los volúmenes persistentes no se eliminan a menos que se indique expresamente.

## Endpoints

Las siguientes rutas se exponen a través del API Gateway.

| Método | Endpoint               | Descripción                             |
| ------ | ---------------------- | --------------------------------------- |
| GET    | `/`                    | Verificar el funcionamiento del Gateway |
| GET    | `/usuarios/usuarios`   | Consultar usuarios                      |
| GET    | `/repuestos/repuestos` | Consultar repuestos                     |
| GET    | `/ventas/ventas`       | Consultar ventas                        |

Ejemplos de consulta:

```bash
curl http://localhost:8080/usuarios/usuarios
curl http://localhost:8080/repuestos/repuestos
curl http://localhost:8080/ventas/ventas
```

Las operaciones adicionales disponibles dependen de las rutas implementadas en cada microservicio.

## Pruebas y calidad

El proyecto incluye pruebas automatizadas para el Gateway y los tres microservicios.

### Ejecutar las pruebas

Activar el entorno virtual y ejecutar:

```bash
source .venv/bin/activate
python -m pytest -v
```

### Revisar la calidad del código

```bash
ruff check .
```

### Analizar posibles problemas de seguridad

```bash
bandit -r gateway usuarios repuestos ventas
```

### Resultados obtenidos

En la ejecución registrada durante el desarrollo se obtuvieron los siguientes resultados:

- **Pytest:** 16 pruebas aprobadas.
- **Ruff:** todas las comprobaciones superadas.
- **Bandit:** no se identificaron problemas en el análisis realizado.

Los resultados corresponden a la ejecución documentada y pueden variar si se modifica el código o el entorno.

## Prueba de carga

Se utiliza Locust para simular solicitudes concurrentes contra el API Gateway y medir el comportamiento de los endpoints.

### Ejecutar Locust

Con el entorno virtual activado:

```bash
locust -f locustfile.py --host http://localhost:8080
```

Abrir en el navegador:

[http://localhost:8089](http://localhost:8089)

Desde la interfaz se pueden configurar los usuarios simulados y la tasa de generación de solicitudes.

### Resultados registrados

En una ejecución de prueba se obtuvieron estas métricas:

| Métrica                   | Resultado |
| ------------------------- | --------: |
| Solicitudes totales       |     1.531 |
| Solicitudes fallidas      |         0 |
| Tasa de fallos            |       0 % |
| Tiempo medio de respuesta |  30,55 ms |
| Mediana                   |     34 ms |
| Percentil 95 (P95)        |     60 ms |
| Percentil 99 (P99)        |     95 ms |
| Tiempo máximo registrado  |    366 ms |
| Solicitudes por segundo   |      12,8 |

Estos resultados corresponden a la ejecución registrada; el rendimiento puede variar según el hardware, la configuración y la carga aplicada.

## Evidencias

En la carpeta `evidencias/` se encuentran los archivos relacionados con la validación del proyecto:

- `calidad.txt`: resultados de las pruebas automatizadas y herramientas de calidad.
- `demo_en_vivo.txt`: evidencia de las consultas y respuestas de los servicios.
- `locust_resultados.txt`: resumen textual de las métricas de la prueba de carga.
- `locust_resultados.png`: captura de los resultados obtenidos en Locust.

El diagrama general de la arquitectura está disponible en el archivo `diagrama_arquitectura_repart.png`, ubicado en la raíz del repositorio.



Repositorio: [https://github.com/Dayanna2612/repart-microservicios](https://github.com/Dayanna2612/repart-microservicios)
# Microservicio-Repart-Laboratorio


from locust import HttpUser, task, between


class RepartGatewayUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def consultar_inicio(self):
        self.client.get("/", name="Gateway - inicio")

    @task(2)
    def consultar_usuarios(self):
        self.client.get("/usuarios/usuarios", name="Usuarios - listar")

    @task(2)
    def consultar_repuestos(self):
        self.client.get("/repuestos/repuestos", name="Repuestos - listar")

    @task(2)
    def consultar_ventas(self):
        self.client.get("/ventas/ventas", name="Ventas - listar")

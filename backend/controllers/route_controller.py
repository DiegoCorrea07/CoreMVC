
class RouteController:
    """
    Controlador para orquestar las operaciones de las Rutas geográficas.
    Recibe un repositorio a través de inyección de dependencias.
    """

    # 1. Creamos un constructor que RECIBE el repositorio.
    def __init__(self, repository):
        self.repository = repository

    # 2. Quitamos @staticmethod y usamos 'self' para acceder al repositorio.
    def create_route(self, origen, destino, distancia):
        # La lógica de negocio, como validar los datos, vive en el controlador.
        if int(distancia) <= 0:
            raise ValueError("La distancia debe ser un número positivo.")
        if origen.strip().lower() == destino.strip().lower():
            raise ValueError("El origen y el destino no pueden ser iguales.")

        # 3. Usamos la instancia del repositorio que recibimos.
        return self.repository.create(origen, destino, distancia)

    def get_route(self, route_id):
        return self.repository.get_by_id(route_id)

    def list_routes(self):
        return self.repository.get_all()

    def delete_route(self, route_id):
        return self.repository.delete(route_id)

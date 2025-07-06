from backend.models.route import Route

class RouteRepository:
    """
    Repositorio para gestionar las operaciones de la base de datos para las Rutas geográficas.
    Los métodos son de instancia para permitir la Inyección de Dependencias.
    """

    # SE ELIMINA @staticmethod
    def create(self, origen, destino, distancia):
        return Route.create(origen=origen, destino=destino, distancia=distancia)

    # SE ELIMINA @staticmethod
    def get_by_id(self, route_id):
        return Route.get_or_none(Route.id == route_id)

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(Route.select())

    def update(self, route_id, **kwargs):
        allowed_fields = ['origen', 'destino', 'distancia']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}

        query = Route.update(**update_data).where(Route.id == route_id)
        rows_updated = query.execute()
        return rows_updated > 0

    # SE ELIMINA @staticmethod
    def delete(self, route_id):
        route = Route.get_or_none(Route.id == route_id)
        if route:
            route.delete_instance()
            return True
        return False


from backend.models.route import Route

class RouteRepository:
    @staticmethod
    def create(origen, destino, distancia):
        return Route.create(origen=origen, destino=destino, distancia=distancia)

    @staticmethod
    def get_by_id(route_id):
        return Route.get_or_none(Route.id == route_id)

    @staticmethod
    def get_all():
        return list(Route.select())

    @staticmethod
    def delete(route_id):
        route = Route.get_or_none(Route.id == route_id)
        if route:
            route.delete_instance()
            return True
        return False

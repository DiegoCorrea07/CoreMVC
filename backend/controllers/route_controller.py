
from backend.repositories.route_repository import RouteRepository

class RouteController:
    @staticmethod
    def create_route(origen, destino, distancia):
        return RouteRepository.create(origen, destino, distancia)

    @staticmethod
    def get_route(route_id):
        return RouteRepository.get_by_id(route_id)

    @staticmethod
    def list_routes():
        return RouteRepository.get_all()

    @staticmethod
    def delete_route(route_id):
        return RouteRepository.delete(route_id)

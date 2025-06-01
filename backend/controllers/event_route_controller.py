from backend.repositories.event_route_repository import EventRouteRepository
from backend.models.event_route import EventRoute

class EventRouteController:
    @staticmethod
    def create_event_route(ruta_id, evento_id, demanda_estimada):
        existing = EventRouteRepository.get_by_route_and_event(ruta_id, evento_id)
        if existing:
            raise ValueError("Esta ruta ya está asignada a este evento.")
        return EventRouteRepository.create(ruta_id, evento_id, demanda_estimada)

    @staticmethod
    def get_event_route(event_route_id):
        return EventRouteRepository.get_by_id(event_route_id)

    @staticmethod
    def list_event_routes():
        return EventRouteRepository.get_all()

    @staticmethod
    def delete_event_route(event_route_id):
        return EventRouteRepository.delete(event_route_id)

    @staticmethod
    def update_event_route(event_route_id, demanda_estimada):
        event_route = EventRouteRepository.get_by_id(event_route_id)
        if not event_route:
            raise ValueError("Ruta de Evento no encontrada.")
        event_route.demanda_estimada = demanda_estimada
        event_route.save()
        return event_route

from backend.repositories.event_repository import EventRepository

class EventController:
    @staticmethod
    def create_event(codigo_evento, nombre_evento, descripcion, fecha_inicio, fecha_fin):
        return EventRepository.create(
            codigo_evento, nombre_evento, descripcion, fecha_inicio, fecha_fin
        )

    @staticmethod
    def get_event(event_id):
        return EventRepository.get_by_id(event_id)

    @staticmethod
    def list_events():
        return EventRepository.get_all()

    @staticmethod
    def delete_event(event_id):
        return EventRepository.delete(event_id)

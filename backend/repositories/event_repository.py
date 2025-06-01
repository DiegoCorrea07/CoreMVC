from backend.models.event import Event

class EventRepository:
    @staticmethod
    def create(codigo_evento, nombre_evento, descripcion, fecha_inicio, fecha_fin):
        return Event.create(
            codigo_evento=codigo_evento,
            nombre_evento=nombre_evento,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    @staticmethod
    def get_by_id(event_id):
        return Event.get_or_none(Event.id == event_id)

    @staticmethod
    def get_all():
        return list(Event.select())

    @staticmethod
    def delete(event_id):
        event = Event.get_or_none(Event.id == event_id)
        if event:
            event.delete_instance()
            return True
        return False

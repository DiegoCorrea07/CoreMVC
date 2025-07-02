from backend.models.event import Event

class EventRepository:
    """
    Repositorio para gestionar las operaciones de la base de datos para los Eventos.
    Los métodos son de instancia para permitir la Inyección de Dependencias.
    """

    # SE ELIMINA @staticmethod
    def create(self, codigo_evento, nombre_evento, descripcion, pais_evento, fecha_inicio, fecha_fin):
        return Event.create(
            codigo_evento=codigo_evento,
            nombre_evento=nombre_evento,
            descripcion=descripcion,
            pais_evento=pais_evento,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    # SE ELIMINA @staticmethod
    def get_by_id(self, event_id):
        return Event.get_or_none(Event.id == event_id)

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(Event.select())

    # SE ELIMINA @staticmethod
    def update(self, event_id, **kwargs):
        event = Event.get_or_none(Event.id == event_id)
        if event:
            # Esta lógica para actualizar campos dinámicamente es muy buena.
            for key, value in kwargs.items():
                setattr(event, key, value)
            event.save()
            return event
        return None

    # SE ELIMINA @staticmethod
    def delete(self, event_id):
        event = Event.get_or_none(Event.id == event_id)
        if event:
            event.delete_instance()
            return True
        return False

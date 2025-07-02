import datetime

class EventController:
    """
    Controlador para orquestar las operaciones de los Eventos.
    Recibe un repositorio a través de inyección de dependencias.
    """

    # 1. Creamos un constructor que RECIBE el repositorio.
    def __init__(self, repository):
        self.repository = repository

    # 2. Quitamos @staticmethod y usamos 'self' para acceder al repositorio.
    def create_event(self, codigo_evento, nombre_evento, descripcion, pais_evento, fecha_inicio, fecha_fin):

        if datetime.date.fromisoformat(fecha_inicio) > datetime.date.fromisoformat(fecha_fin):
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        return self.repository.create(
            codigo_evento, nombre_evento, descripcion, pais_evento, fecha_inicio, fecha_fin
        )

    def get_event(self, event_id):
        return self.repository.get_by_id(event_id)

    def list_events(self):
        return self.repository.get_all()

    def update_event(self, event_id, **kwargs):
        return self.repository.update(event_id, **kwargs)

    def delete_event(self, event_id):
        return self.repository.delete(event_id)

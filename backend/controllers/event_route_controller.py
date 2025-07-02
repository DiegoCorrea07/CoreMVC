
class EventRouteController:
    """
    Controlador para orquestar las operaciones de las Rutas de Evento.
    Recibe un repositorio a través de inyección de dependencias.
    """

    # 1. Creamos un constructor que RECIBE el repositorio.
    def __init__(self, repository):
        self.repository = repository

    # 2. Quitamos @staticmethod y usamos 'self' para acceder al repositorio.
    def create_event_route(self, ruta_id, evento_id, demanda_estimada):

        return self.repository.create(ruta_id, evento_id, demanda_estimada)

    def get_event_route(self, event_route_id):
        return self.repository.get_by_id(event_route_id)

    def list_event_routes(self):
        return self.repository.get_all()

    def delete_event_route(self, event_route_id):
        return self.repository.delete(event_route_id)

    def update_event_route(self, event_route_id, demanda_estimada):

        if int(demanda_estimada) < 0:
            raise ValueError("La demanda estimada no puede ser negativa.")

        # El método de actualización en tu repositorio original no estaba implementado,
        event_route = self.repository.update(event_route_id, demanda_estimada)
        if not event_route:
            raise ValueError("Ruta de Evento no encontrada.")
        return event_route

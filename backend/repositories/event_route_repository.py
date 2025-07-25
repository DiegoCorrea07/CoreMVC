from backend.models.event_route import EventRoute
from backend.models.route import Route
from backend.models.event import Event
from peewee import JOIN, IntegrityError


class EventRouteRepository:
    """
    Repositorio para gestionar las operaciones de la base de datos para las Rutas de Evento.
    Los métodos son de instancia para permitir la Inyección de Dependencias.
    """

    # SE ELIMINA @staticmethod
    def create(self, ruta_id, evento_id, demanda_estimada):
        try:
            return EventRoute.create(
                ruta=ruta_id,
                evento=evento_id,
                demanda_estimada=demanda_estimada
            )
        except IntegrityError:
            # Capturar el error de integridad y lanzar un error más descriptivo
            raise ValueError("Esta ruta ya está asignada a este evento.")

    # SE ELIMINA @staticmethod
    def get_by_id(self, event_route_id):
        return EventRoute.select(
            EventRoute,
            Route,
            Event
        ) \
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id)) \
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id)) \
            .where(EventRoute.id == event_route_id) \
            .get_or_none()

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(
            EventRoute.select(
                EventRoute,
                Route,
                Event
            ) \
                .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id)) \
                .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id)) \
                .order_by(EventRoute.id)
        )

    # SE ELIMINA @staticmethod
    def update(self, event_route_id, **kwargs):
        # Definimos todos los campos que se pueden actualizar
        allowed_fields = ['ruta_id', 'evento_id', 'demanda_estimada']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}

        # "Traducimos" los nombres para que coincidan con los del modelo de Peewee
        if 'ruta_id' in update_data:
            update_data['ruta'] = update_data.pop('ruta_id')

        if 'evento_id' in update_data:
            update_data['evento'] = update_data.pop('evento_id')

        # Si no hay datos válidos para actualizar, no hacemos nada
        if not update_data:
            return False

        try:
            query = EventRoute.update(**update_data).where(EventRoute.id == event_route_id)
            rows_updated = query.execute()
            return rows_updated > 0
        except IntegrityError:
            # Esto previene que se asigne una combinación de ruta y evento que ya existe
            raise ValueError("Error: La combinación de esta ruta y evento ya existe.")

    # SE ELIMINA @staticmethod
    def delete(self, event_route_id):
        event_route = EventRoute.get_or_none(EventRoute.id == event_route_id)
        if event_route:
            event_route.delete_instance()
            return True
        return False

    # SE ELIMINA @staticmethod
    def get_by_route_and_event(self, route_id, event_id):
        return EventRoute.get_or_none(
            (EventRoute.ruta == route_id) & (EventRoute.evento == event_id)
        )

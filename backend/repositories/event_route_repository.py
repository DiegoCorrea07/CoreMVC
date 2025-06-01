from backend.models.event_route import EventRoute
from backend.models.route import Route
from backend.models.event import Event
from peewee import JOIN, IntegrityError

class EventRouteRepository:
    @staticmethod
    def create(ruta_id, evento_id, demanda_estimada):
        try:
            return EventRoute.create(
                ruta=ruta_id,
                evento=evento_id,
                demanda_estimada=demanda_estimada
            )
        except IntegrityError:
            raise ValueError("Esta ruta ya está asignada a este evento.")


    @staticmethod
    def get_by_id(event_route_id):

        return EventRoute.select(
                EventRoute,
                Route,
                Event
            )\
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id))\
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id))\
            .where(EventRoute.id == event_route_id)\
            .get_or_none()

    @staticmethod
    def get_all():

        return list(
            EventRoute.select(
                EventRoute,
                Route,
                Event
            )\
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id))\
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id))\
            .order_by(EventRoute.id)
        )

    @staticmethod
    def update(event_route_id, demanda_estimada):
        event_route = EventRoute.get_or_none(EventRoute.id == event_route_id)
        if event_route:
            event_route.demanda_estimada = demanda_estimada
            event_route.save()
            return event_route
        return None

    @staticmethod
    def delete(event_route_id):
        event_route = EventRoute.get_or_none(EventRoute.id == event_route_id)
        if event_route:
            event_route.delete_instance()
            return True
        return False

    @staticmethod
    def get_by_route_and_event(route_id, event_id):
        return EventRoute.get_or_none(
            (EventRoute.ruta == route_id) & (EventRoute.evento == event_id)
        )
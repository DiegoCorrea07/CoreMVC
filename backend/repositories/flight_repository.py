from backend.models.flight import Flight
from backend.models.aircraft import Aircraft
from backend.models.event_route import EventRoute
from backend.models.route import Route
from backend.models.event import Event
from peewee import JOIN

class FlightRepository:
    # SE ELIMINA @staticmethod
    def create(self, codigo_vuelo, aeronave_id, ruta_evento_id, fecha_salida, fecha_llegada):
        return Flight.create(
            codigo_vuelo=codigo_vuelo,
            aeronave=aeronave_id,
            ruta_evento=ruta_evento_id,
            fecha_salida=fecha_salida,
            fecha_llegada=fecha_llegada
        )

    # SE ELIMINA @staticmethod
    def get_by_id(self, flight_id):
        return Flight.select(
                Flight,
                Aircraft,
                EventRoute,
                Route,
                Event
            )\
            .join(Aircraft, JOIN.LEFT_OUTER).switch(Flight)\
            .join(EventRoute, JOIN.LEFT_OUTER)\
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id))\
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id))\
            .where(Flight.id == flight_id)\
            .get_or_none()

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(
            Flight.select(
                Flight,
                Aircraft,
                EventRoute,
                Route,
                Event
            )\
            .join(Aircraft, JOIN.LEFT_OUTER).switch(Flight)\
            .join(EventRoute, JOIN.LEFT_OUTER)\
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id))\
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id))\
            .order_by(Flight.id)
        )

    # SE ELIMINA @staticmethod
    def delete(self, flight_id):
        flight = Flight.get_or_none(Flight.id == flight_id)
        if flight:
            flight.delete_instance()
            return True
        return False
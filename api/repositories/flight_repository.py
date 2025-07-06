
from api.models.flight import Flight
from api.models.aircraft import Aircraft
from api.models.event_route import EventRoute
from api.models.route import Route
from api.models.event import Event
from peewee import JOIN

class FlightRepository:
    """
    Repositorio para el microservicio de Manifiesto.
    Solo contiene los métodos necesarios para esta API.
    """

    def get_by_id(self, flight_id):
        return Flight.select(
            Flight,
            Aircraft,
            EventRoute,
            Route,
            Event
        ) \
            .join(Aircraft, JOIN.LEFT_OUTER).switch(Flight) \
            .join(EventRoute, JOIN.LEFT_OUTER) \
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id)) \
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id)) \
            .where(Flight.id == flight_id) \
            .get_or_none()

    def get_manifest_data(self, flight_id):
        """
        Obtiene los datos consolidados para el manifiesto de un vuelo específico.
        Esta consulta une todas las tablas relevantes para recolectar la información.
        """
        flight_data = self.get_by_id(flight_id)
        return flight_data
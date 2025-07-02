import datetime
from peewee import DoesNotExist
from backend.models.flight import Flight
from backend.models.event import Event

class FlightValidator:
    # 1. El constructor ahora también recibe el event_route_repo
    def __init__(self, data, aeronave_id, ruta_evento_id, event_route_repo):
        self.data = data
        self.aeronave_id = aeronave_id
        self.ruta_evento_id = ruta_evento_id
        self.event_route_repo = event_route_repo  # Lo guardamos
        self.errors = []
        self.event_route = None
        self.fecha_salida_dt = None
        self.fecha_llegada_dt = None

    def validate(self):
        """Orquesta todas las validaciones. Lanza un ValueError si alguna falla."""
        self._parse_and_validate_dates()
        self._validate_flight_code()
        self._validate_event_route_and_dates()
        self._validate_aircraft_availability()

        if self.errors:
            raise ValueError(". ".join(self.errors))

    def _parse_and_validate_dates(self):
        """Parsea las fechas y valida que la llegada sea después de la salida."""
        try:
            self.fecha_salida_dt = datetime.datetime.fromisoformat(self.data["fecha_salida"])
            self.fecha_llegada_dt = datetime.datetime.fromisoformat(self.data["fecha_llegada"])
            if self.fecha_salida_dt >= self.fecha_llegada_dt:
                self.errors.append("La fecha de salida debe ser anterior a la fecha de llegada")
        except (ValueError, TypeError):
            self.errors.append("Formato de fecha y hora inválido. Use ISO 8601.")

    def _validate_flight_code(self):
        """Valida que el código de vuelo no exista ya."""
        if Flight.get_or_none(Flight.codigo_vuelo == self.data["codigo_vuelo"]):
            self.errors.append("El código de vuelo ya existe")

    def _validate_event_route_and_dates(self):
        """Valida que la ruta del evento exista y que las fechas del vuelo estén dentro del evento."""
        try:
            # 2. Usamos la instancia del repositorio que recibimos
            self.event_route = self.event_route_repo.get_by_id(self.ruta_evento_id)
            if not self.event_route:
                self.errors.append("La Ruta de Evento no existe")
                return

            evento = Event.get_by_id(self.event_route.evento.id)

            fecha_inicio_evento = datetime.datetime.combine(evento.fecha_inicio, datetime.time.min)
            fecha_fin_evento = datetime.datetime.combine(evento.fecha_fin, datetime.time.max)

            if not (fecha_inicio_evento <= self.fecha_salida_dt <= fecha_fin_evento):
                self.errors.append("La fecha de salida del vuelo está fuera del rango de fechas del evento.")

            if not (fecha_inicio_evento <= self.fecha_llegada_dt <= fecha_fin_evento):
                self.errors.append("La fecha de llegada del vuelo está fuera del rango de fechas del evento.")

        except DoesNotExist:
            self.errors.append("La Ruta de Evento o el Evento asociado no existe")

    def _validate_aircraft_availability(self):
        """Valida que la aeronave no tenga vuelos que se solapen en el tiempo."""
        if not self.fecha_salida_dt or not self.fecha_llegada_dt:
            return

        conflicting_flight = Flight.select().where(
            (Flight.aeronave == self.aeronave_id) &
            (
                    (Flight.fecha_salida < self.fecha_llegada_dt) & (Flight.fecha_llegada > self.fecha_salida_dt)
            )
        ).first()

        if conflicting_flight:
            self.errors.append(
                f"La aeronave ya tiene un vuelo programado ({conflicting_flight.codigo_vuelo}) que se solapa con este horario.")


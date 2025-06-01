from backend.models.flight import Flight
from backend.repositories.event_repository import EventRepository
from backend.repositories.flight_repository import FlightRepository
from backend.repositories.event_route_repository import EventRouteRepository
from backend.db.connection import db
import datetime

class FlightController:
    @staticmethod
    def create_flight(codigo_vuelo, aeronave_id, ruta_evento_id, fecha_salida, fecha_llegada):
        with db.atomic():
            # 1. Validar que el código de vuelo no se repita
            existing = Flight.get_or_none(Flight.codigo_vuelo == codigo_vuelo)
            if existing:
                raise ValueError("El código de vuelo ya existe. No puede repetirse.")

            # 2. Obtener la Ruta de Evento y el Evento asociado
            event_route = EventRouteRepository.get_by_id(ruta_evento_id)
            if not event_route:
                raise ValueError("La Ruta de Evento especificada no existe.")

            event_obj = EventRepository.get_by_id(event_route.evento.id) # Accede al ID del evento a través de la relación
            if not event_obj:
                raise ValueError("El Evento asociado a la Ruta de Evento no fue encontrado.")

            # 3. Convertir las fechas de string a objetos datetime
            try:
                fecha_salida_vuelo = datetime.datetime.fromisoformat(fecha_salida)
                fecha_llegada_vuelo = datetime.datetime.fromisoformat(fecha_llegada)
            except ValueError:
                raise ValueError("Formato de fecha u hora inválido. Utilice 'YYYY-MM-DDTHH:MM'.")

            fecha_inicio_evento = event_obj.fecha_inicio
            fecha_fin_evento = event_obj.fecha_fin

            if isinstance(fecha_inicio_evento, datetime.date) and not isinstance(fecha_inicio_evento, datetime.datetime):
                fecha_inicio_evento = datetime.datetime.combine(fecha_inicio_evento, datetime.time.min)
            if isinstance(fecha_fin_evento, datetime.date) and not isinstance(fecha_fin_evento, datetime.datetime):
                fecha_fin_evento = datetime.datetime.combine(fecha_fin_evento, datetime.time.max)

            # 4. Realizar la validación de rango de fechas del evento
            if not (fecha_inicio_evento <= fecha_salida_vuelo <= fecha_fin_evento):
                raise ValueError(
                    f"La fecha de salida del vuelo ({fecha_salida_vuelo.strftime('%Y-%m-%d %H:%M')}) "
                    f"no está dentro del rango del evento '{event_obj.nombre_evento}' "
                    f"({fecha_inicio_evento.strftime('%Y-%m-%d %H:%M')} a {fecha_fin_evento.strftime('%Y-%m-%d %H:%M')})."
                )

            if not (fecha_inicio_evento <= fecha_llegada_vuelo <= fecha_fin_evento):
                 raise ValueError(
                    f"La fecha de llegada del vuelo ({fecha_llegada_vuelo.strftime('%Y-%m-%d %H:%M')}) "
                    f"no está dentro del rango del evento '{event_obj.nombre_evento}' "
                    f"({fecha_inicio_evento.strftime('%Y-%m-%d %H:%M')} a {fecha_fin_evento.strftime('%Y-%m-%d %H:%M')})."
                )

            # 5. Opcional: Validar que fecha_salida_vuelo sea anterior o igual a fecha_llegada_vuelo
            if fecha_salida_vuelo > fecha_llegada_vuelo:
                raise ValueError("La fecha de salida del vuelo no puede ser posterior a la fecha de llegada.")

            MARGEN_ENTRE_VUELOS = datetime.timedelta(minutes=1)
            # Buscar vuelos de la misma aeronave que puedan solaparse
            conflicting_flights = Flight.select().where(
                (Flight.aeronave == aeronave_id) &
                (
                    # El vuelo existente empieza antes que el nuevo termine Y el vuelo existente termina después que el nuevo empiece
                        (Flight.fecha_salida < (
                                    fecha_llegada_vuelo + MARGEN_ENTRE_VUELOS)) &  # Vuelo existente empieza antes de que el nuevo termine + margen
                        (Flight.fecha_llegada > (fecha_salida_vuelo - MARGEN_ENTRE_VUELOS))
                # Vuelo existente termina después de que el nuevo empiece - margen
                )
            ).count()

            if conflicting_flights > 0:
                raise ValueError(
                    f"La aeronave con ID {aeronave_id} ya tiene vuelos programados "
                    "Por favor, revise la disponibilidad de la aeronave. "
                    "O seleccione otra aeronave"
                )

            # 6. Si todas las validaciones pasan, procede con la creación
            return FlightRepository.create(
                codigo_vuelo, aeronave_id, ruta_evento_id, fecha_salida_vuelo, fecha_llegada_vuelo # ¡Pasar objetos datetime!
            )

    @staticmethod
    def get_flight(flight_id):
        return FlightRepository.get_by_id(flight_id)

    @staticmethod
    def list_flights():
        return FlightRepository.get_all()

    @staticmethod
    def delete_flight(flight_id):
        return FlightRepository.delete(flight_id)
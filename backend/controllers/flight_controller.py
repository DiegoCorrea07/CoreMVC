from backend.models.flight import Flight
from backend.repositories.flight_repository import FlightRepository

class FlightController:
    @staticmethod
    def create_flight(codigo_vuelo, aeronave_id, route_id, evento_id, fecha_salida, fecha_llegada):

        existing = Flight.get_or_none(Flight.codigo_vuelo == codigo_vuelo)
        if existing:
            raise ValueError("El código de vuelo ya existe. No puede repetirse.")

        return FlightRepository.create(
            codigo_vuelo, aeronave_id, route_id, evento_id, fecha_salida, fecha_llegada
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

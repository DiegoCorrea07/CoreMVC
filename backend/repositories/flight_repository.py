
from backend.models.flight import Flight

class FlightRepository:
    @staticmethod
    def create(codigo_vuelo, aeronave_id, route_id, evento_id, fecha_salida, fecha_llegada):
        return Flight.create(
            codigo_vuelo=codigo_vuelo,
            aeronave_id=aeronave_id,
            ruta_id=route_id,
            evento_id=evento_id,
            fecha_salida=fecha_salida,
            fecha_llegada=fecha_llegada
        )

    @staticmethod
    def get_by_id(flight_id):
        return Flight.get_or_none(Flight.id == flight_id)

    @staticmethod
    def get_all():
        return list(Flight.select())

    @staticmethod
    def delete(flight_id):
        flight = Flight.get_or_none(Flight.id == flight_id)
        if flight:
            flight.delete_instance()
            return True
        return False

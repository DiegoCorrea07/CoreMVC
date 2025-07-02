from backend.validators.flight_validator import FlightValidator

class FlightController:
    # 1. El constructor ahora recibe AMBOS repositorios
    def __init__(self, repository, event_route_repo):
        self.repository = repository
        self.event_route_repo = event_route_repo

    def create_flight(self, codigo_vuelo, aeronave_id, ruta_evento_id, fecha_salida, fecha_llegada):
        try:
            validator_data = {
                "codigo_vuelo": codigo_vuelo,
                "fecha_salida": fecha_salida,
                "fecha_llegada": fecha_llegada,
            }
            # 2. Le pasamos el event_route_repo al validador
            validator = FlightValidator(
                validator_data,
                aeronave_id,
                ruta_evento_id,
                event_route_repo=self.event_route_repo
            )
            validator.validate()

            return self.repository.create(
                codigo_vuelo=codigo_vuelo,
                aeronave_id=aeronave_id,
                ruta_evento_id=ruta_evento_id,
                fecha_salida=validator.fecha_salida_dt,
                fecha_llegada=validator.fecha_llegada_dt
            )
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Error inesperado al crear el vuelo: {e}")

    def get_flight(self, flight_id):
        return self.repository.get_by_id(flight_id)

    def list_flights(self):
        return self.repository.get_all()

    def delete_flight(self, flight_id):
        return self.repository.delete(flight_id)

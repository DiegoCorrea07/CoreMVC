from backend.validators.flight_validator import FlightValidator
import datetime

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

    def update_flight(self, flight_id, **data):
        """
        Maneja la lógica de negocio para actualizar un vuelo.
        """

        if 'fecha_salida' in data and 'fecha_llegada' in data:
            if data['fecha_salida'] >= data['fecha_llegada']:
                raise ValueError("La fecha de salida debe ser anterior a la de llegada.")

        # Convertimos las fechas a objetos datetime si vienen como string
        if 'fecha_salida' in data:
            data['fecha_salida'] = datetime.datetime.fromisoformat(data['fecha_salida'])
        if 'fecha_llegada' in data:
            data['fecha_llegada'] = datetime.datetime.fromisoformat(data['fecha_llegada'])

        # Llamamos al método update del repositorio
        updated = self.repository.update(flight_id, **data)

        if not updated:
            raise ValueError("Vuelo no encontrado o datos inválidos para actualizar.")

        # Devolvemos el objeto actualizado para enviarlo en la respuesta de la API
        return self.repository.get_by_id(flight_id)

    def delete_flight(self, flight_id):
        return self.repository.delete(flight_id)

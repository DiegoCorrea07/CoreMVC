from backend.validators.flight_validator import FlightValidator
import datetime


class FlightController:
    """
    Controlador para orquestar las operaciones de los Vuelos.
    Ahora también gestiona la creación de manifiestos.
    """

    def __init__(self, repository, event_route_repo, real_coverage_repo):
        self.repository = repository
        self.event_route_repo = event_route_repo
        self.real_coverage_repo = real_coverage_repo

    def create_flight(self, codigo_vuelo, aeronave_id, ruta_evento_id, fecha_salida, fecha_llegada):
        # Este método no cambia.
        try:
            validator_data = {
                "codigo_vuelo": codigo_vuelo,
                "fecha_salida": fecha_salida,
                "fecha_llegada": fecha_llegada,
            }
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

    def get_manifest(self, flight_id):
        """
        Orquesta la obtención de datos de múltiples fuentes para construir el manifiesto.
        """
        flight_data = self.repository.get_manifest_data(flight_id)

        if not flight_data:
            return None

        event_route_id = flight_data.ruta_evento.id
        latest_coverage = self.real_coverage_repo.get_latest_for_event_route(event_route_id)

        # --- CORRECCIÓN AQUÍ: Usamos int() para valores que son inherentemente enteros ---
        demanda_estimada = int(flight_data.ruta_evento.demanda_estimada)
        capacidad_vuelo_actual = int(flight_data.aeronave.capacidad)

        estado_cobertura = "Sin Datos"
        capacidad_real_vuelos = 0

        if latest_coverage:
            estado_cobertura = latest_coverage.estado_cobertura
            capacidad_real_vuelos = int(
                latest_coverage.capacidad_real) if latest_coverage.capacidad_real is not None else 0

        # El cálculo de asientos disponibles ahora opera con enteros.
        asientos_disponibles = max(0, capacidad_vuelo_actual)

        manifest = {
            "vuelo": {
                "id": flight_data.id,
                "codigo": flight_data.codigo_vuelo,
                "fecha_salida": flight_data.fecha_salida.isoformat(),
                "fecha_llegada": flight_data.fecha_llegada.isoformat(),
            },
            "ruta": {
                "origen": flight_data.ruta_evento.ruta.origen,
                "destino": flight_data.ruta_evento.ruta.destino,
            },
            "aeronave": {
                "modelo": flight_data.aeronave.modelo,
                "matricula": flight_data.aeronave.matricula,
                "capacidad_maxima": capacidad_vuelo_actual,
            },
            "evento": {
                "nombre": flight_data.ruta_evento.evento.nombre_evento,
            },
            "cobertura_ruta": {
                "demanda_estimada": demanda_estimada,
                "estado_general": estado_cobertura,
                "capacidad_total_asignada": capacidad_real_vuelos,
            },
            "manifiesto_vuelo": {
                "asientos_disponibles": asientos_disponibles
            }
        }
        return manifest

    # Los métodos CRUD existentes no cambian.
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

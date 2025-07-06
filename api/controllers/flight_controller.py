class FlightController:

    def __init__(self, repository, real_coverage_repo):
        self.repository = repository
        self.real_coverage_repo = real_coverage_repo

    def get_manifest(self, flight_id):
        """
        Orquesta la obtención de datos de múltiples fuentes para construir el manifiesto.
        """
        # 1. Obtención de datos principales del vuelo
        flight_data = self.repository.get_manifest_data(flight_id)

        if not flight_data:
            return None

        # 2. Obtención de datos de cobertura relacionados
        event_route_id = flight_data.ruta_evento.id
        latest_coverage = self.real_coverage_repo.get_latest_for_event_route(event_route_id)

        # 3. Preparación de las variables para el manifiesto
        demanda_estimada = int(flight_data.ruta_evento.demanda_estimada)
        capacidad_vuelo_actual = int(flight_data.aeronave.capacidad)

        # Valores por defecto
        estado_cobertura = "Sin Datos"
        capacidad_real_vuelos = 0

        if latest_coverage:
            estado_cobertura = latest_coverage.estado_cobertura
            # Se asegura de que capacidad_real no sea None antes de convertir a entero
            if latest_coverage.capacidad_real is not None:
                capacidad_real_vuelos = int(latest_coverage.capacidad_real)

        # Cálculo de asientos disponibles (respetando tu lógica original)
        asientos_disponibles = max(0, capacidad_vuelo_actual)

        # 4. Construcción del diccionario 'manifest' con toda la información
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
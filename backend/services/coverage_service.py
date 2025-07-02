import datetime
import math
from peewee import fn, SQL

# 1. Importa las nuevas estrategias que creaste
from backend.strategies.coverage_strategies import (
    CriticalStatusStrategy,
    PartialStatusStrategy,
    CoveredStatusStrategy,
    ICoverageStatusStrategy
)

from backend.models.event_route import EventRoute
from backend.models.route import Route
from backend.models.event import Event
from backend.models.flight import Flight
from backend.models.aircraft import Aircraft


class CoverageService:
    def __init__(self, real_coverage_repo, coverage_alert_repo):
        self.real_coverage_repo = real_coverage_repo
        self.coverage_alert_repo = coverage_alert_repo
        # 2. Define la lista de estrategias que el servicio usará
        self.status_strategies: list[ICoverageStatusStrategy] = [
            CriticalStatusStrategy(),
            PartialStatusStrategy(),
            CoveredStatusStrategy()
        ]

    def _determine_coverage_status(self, percentage: float) -> str:
        """
        Este método aplica el Patrón Estrategia.
        Itera sobre las estrategias y usa la primera que devuelva un resultado.
        """
        for strategy in self.status_strategies:
            status = strategy.get_status(percentage)
            if status:
                return status
        return "Indefinido"  # Un valor por defecto si ninguna estrategia aplica

    async def calculate_coverage_for_event(self, event_id, status_filter=None, page=1, limit=10):
        # La consulta a la base de datos se mantiene igual...
        subquery_flights_capacity = (
            Flight.select(
                Flight.ruta_evento,
                fn.SUM(Aircraft.capacidad).alias('total_capacidad_vuelos')
            )
            .join(Aircraft, on=(Flight.aeronave == Aircraft.id))
            .group_by(Flight.ruta_evento)
            .alias('flight_capacity_subquery')
        )

        query = EventRoute.select(
            EventRoute.id,
            EventRoute.demanda_estimada,
            Route.origen,
            Route.destino,
            Event.nombre_evento,
            subquery_flights_capacity.c.total_capacidad_vuelos.alias('capacidad_real_vuelos')
        ).join(
            Route, on=(EventRoute.ruta == Route.id)
        ).join(
            Event, on=(EventRoute.evento == Event.id)
        ).left_outer_join(
            subquery_flights_capacity, on=(EventRoute.id == subquery_flights_capacity.c.ruta_evento_id)
        )

        if event_id is not None:
            query = query.where(EventRoute.evento == event_id)

        all_event_routes_processed = []

        for er_data_row in query.dicts().iterator():
            demanda_estimada = float(er_data_row['demanda_estimada'])
            capacidad_real = float(er_data_row['capacidad_real_vuelos']) if er_data_row[
                                                                                'capacidad_real_vuelos'] is not None else 0.0

            if demanda_estimada > 0:
                porcentaje_cobertura = (capacidad_real / demanda_estimada) * 100
            else:
                porcentaje_cobertura = 100.0

            # --- 3. REEMPLAZO DEL IF/ELIF/ELSE ---
            # En lugar del bloque de condicionales, ahora llamamos a nuestro método de estrategia.
            estado_cobertura = self._determine_coverage_status(porcentaje_cobertura)

            if status_filter is None or estado_cobertura.lower() == status_filter.lower():
                all_event_routes_processed.append({
                    "id": er_data_row['id'],
                    "nombre_ruta": f"{er_data_row['origen']}-{er_data_row['destino']}",
                    "nombre_evento": er_data_row['nombre_evento'],
                    "demanda_estimada": demanda_estimada,
                    "capacidad_real": capacidad_real,
                    "porcentaje_cobertura": round(porcentaje_cobertura, 2),
                    "estado_cobertura": estado_cobertura,
                    "fecha_calculo": datetime.datetime.now().isoformat()
                })

        # El resto del método (paginación, creación de alertas, etc.) se mantiene exactamente igual...
        total_items_filtered_by_status = len(all_event_routes_processed)
        cubiertas_count = sum(1 for r in all_event_routes_processed if r['estado_cobertura'] == "Cubierta")
        parciales_count = sum(1 for r in all_event_routes_processed if r['estado_cobertura'] == "Parcial")
        criticas_count = sum(1 for r in all_event_routes_processed if r['estado_cobertura'] == "Crítica")
        porcentaje_cubiertas = round((cubiertas_count / total_items_filtered_by_status) * 100,
                                     2) if total_items_filtered_by_status > 0 else 0
        porcentaje_parciales = round((parciales_count / total_items_filtered_by_status) * 100,
                                     2) if total_items_filtered_by_status > 0 else 0
        porcentaje_criticas = round((criticas_count / total_items_filtered_by_status) * 100,
                                    2) if total_items_filtered_by_status > 0 else 0
        summary_metrics = {"cubiertas": porcentaje_cubiertas, "parciales": porcentaje_parciales,
                           "criticas": porcentaje_criticas, "total_routes": total_items_filtered_by_status}
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paged_routes = all_event_routes_processed[start_index:end_index]

        for er_data in paged_routes:
            original_er = EventRoute.get_or_none(EventRoute.id == er_data['id'])
            if original_er:
                real_coverage = self.real_coverage_repo.create(
                    ruta_evento_id=original_er.id,
                    capacidad_real=er_data['capacidad_real'],
                    porcentaje_cobertura=er_data['porcentaje_cobertura'],
                    estado_cobertura=er_data['estado_cobertura'],
                    fecha_calculo=datetime.datetime.now()
                )

                if er_data['estado_cobertura'] == "Crítica":
                    self.coverage_alert_repo.create(
                        cobertura_id=real_coverage.id,
                        tipo_alerta="roja",
                        descripcion=f"La cobertura para la ruta '{er_data['nombre_ruta']}' en el evento '{er_data['nombre_evento']}' es CRÍTICA ({er_data['porcentaje_cobertura']:.2f}%). Demanda: {er_data['demanda_estimada']}, Capacidad: {er_data['capacidad_real']}.",
                        fecha_generacion=datetime.datetime.now()
                    )
                elif er_data['estado_cobertura'] == "Parcial":
                    self.coverage_alert_repo.create(
                        cobertura_id=real_coverage.id,
                        tipo_alerta="amarilla",
                        descripcion=f"La cobertura para la ruta '{er_data['nombre_ruta']}' en el evento '{er_data['nombre_evento']}' es PARCIAL ({er_data['porcentaje_cobertura']:.2f}%). Demanda: {er_data['demanda_estimada']}, Capacidad: {er_data['capacidad_real']}.",
                        fecha_generacion=datetime.datetime.now()
                    )

        total_pages = math.ceil(total_items_filtered_by_status / limit) if total_items_filtered_by_status > 0 else 1

        return {
            "dashboard_data": paged_routes,
            "summary_metrics": summary_metrics,
            "total_pages": total_pages,
            "total_items": total_items_filtered_by_status
        }

    async def get_route_detail(self, ruta_evento_id):

        event_route = (EventRoute.select(EventRoute, Route, Event)
                       .join(Route, on=(EventRoute.ruta == Route.id))
                       .switch(EventRoute)  # Volvemos a EventRoute
                       .join(Event, on=(EventRoute.evento == Event.id))
                       .where(EventRoute.id == ruta_evento_id)
                       .get_or_none())

        if not event_route:
            return None

        demanda_estimada = float(event_route.demanda_estimada)

        latest_coverage = self.real_coverage_repo.get_latest_for_event_route(ruta_evento_id)

        capacidad_real_total = float(latest_coverage.capacidad_real) if latest_coverage else 0.0
        porcentaje_cobertura_total = float(latest_coverage.porcentaje_cobertura) if latest_coverage else 0.0
        estado_cobertura_total = latest_coverage.estado_cobertura if latest_coverage else "Sin Datos"

        fecha_inicio_evento = event_route.evento.fecha_inicio
        fecha_fin_evento = event_route.evento.fecha_fin

        if isinstance(fecha_inicio_evento, datetime.date) and not isinstance(fecha_inicio_evento, datetime.datetime):
            fecha_inicio_evento = datetime.datetime.combine(fecha_inicio_evento, datetime.time.min)
        if isinstance(fecha_fin_evento, datetime.date) and not isinstance(fecha_fin_evento, datetime.datetime):
            fecha_fin_evento = datetime.datetime.combine(fecha_fin_evento, datetime.time.max)

        flights_weekly_capacity_query = Flight.select(
            SQL("EXTRACT('dow' FROM fecha_salida) AS day_of_week_num"),
            fn.SUM(Aircraft.capacidad).alias('total_capacity_for_day')
        ).join(Aircraft).where(
            (Flight.ruta_evento == event_route.id) &
            (Flight.fecha_salida >= fecha_inicio_evento) &
            (Flight.fecha_salida <= fecha_fin_evento)
        ).group_by(SQL("EXTRACT('dow' FROM fecha_salida)")).dicts()

        weekly_capacities_map = {int(entry['day_of_week_num']): float(entry['total_capacity_for_day']) for entry in
                                 flights_weekly_capacity_query}
        day_names_map = {0: "Domingo", 1: "Lunes", 2: "Martes", 3: "Miércoles", 4: "Jueves", 5: "Viernes", 6: "Sábado"}
        weekly_coverage_data = []
        for dow_num in range(7):
            day_name = day_names_map[dow_num]
            capacidad_ofrecida_semana_dia = weekly_capacities_map.get(dow_num, 0)
            percentage = (capacidad_ofrecida_semana_dia / demanda_estimada) * 100 if demanda_estimada > 0 else 0.0
            weekly_coverage_data.append({"day": day_name, "coverage": round(percentage, 2)})

        return {
            "id": event_route.id,
            "route_name": f"{event_route.ruta.origen} - {event_route.ruta.destino}",
            "status": estado_cobertura_total,
            "event_name": event_route.evento.nombre_evento,
            "event_start_date": event_route.evento.fecha_inicio.isoformat(),
            "event_end_date": event_route.evento.fecha_fin.isoformat(),
            "demanda_estimada": demanda_estimada,
            "capacidad_ofrecida": capacidad_real_total,
            "porcentaje_cobertura": porcentaje_cobertura_total,
            "daily_coverage": weekly_coverage_data
        }


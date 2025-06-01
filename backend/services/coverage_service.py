import datetime
from peewee import fn, JOIN, SQL
from backend.models.event_route import EventRoute
from backend.models.route import Route
from backend.models.event import Event
from backend.models.flight import Flight
from backend.models.aircraft import Aircraft
from backend.repositories.real_coverage_repository import RealCoverageRepository
from backend.repositories.coverage_alert_repository import CoverageAlertRepository
import decimal


class CoverageService:
    async def calculate_coverage_for_event(self, event_id, status_filter=None, page=1,
                                           limit=10):
        results = []
        all_event_routes_for_event = []

        event_routes_full_query = EventRoute.select(
            EventRoute, Route, Event
        ).where(EventRoute.evento == event_id) \
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id)) \
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id))

        for er_full in event_routes_full_query:
            demanda_estimada_full = float(er_full.demanda_estimada) if isinstance(er_full.demanda_estimada,
                                                                                  decimal.Decimal) else float(
                er_full.demanda_estimada)

            capacidad_real_full_query = Flight.select(fn.SUM(Aircraft.capacidad)) \
                .join(Aircraft) \
                .where(Flight.ruta_evento == er_full.id) \
                .scalar()
            capacidad_real_full = float(capacidad_real_full_query) if isinstance(capacidad_real_full_query,
                                                                                 decimal.Decimal) else (
                capacidad_real_full_query if capacidad_real_full_query is not None else 0)

            if demanda_estimada_full > 0:
                porcentaje_cobertura_full = (capacidad_real_full / demanda_estimada_full) * 100
            else:
                porcentaje_cobertura_full = 100.0

            if porcentaje_cobertura_full >= 100:
                estado_cobertura_full = "Cubierta"
            elif porcentaje_cobertura_full >= 70:
                estado_cobertura_full = "Parcial"
            else:
                estado_cobertura_full = "Crítica"

            all_event_routes_for_event.append({
                "id": er_full.id,
                "nombre_ruta": f"{er_full.ruta.origen}-{er_full.ruta.destino}",
                "nombre_evento": er_full.evento.nombre_evento,
                "demanda_estimada": demanda_estimada_full,
                "capacidad_real": capacidad_real_full,
                "porcentaje_cobertura": round(porcentaje_cobertura_full, 2),
                "estado_cobertura": estado_cobertura_full,
                "fecha_calculo": datetime.datetime.now().isoformat()
            })

        total_routes = len(all_event_routes_for_event)
        cubiertas_count = sum(1 for r in all_event_routes_for_event if r['estado_cobertura'] == "Cubierta")
        parciales_count = sum(1 for r in all_event_routes_for_event if r['estado_cobertura'] == "Parcial")
        criticas_count = sum(1 for r in all_event_routes_for_event if r['estado_cobertura'] == "Crítica")

        porcentaje_cubiertas = round((cubiertas_count / total_routes) * 100, 2) if total_routes > 0 else 0
        porcentaje_parciales = round((parciales_count / total_routes) * 100, 2) if total_routes > 0 else 0
        porcentaje_criticas = round((criticas_count / total_routes) * 100, 2) if total_routes > 0 else 0

        summary_metrics = {
            "cubiertas": porcentaje_cubiertas,
            "parciales": porcentaje_parciales,
            "criticas": porcentaje_criticas,
            "total_routes": total_routes
        }

        filtered_paged_routes = all_event_routes_for_event

        if status_filter:
            filtered_paged_routes = [
                r for r in filtered_paged_routes if r['estado_cobertura'].lower() == status_filter.lower()
            ]

        start_index = (page - 1) * limit
        end_index = start_index + limit
        paged_routes = filtered_paged_routes[start_index:end_index]

        for er_data in paged_routes:
            original_er = EventRoute.get_or_none(EventRoute.id == er_data['id'])
            if original_er:
                real_coverage = RealCoverageRepository.create(
                    ruta_evento_id=original_er.id,
                    capacidad_real=er_data['capacidad_real'],
                    porcentaje_cobertura=er_data['porcentaje_cobertura'],
                    estado_cobertura=er_data['estado_cobertura'],
                    fecha_calculo=datetime.datetime.now()
                )

                if er_data['estado_cobertura'] == "Crítica":
                    CoverageAlertRepository.create(
                        cobertura_id=real_coverage.id,
                        tipo_alerta="roja",
                        descripcion=f"La cobertura para la ruta '{er_data['nombre_ruta']}' en el evento '{er_data['nombre_evento']}' es CRÍTICA ({er_data['porcentaje_cobertura']:.2f}%). Demanda: {er_data['demanda_estimada']}, Capacidad: {er_data['capacidad_real']}.",
                        fecha_generacion=datetime.datetime.now()
                    )
                elif er_data['estado_cobertura'] == "Parcial":
                    CoverageAlertRepository.create(
                        cobertura_id=real_coverage.id,
                        tipo_alerta="amarilla",
                        descripcion=f"La cobertura para la ruta '{er_data['nombre_ruta']}' en el evento '{er_data['nombre_evento']}' es PARCIAL ({er_data['porcentaje_cobertura']:.2f}%). Demanda: {er_data['demanda_estimada']}, Capacidad: {er_data['capacidad_real']}.",
                        fecha_generacion=datetime.datetime.now()
                    )

        return {
            "dashboard_data": paged_routes,
            "summary_metrics": summary_metrics,
            "total_pages": (len(filtered_paged_routes) + limit - 1) // limit,
            "total_items": len(filtered_paged_routes)
        }

    async def get_route_detail(self, ruta_evento_id):
        event_route = EventRoute.select(
            EventRoute,
            Route,
            Event
        ) \
            .join(Route, JOIN.LEFT_OUTER, on=(EventRoute.ruta == Route.id)) \
            .join(Event, JOIN.LEFT_OUTER, on=(EventRoute.evento == Event.id)) \
            .where(EventRoute.id == ruta_evento_id) \
            .get_or_none()

        if not event_route:
            return None

        demanda_estimada = float(event_route.demanda_estimada) if isinstance(event_route.demanda_estimada,
                                                                             decimal.Decimal) else float(
            event_route.demanda_estimada)

        latest_coverage = RealCoverageRepository.get_latest_for_event_route(ruta_evento_id)
        capacidad_real_total = float(latest_coverage.capacidad_real) if latest_coverage and isinstance(
            latest_coverage.capacidad_real, decimal.Decimal) else (
            latest_coverage.capacidad_real if latest_coverage else 0)
        porcentaje_cobertura_total = float(latest_coverage.porcentaje_cobertura) if latest_coverage and isinstance(
            latest_coverage.porcentaje_cobertura, decimal.Decimal) else (
            latest_coverage.porcentaje_cobertura if latest_coverage else 0.0)
        estado_cobertura_total = latest_coverage.estado_cobertura if latest_coverage else "Sin Datos"

        fecha_inicio_evento = event_route.evento.fecha_inicio
        fecha_fin_evento = event_route.evento.fecha_fin

        if isinstance(fecha_inicio_evento, datetime.date) and not isinstance(fecha_inicio_evento, datetime.datetime):
            fecha_inicio_evento = datetime.datetime.combine(fecha_inicio_evento, datetime.time.min)
        if isinstance(fecha_fin_evento, datetime.date) and not isinstance(fecha_fin_evento, datetime.datetime):
            fecha_fin_evento = datetime.datetime.combine(fecha_fin_evento, datetime.time.max)

        # 1. Obtener la capacidad total ofrecida agrupada por día de la semana (número de 0-6)
        # Usamos EXTRACT(DOW FROM fecha_salida) para PostgreSQL, que devuelve 0 (Domingo) a 6 (Sábado)
        flights_weekly_capacity_query = Flight.select(
            # ¡CAMBIO A T2 AQUÍ!
            SQL("EXTRACT('dow' FROM t2.fecha_salida) AS day_of_week_num"),
            fn.SUM(Aircraft.capacidad).alias('total_capacity_for_day')
        ).join(Aircraft).where(
            (Flight.ruta_evento == event_route.id) &
            (Flight.fecha_salida >= fecha_inicio_evento) &
            (Flight.fecha_salida <= fecha_fin_evento)
        ).group_by(SQL("EXTRACT('dow' FROM t2.fecha_salida)")).dicts()


        weekly_capacities_map = {
            int(entry['day_of_week_num']): float(entry['total_capacity_for_day'])
            if isinstance(entry['total_capacity_for_day'], decimal.Decimal) else entry['total_capacity_for_day']
            for entry in flights_weekly_capacity_query
        }

        day_names_map = {
            0: "Domingo",
            1: "Lunes",
            2: "Martes",
            3: "Miércoles",
            4: "Jueves",
            5: "Viernes",
            6: "Sábado"
        }

        # Construir la lista de cobertura por día de la semana
        weekly_coverage_data = []
        for dow_num in range(7):  # Iterar por los 7 días de la semana (0 a 6)
            day_name = day_names_map[dow_num]
            capacidad_ofrecida_semana_dia = weekly_capacities_map.get(dow_num, 0)

            # Cálculo del porcentaje: Capacidad ofrecida para ese DÍA DE LA SEMANA / Demanda TOTAL del evento
            if demanda_estimada > 0:
                percentage = (capacidad_ofrecida_semana_dia / demanda_estimada) * 100
            else:
                percentage = 0.0  # No hay demanda total, no hay porcentaje de cobertura significativo

            weekly_coverage_data.append({
                "day": day_name,
                "coverage": round(percentage, 2)
            })

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
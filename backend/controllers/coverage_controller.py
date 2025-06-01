from backend.services.coverage_service import CoverageService

class CoverageController:
    def __init__(self, coverage_service: CoverageService):
        self.coverage_service = coverage_service

    async def get_dashboard_data(self, user_data, event_id, status_filter=None, page=1, limit=10):

        return await self.coverage_service.calculate_coverage_for_event(
            event_id, status_filter, page, limit
        )

    # Método para obtener los datos detallados de una ruta de evento.
    async def get_route_detail_data(self, ruta_evento_id):

        return await self.coverage_service.get_route_detail(ruta_evento_id)

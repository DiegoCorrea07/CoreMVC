from backend.models.real_coverage import RealCoverage

class RealCoverageRepository:
    @staticmethod
    def create(ruta_evento_id, capacidad_real, porcentaje_cobertura, estado_cobertura, fecha_calculo):
        return RealCoverage.create(
            ruta_evento=ruta_evento_id,
            capacidad_real=capacidad_real,
            porcentaje_cobertura=porcentaje_cobertura,
            estado_cobertura=estado_cobertura,
            fecha_calculo=fecha_calculo
        )

    @staticmethod
    def get_by_id(coverage_id):
        return RealCoverage.get_or_none(RealCoverage.id == coverage_id)

    @staticmethod
    def get_all():
        return list(RealCoverage.select())

    @staticmethod
    def delete(coverage_id):
        coverage = RealCoverage.get_or_none(RealCoverage.id == coverage_id)
        if coverage:
            coverage.delete_instance()
            return True
        return False

    @staticmethod
    def get_latest_for_event_route(ruta_evento_id):
        """Obtiene el cálculo de cobertura más reciente para una EventRoute."""
        return RealCoverage.select().where(RealCoverage.ruta_evento == ruta_evento_id).order_by(
            RealCoverage.fecha_calculo.desc()).get_or_none()
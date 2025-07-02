from backend.models.real_coverage import RealCoverage

class RealCoverageRepository:
    """
    Repositorio para gestionar las operaciones de la base de datos para los cálculos de Cobertura Real.
    Los métodos son de instancia para permitir la Inyección de Dependencias.
    """

    # SE ELIMINA @staticmethod
    def create(self, ruta_evento_id, capacidad_real, porcentaje_cobertura, estado_cobertura, fecha_calculo):
        return RealCoverage.create(
            ruta_evento=ruta_evento_id,
            capacidad_real=capacidad_real,
            porcentaje_cobertura=porcentaje_cobertura,
            estado_cobertura=estado_cobertura,
            fecha_calculo=fecha_calculo
        )

    # SE ELIMINA @staticmethod
    def get_by_id(self, coverage_id):
        return RealCoverage.get_or_none(RealCoverage.id == coverage_id)

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(RealCoverage.select())

    # SE ELIMINA @staticmethod
    def delete(self, coverage_id):
        coverage = RealCoverage.get_or_none(RealCoverage.id == coverage_id)
        if coverage:
            coverage.delete_instance()
            return True
        return False

    # SE ELIMINA @staticmethod
    def get_latest_for_event_route(self, ruta_evento_id):
        """Obtiene el cálculo de cobertura más reciente para una EventRoute."""
        return RealCoverage.select().where(RealCoverage.ruta_evento == ruta_evento_id).order_by(
            RealCoverage.fecha_calculo.desc()).get_or_none()

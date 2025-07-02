from backend.models.coverage_alert import CoverageAlert

class CoverageAlertRepository:
    """
    Repositorio para gestionar las operaciones de la base de datos para las Alertas de Cobertura.
    Los métodos son de instancia para permitir la Inyección de Dependencias.
    """

    # SE ELIMINA @staticmethod
    def create(self, cobertura_id, tipo_alerta, descripcion, fecha_generacion):
        return CoverageAlert.create(
            cobertura=cobertura_id,
            tipo_alerta=tipo_alerta,
            descripcion=descripcion,
            fecha_generacion=fecha_generacion
        )

    # SE ELIMINA @staticmethod
    def get_by_id(self, alert_id):
        return CoverageAlert.get_or_none(CoverageAlert.id == alert_id)

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(CoverageAlert.select())

    # SE ELIMINA @staticmethod
    def delete(self, alert_id):
        alert = CoverageAlert.get_or_none(CoverageAlert.id == alert_id)
        if alert:
            alert.delete_instance()
            return True
        return False

    # SE ELIMINA @staticmethod
    def get_alerts_for_coverage(self, coverage_id):
        return list(CoverageAlert.select().where(CoverageAlert.cobertura == coverage_id))

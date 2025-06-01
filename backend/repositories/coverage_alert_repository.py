from backend.models.coverage_alert import CoverageAlert

class CoverageAlertRepository:
    @staticmethod
    def create(cobertura_id, tipo_alerta, descripcion, fecha_generacion):
        return CoverageAlert.create(
            cobertura=cobertura_id,
            tipo_alerta=tipo_alerta,
            descripcion=descripcion,
            fecha_generacion=fecha_generacion
        )

    @staticmethod
    def get_by_id(alert_id):
        return CoverageAlert.get_or_none(CoverageAlert.id == alert_id)

    @staticmethod
    def get_all():
        return list(CoverageAlert.select())

    @staticmethod
    def delete(alert_id):
        alert = CoverageAlert.get_or_none(CoverageAlert.id == alert_id)
        if alert:
            alert.delete_instance()
            return True
        return False

    @staticmethod
    def get_alerts_for_coverage(coverage_id):
        return list(CoverageAlert.select().where(CoverageAlert.cobertura == coverage_id))
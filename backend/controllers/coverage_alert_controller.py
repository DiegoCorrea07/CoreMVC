from backend.repositories.coverage_alert_repository import CoverageAlertRepository
import datetime

class CoverageAlertController:
    @staticmethod
    def create_alerta_cobertura(cobertura_id, tipo_alerta, descripcion):
        return CoverageAlertRepository.create(cobertura_id, tipo_alerta, descripcion, datetime.datetime.now())

    @staticmethod
    def get_alerta_cobertura(alert_id):
        return CoverageAlertRepository.get_by_id(alert_id)

    @staticmethod
    def list_alerta_coberturas():
        return CoverageAlertRepository.get_all()

    @staticmethod
    def delete_alerta_cobertura(alert_id):
        return CoverageAlertRepository.delete(alert_id)

    @staticmethod
    def get_alerts_for_coverage(coverage_id):
        return CoverageAlertRepository.get_alerts_for_coverage(coverage_id)
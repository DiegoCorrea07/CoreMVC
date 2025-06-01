from backend.repositories.real_coverage_repository import RealCoverageRepository
import datetime


class RealCoverageController:
    @staticmethod
    def create_real_coverage(ruta_evento_id, capacidad_real, porcentaje_cobertura, estado_cobertura):

        return RealCoverageRepository.create(ruta_evento_id, capacidad_real, porcentaje_cobertura, estado_cobertura,
                                             datetime.datetime.now())

    @staticmethod
    def get_real_coverage(coverage_id):
        return RealCoverageRepository.get_by_id(coverage_id)

    @staticmethod
    def list_real_coverages():
        return RealCoverageRepository.get_all()

    @staticmethod
    def delete_real_coverage(coverage_id):
        return RealCoverageRepository.delete(coverage_id)

    @staticmethod
    def get_latest_coverage_for_event_route(ruta_evento_id):
        return RealCoverageRepository.get_latest_for_event_route(ruta_evento_id)
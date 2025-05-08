
from backend.repositories.demand_repository import DemandRepository

class DemandController:
    @staticmethod
    def create_demand(evento_id, ruta_id, demanda_esperada):
        return DemandRepository.create(evento_id, ruta_id, demanda_esperada)

    @staticmethod
    def get_demand(demand_id):
        return DemandRepository.get_by_id(demand_id)

    @staticmethod
    def list_demands():
        return DemandRepository.get_all()

    @staticmethod
    def delete_demand(demand_id):
        return DemandRepository.delete(demand_id)

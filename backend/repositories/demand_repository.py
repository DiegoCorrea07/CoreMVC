
from backend.models.demand import Demand

class DemandRepository:
    @staticmethod
    def create(evento_id, ruta_id, demanda_esperada):
        return Demand.create(
            evento_id=evento_id,
            ruta_id=ruta_id,
            demanda_esperada=demanda_esperada
        )

    @staticmethod
    def get_by_id(demand_id):
        return Demand.get_or_none(Demand.id == demand_id)

    @staticmethod
    def get_all():
        return list(Demand.select())

    @staticmethod
    def delete(demand_id):
        demand = Demand.get_or_none(Demand.id == demand_id)
        if demand:
            demand.delete_instance()
            return True
        return False

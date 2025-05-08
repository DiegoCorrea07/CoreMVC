
from backend.models.aircraft import Aircraft

class AircraftRepository:
    @staticmethod
    def create(matricula, modelo, capacidad):
        return Aircraft.create(matricula=matricula, modelo=modelo, capacidad=capacidad)

    @staticmethod
    def get_by_id(aircraft_id):
        return Aircraft.get_or_none(Aircraft.id == aircraft_id)

    @staticmethod
    def get_all():
        return list(Aircraft.select())

    @staticmethod
    def delete(aircraft_id):
        aircraft = Aircraft.get_or_none(Aircraft.id == aircraft_id)
        if aircraft:
            aircraft.delete_instance()
            return True
        return False

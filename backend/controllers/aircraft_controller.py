from backend.models.aircraft import Aircraft
from backend.repositories.aircraft_repository import AircraftRepository

class AircraftController:
    @staticmethod
    def create_aircraft(matricula, modelo, capacidad):

        existing = Aircraft.get_or_none(Aircraft.matricula == matricula)
        if existing:
            raise ValueError("La matrícula ya existe. No puede repetirse.")

        return AircraftRepository.create(matricula, modelo, capacidad)

    @staticmethod
    def get_aircraft(aircraft_id):
        return AircraftRepository.get_by_id(aircraft_id)

    @staticmethod
    def list_aircrafts():
        return AircraftRepository.get_all()

    @staticmethod
    def delete_aircraft(aircraft_id):
        return AircraftRepository.delete(aircraft_id)

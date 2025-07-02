from backend.models.aircraft import Aircraft


class AircraftController:
    """
    Controlador para orquestar las operaciones de las aeronaves.
    Recibe un repositorio a través de inyección de dependencias.
    """

    # 1. Creamos un constructor que RECIBE el repositorio.
    def __init__(self, repository):
        self.repository = repository

    # 2. Quitamos @staticmethod y usamos 'self' para acceder al repositorio.
    def create_aircraft(self, matricula, modelo, capacidad):

        existing = Aircraft.get_or_none(Aircraft.matricula == matricula)
        if existing:
            raise ValueError("La matrícula ya existe. No puede repetirse.")

        # 3. Usamos la instancia del repositorio que recibimos.
        return self.repository.create(matricula, modelo, capacidad)

    def get_aircraft(self, aircraft_id):
        return self.repository.get_by_id(aircraft_id)

    def list_aircrafts(self):
        return self.repository.get_all()

    def delete_aircraft(self, aircraft_id):
        return self.repository.delete(aircraft_id)

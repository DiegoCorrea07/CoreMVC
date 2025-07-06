from backend.models.aircraft import Aircraft


class AircraftRepository:
    """
    Repositorio para gestionar las operaciones de la base de datos para las Aeronaves.
    Los métodos son de instancia para permitir la Inyección de Dependencias.
    """

    # SE ELIMINA @staticmethod
    def create(self, matricula, modelo, capacidad):
        return Aircraft.create(matricula=matricula, modelo=modelo, capacidad=capacidad)

    # SE ELIMINA @staticmethod
    def get_by_id(self, aircraft_id):
        return Aircraft.get_or_none(Aircraft.id == aircraft_id)

    # SE ELIMINA @staticmethod
    def get_all(self):
        return list(Aircraft.select())

    def update(self, aircraft_id, **kwargs):
        # Filtra los campos permitidos para evitar errores
        allowed_fields = ['matricula', 'modelo', 'capacidad']
        update_data = {k: v for k, v in kwargs.items() if k in allowed_fields}

        query = Aircraft.update(**update_data).where(Aircraft.id == aircraft_id)
        rows_updated = query.execute()
        return rows_updated > 0

    # SE ELIMINA @staticmethod
    def delete(self, aircraft_id):
        aircraft = Aircraft.get_or_none(Aircraft.id == aircraft_id)
        if aircraft:
            aircraft.delete_instance()
            return True
        return False

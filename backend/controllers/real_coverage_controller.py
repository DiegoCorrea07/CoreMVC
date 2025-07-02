import datetime

class RealCoverageController:
    """
    Controlador para orquestar las operaciones de Cobertura Real.
    Recibe un repositorio a través de inyección de dependencias.
    """

    # 1. Creamos un constructor que RECIBE el repositorio.
    def __init__(self, repository):
        self.repository = repository

    # 2. Quitamos @staticmethod y usamos 'self' para acceder al repositorio.
    def create_real_coverage(self, ruta_evento_id, capacidad_real, porcentaje_cobertura, estado_cobertura):
        # La lógica de negocio (como obtener la fecha actual) permanece aquí.
        fecha_calculo = datetime.datetime.now()
        # 3. Usamos la instancia del repositorio que recibimos.
        return self.repository.create(
            ruta_evento_id,
            capacidad_real,
            porcentaje_cobertura,
            estado_cobertura,
            fecha_calculo
        )

    def get_real_coverage(self, coverage_id):
        return self.repository.get_by_id(coverage_id)

    def list_real_coverages(self):
        return self.repository.get_all()

    def delete_real_coverage(self, coverage_id):
        return self.repository.delete(coverage_id)

    def get_latest_coverage_for_event_route(self, ruta_evento_id):
        return self.repository.get_latest_for_event_route(ruta_evento_id)

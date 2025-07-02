import datetime

class CoverageAlertController:
    """
    Controlador para orquestar las operaciones de las Alertas de Cobertura.
    Recibe un repositorio a través de inyección de dependencias.
    """

    # 1. Creamos un constructor que RECIBE el repositorio.
    def __init__(self, repository):
        self.repository = repository

    # 2. Quitamos @staticmethod y usamos 'self' para acceder al repositorio.
    def create_alerta_cobertura(self, cobertura_id, tipo_alerta, descripcion):
        # La lógica de negocio (como obtener la fecha actual) permanece en el controlador.
        fecha_generacion = datetime.datetime.now()
        # 3. Usamos la instancia del repositorio que recibimos.
        return self.repository.create(cobertura_id, tipo_alerta, descripcion, fecha_generacion)

    def get_alerta_cobertura(self, alert_id):
        return self.repository.get_by_id(alert_id)

    def list_alerta_coberturas(self):
        return self.repository.get_all()

    def delete_alerta_cobertura(self, alert_id):
        return self.repository.delete(alert_id)

    def get_alerts_for_coverage(self, coverage_id):
        return self.repository.get_alerts_for_coverage(coverage_id)

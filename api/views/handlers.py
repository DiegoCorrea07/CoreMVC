import traceback
import tornado
from api.utils.auth import authenticated_user, require_permission


class FlightHandler(tornado.web.RequestHandler):
    """
    Handler para el microservicio de Manifiesto.
    Su única responsabilidad es manejar el endpoint del manifiesto.
    """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def get(self, flight_id):
        try:
            # Llama al método del controlador para obtener los datos del manifiesto
            manifest_data = self.controller.get_manifest(int(flight_id))

            if manifest_data:
                # Escribe la respuesta JSON
                self.write(manifest_data)
            else:
                # Si no se encuentra el vuelo, devuelve un error 404
                self.set_status(404)
                self.write({"error": "Vuelo no encontrado para generar manifiesto."})
        except Exception as e:
            # Manejo de errores genérico
            print(f"!!!! ERROR EN MANIFEST HANDLER: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}"})


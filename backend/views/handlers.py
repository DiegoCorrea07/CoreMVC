import json
import tornado.web
import traceback
from backend.utils.serializers import model_to_dict
from peewee import IntegrityError
from backend.utils.auth import authenticated_user, require_permission

class CORSRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class AircraftHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web relacionadas con las aeronaves.
    Recibe una instancia del controlador a través del método initialize.
    """

    # --- CAMBIO 1: Añadir el método initialize ---
    # Recibe la instancia del controlador que se le pasa desde app.py.
    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("gestionar_aeronaves")
    async def get(self, aircraft_id=None):
        try:
            # --- CAMBIO 2: Usar la instancia self.controller ---
            if aircraft_id:
                aircraft = self.controller.get_aircraft(int(aircraft_id))
                if aircraft:
                    self.write({"aircraft": model_to_dict(aircraft)})
                else:
                    self.set_status(404)
                    self.write({"error": "Aeronave no encontrada"})
            else:
                aircrafts = self.controller.list_aircrafts()
                self.write({"aircrafts": [model_to_dict(a) for a in aircrafts]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN AIRCRAFTHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener aeronaves: {str(e)}"})

    @authenticated_user
    @require_permission("gestionar_aeronaves")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            # --- CAMBIO 3: Usar la instancia self.controller ---
            aircraft = self.controller.create_aircraft(data["matricula"], data["modelo"], data["capacidad"])
            self.write({"aircraft": model_to_dict(aircraft)})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except IntegrityError as ie:
            self.set_status(409) # Conflict
            self.write({"error": f"La matrícula ya existe"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN AIRCRAFTHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}"})

    @authenticated_user
    @require_permission("gestionar_aeronaves")
    async def put(self, aircraft_id):
        try:
            data = json.loads(self.request.body)
            updated_aircraft = self.controller.update_aircraft(int(aircraft_id), **data)
            self.write({"aircraft": model_to_dict(updated_aircraft)})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except Exception as e:
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}"})


    @authenticated_user
    @require_permission("gestionar_aeronaves")
    async def delete(self, aircraft_id):
        try:
            # --- CAMBIO 4: Usar la instancia self.controller ---
            success = self.controller.delete_aircraft(int(aircraft_id))
            if success:
                self.set_status(200)
                self.write({"message": "Aeronave eliminada correctamente"})
            else:
                self.set_status(404)
                self.write({"error": "Aeronave no encontrada"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN AIRCRAFTHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar aeronave: {str(e)}"})

class RouteHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web relacionadas con las Rutas geográficas.
    Recibe una instancia del controlador a través del método initialize.
    """

    # --- CAMBIO 1: Añadir el método initialize ---
    # Recibe la instancia del controlador que se le pasa desde app.py.
    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("gestionar_rutas")
    async def get(self, route_id=None):
        try:
            # --- CAMBIO 2: Usar la instancia self.controller ---
            if route_id:
                route = self.controller.get_route(int(route_id))
                if route:
                    self.write({"route": model_to_dict(route)})
                else:
                    self.set_status(404)
                    self.write({"error": "Ruta no encontrada"})
            else:
                routes = self.controller.list_routes()
                self.write({"routes": [model_to_dict(r) for r in routes]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN ROUTEHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener rutas: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_rutas")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            # --- CAMBIO 3: Usar la instancia self.controller ---
            route = self.controller.create_route(data["origen"], data["destino"], data["distancia"])
            self.write({"route": model_to_dict(route)})
        except ValueError as ve:
            # Capturamos los errores de validación del controlador (distancia negativa, etc.)
            self.set_status(400) # Bad Request
            self.write({"error": str(ve)})
        except IntegrityError as ie:
            self.set_status(409) # Conflict
            self.write({"error": f"Error de integridad: {str(ie)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN ROUTEHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_rutas")
    async def put(self, route_id):
        try:
            data = json.loads(self.request.body)
            updated_route = self.controller.update_route(int(route_id), **data)
            self.write({"route": model_to_dict(updated_route)})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except Exception as e:
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}"})


    @authenticated_user
    @require_permission("gestionar_rutas")
    async def delete(self, route_id):
        try:
            # --- CAMBIO 4: Usar la instancia self.controller ---
            success = self.controller.delete_route(int(route_id))
            if success:
                self.write({"message": "Ruta eliminada correctamente"})
            else:
                self.set_status(404)
                self.write({"error": "Ruta no encontrada"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN ROUTEHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar ruta: {str(e)}."})

class FlightHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web relacionadas con los vuelos.
    Esta clase ya no depende de la clase estática FlightController, sino que
    recibe una instancia de un controlador a través del método initialize.
    """

    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def get(self, flight_id=None):
        try:

            if flight_id:
                # Si no es un manifiesto pero tiene ID, es una petición de un solo vuelo.
                flight = self.controller.get_flight(int(flight_id))
                if flight:
                    self.write(model_to_dict(flight))
                else:
                    self.set_status(404)
                    self.write({"error": "Vuelo no encontrado"})
            else:
                # Si no tiene ID, es una petición de todos los vuelos.
                flights = self.controller.list_flights()
                self.write({"flights": [model_to_dict(f) for f in flights]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN FLIGHTHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener datos de vuelos: {str(e)}"})

    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            flight = self.controller.create_flight(
                data["codigo_vuelo"],
                data["aeronave_id"],
                data["ruta_evento_id"],
                data["fecha_salida"],
                data["fecha_llegada"]
            )
            self.write({"flight": model_to_dict(flight)})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except IntegrityError as ie:
            self.set_status(409)
            self.write({"error": f"Error de integridad de datos: {str(ie)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN FLIGHTHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def put(self, flight_id):
        try:
            data = json.loads(self.request.body)
            updated_flight = self.controller.update_flight(int(flight_id), **data)
            self.write({"flight": model_to_dict(updated_flight)})
        except ValueError as ve:
            self.set_status(400)  # Bad Request
            self.write({"error": str(ve)})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN FLIGHTHANDLER.PUT: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}."})


    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def delete(self, flight_id):
        try:
            success = self.controller.delete_flight(int(flight_id))
            if success:
                self.set_status(200)
                self.write({"message": "Vuelo eliminado correctamente"})
            else:
                self.set_status(404)
                self.write({"error": "Vuelo no encontrado"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN FLIGHTHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar vuelo: {str(e)}"})


class UserHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web de gestión de usuarios (listar, registrar, eliminar).
    Recibe una instancia del controlador a través del método initialize.
    """

    # --- CAMBIO 1: Añadir el método initialize ---
    # Recibe la instancia del controlador que se le pasa desde app.py.
    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("gestionar_usuarios")
    async def get(self, user_id=None):
        try:
            # --- CAMBIO 2: Se ajusta para reflejar solo la funcionalidad original ---
            if user_id:
                self.set_status(501)  # Not Implemented
                self.write({"error": "Obtener usuario por ID."})
            else:
                users = self.controller.list_users()
                # Excluimos la contraseña de la respuesta por seguridad.
                self.write({"users": [
                    {"id": u.id, "username": u.username, "role": u.role} for u in users
                ]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN USERHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener usuarios: {str(e)}."})

    async def post(self):
        """Maneja el registro de un nuevo usuario. Este endpoint es público."""
        try:
            data = json.loads(self.request.body)
            # --- CAMBIO 3: Usar la instancia self.controller ---
            user = self.controller.register(data["username"], data["password"], data["role"])
            # Por seguridad, no devolvemos la contraseña hasheada.
            self.write({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }
            })
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except IntegrityError:
            self.set_status(409)
            self.write({"error": "El nombre de usuario ya existe."})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN USERHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_usuarios")
    async def delete(self, user_id):
        try:
            # --- CAMBIO 4: Usar la instancia self.controller ---
            success = self.controller.delete_user(int(user_id))
            if success:
                self.write({"message": "Usuario eliminado correctamente"})
            else:
                self.set_status(404)
                self.write({"error": "Usuario no encontrado"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN USERHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar usuario: {str(e)}."})


class LoginHandler(CORSRequestHandler):
    """
    Handler dedicado exclusivamente para el login de usuarios.
    """

    def initialize(self, controller):
        self.controller = controller

    async def post(self):
        try:
            data = json.loads(self.request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                self.set_status(400)
                self.write({"error": "Usuario y contraseña son requeridos."})
                return

            # --- CAMBIO 5: Usar el método login del controlador, que ahora genera el token ---
            token = self.controller.login(username, password)

            if token:
                # El controlador ahora devuelve el token directamente.
                self.write({"message": "Login successful", "token": token})
            else:
                self.set_status(401)  # Unauthorized
                self.write({"error": "Credenciales inválidas."})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN LOGINHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor durante el login: {str(e)}."})


class EventHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web relacionadas con los Eventos.
    Recibe una instancia del controlador a través del método initialize.
    """

    # --- CAMBIO 1: Añadir el método initialize ---
    # Recibe la instancia del controlador que se le pasa desde app.py.
    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("gestionar_eventos")
    async def get(self, event_id=None):
        try:
            # --- CAMBIO 2: Usar la instancia self.controller ---
            if event_id:
                event = self.controller.get_event(int(event_id))
                if event:
                    self.write({"event": model_to_dict(event)})
                else:
                    self.set_status(404)
                    self.write({"error": "Evento no encontrado"})
            else:
                events = self.controller.list_events()
                self.write({"events": [model_to_dict(e) for e in events]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener eventos: {str(e)}"})

    @authenticated_user
    @require_permission("gestionar_eventos")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            # --- CAMBIO 3: Usar la instancia self.controller ---
            event = self.controller.create_event(
                data["codigo_evento"],
                data["nombre_evento"],
                data["descripcion"],
                data["ciudad_evento"],
                data["fecha_inicio"],
                data["fecha_fin"]
            )
            self.write({"event": model_to_dict(event)})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except IntegrityError:
            self.set_status(409)
            self.write({"error": "El código de evento ya existe."})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}"})

    @authenticated_user
    @require_permission("gestionar_eventos")
    async def put(self, event_id):
        try:
            data = json.loads(self.request.body)
            allowed_fields = [
                "codigo_evento", "nombre_evento", "descripcion",
                "ciudad_evento", "fecha_inicio", "fecha_fin"
            ]
            update_data = {k: v for k, v in data.items() if k in allowed_fields}

            if not update_data:
                self.set_status(400)
                self.write({"error": "No se proporcionaron campos válidos para actualizar."})
                return

            # --- CAMBIO 4: Usar la instancia self.controller ---
            event = self.controller.update_event(int(event_id), **update_data)
            if event:
                self.write({"event": model_to_dict(event)})
            else:
                self.set_status(404)
                self.write({"error": "Evento no encontrado"})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": f"Error en los datos proporcionados: {str(ve)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTHANDLER.PUT: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor al actualizar evento: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_eventos")
    async def delete(self, event_id):
        try:
            # --- CAMBIO 5: Usar la instancia self.controller ---
            success = self.controller.delete_event(int(event_id))
            if success:
                self.write({"message": "Evento eliminado correctamente"})
            else:
                self.set_status(404)
                self.write({"error": "Evento no encontrado"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar evento: {str(e)}"})


class EventRouteHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web relacionadas con las Rutas de Evento.
    Recibe una instancia del controlador a través del método initialize.
    """

    # --- CAMBIO 1: Añadir el método initialize ---
    # Recibe la instancia del controlador que se le pasa desde app.py.
    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("gestionar_demanda")
    async def get(self, event_route_id=None):
        try:
            # --- CAMBIO 2: Usar la instancia self.controller ---
            if event_route_id:
                event_route = self.controller.get_event_route(int(event_route_id))
                if event_route:
                    self.write({"event_route": model_to_dict(event_route)})
                else:
                    self.set_status(404)
                    self.write({"error": "Ruta de evento no encontrada"})
            else:
                event_routes = self.controller.list_event_routes()
                self.write({"event_routes": [model_to_dict(er) for er in event_routes]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTROUTEHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener rutas de evento: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_demanda")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            # --- CAMBIO 3: Usar la instancia self.controller ---
            event_route = self.controller.create_event_route(
                data["ruta_id"],
                data["evento_id"],
                data["demanda_estimada"]
            )
            self.write({"event_route": model_to_dict(event_route)})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except IntegrityError as ie:
            self.set_status(409)
            self.write({"error": f"Error de integridad: {str(ie)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTROUTEHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_demanda")
    async def put(self, event_route_id):
        try:
            data = json.loads(self.request.body)

            # Pasamos el diccionario 'data' completo usando **data
            updated_event_route = self.controller.update_event_route(int(event_route_id), **data)

            # Usamos model_to_dict para serializar la respuesta
            self.write({"event_route": model_to_dict(updated_event_route)})

        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTROUTEHANDLER.PUT: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}."})

    @authenticated_user
    @require_permission("gestionar_demanda")
    async def delete(self, event_route_id):
        try:
            # --- CAMBIO 5: Usar la instancia self.controller ---
            success = self.controller.delete_event_route(int(event_route_id))
            if success:
                self.write({"message": "Ruta de evento eliminada correctamente"})
            else:
                self.set_status(404)
                self.write({"error": "Ruta de evento no encontrada"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTROUTEHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar la ruta de evento: {str(e)}."})


class RealCoverageHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web relacionadas con la Cobertura Real.
    Recibe una instancia del controlador a través del método initialize.
    """

    # --- CAMBIO 1: Añadir el método initialize ---
    # Recibe la instancia del controlador que se le pasa desde app.py.
    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("consultar_panel")
    async def get(self, coverage_id=None):
        """
        Maneja las peticiones GET para obtener una o todas las coberturas reales.
        También puede obtener la última cobertura para una ruta de evento específica.
        Ej: GET /real_coverages?event_route_id=5
        """
        try:
            event_route_id = self.get_query_argument("event_route_id", None)

            # --- CAMBIO 2: Usar la instancia self.controller ---
            if coverage_id:
                coverage = self.controller.get_real_coverage(int(coverage_id))
                if coverage:
                    self.write({"coverage": model_to_dict(coverage)})
                else:
                    self.set_status(404)
                    self.write({"error": "Cobertura real no encontrada"})
            elif event_route_id:
                coverage = self.controller.get_latest_coverage_for_event_route(int(event_route_id))
                if coverage:
                    self.write({"coverage": model_to_dict(coverage)})
                else:
                    self.set_status(404)
                    self.write({"error": "No se encontró cobertura para la ruta de evento especificada."})
            else:
                coverages = self.controller.list_real_coverages()
                self.write({"coverages": [model_to_dict(c) for c in coverages]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN REALCOVERAGEHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener coberturas reales: {str(e)}."})

class CoverageAlertHandler(CORSRequestHandler):
    """
    Handler para gestionar las peticiones web relacionadas con las Alertas de Cobertura.
    Recibe una instancia del controlador a través del método initialize.
    """

    # --- CAMBIO 1: Añadir el método initialize ---
    # Recibe la instancia del controlador que se le pasa desde app.py.
    def initialize(self, controller):
        self.controller = controller

    @authenticated_user
    @require_permission("ver_alertas")
    async def get(self, alert_id=None):
        """
        Maneja las peticiones GET para obtener una o todas las alertas.
        También puede obtener alertas para una cobertura específica si se pasa el query param 'coverage_id'.
        Ej: GET /coverage_alert?coverage_id=1
        """
        try:
            coverage_id = self.get_query_argument("coverage_id", None)

            # --- CAMBIO 2: Usar la instancia self.controller ---
            if alert_id:
                alert = self.controller.get_alerta_cobertura(int(alert_id))
                if alert:
                    self.write({"alert": model_to_dict(alert)})
                else:
                    self.set_status(404)
                    self.write({"error": "Alerta no encontrada"})
            elif coverage_id:
                alerts = self.controller.get_alerts_for_coverage(int(coverage_id))
                self.write({"alerts": [model_to_dict(a) for a in alerts]})
            else:
                alerts = self.controller.list_alerta_coberturas()
                self.write({"alerts": [model_to_dict(a) for a in alerts]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN COVERAGEALERTHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write(
                {"error": f"Error al obtener alertas de cobertura: {str(e)}."})


# ---- HANDLER PRINCIPAL DEL CORE ----
class CoverageHandler(CORSRequestHandler):
    def initialize(self, coverage_controller):
        self.coverage_controller = coverage_controller

    @authenticated_user
    @require_permission("consultar_panel")
    async def get(self, ruta_evento_id=None):
        try:
            user_data = self.current_user
            if not user_data:
                self.set_status(401)
                self.write(json.dumps({"message": "No autenticado."}))
                return

            if ruta_evento_id:
                try:
                    ruta_evento_id = int(ruta_evento_id)
                except ValueError:
                    self.set_status(400)
                    self.write(json.dumps({"message": "El ID de la ruta de evento debe ser un número entero."}))
                    return

                data = await self.coverage_controller.get_route_detail_data(ruta_evento_id)

                if data is None:
                    self.set_status(404)
                    self.write(json.dumps({"message": f"Detalle de ruta con ID {ruta_evento_id} no encontrado."}))
                    return
            else:
                event_id = self.get_query_argument("event_id", None)
                status_filter = self.get_query_argument("status_filter", None)
                page = self.get_query_argument("page", "1")
                limit = self.get_query_argument("limit", "10")

                if event_id:
                    try:
                        event_id = int(event_id)
                    except ValueError:
                        self.set_status(400)
                        self.write(json.dumps(
                            {"message": "El parámetro 'event_id' debe ser un número entero válido si se proporciona."}))
                        return

                try:
                    page = int(page)
                    limit = int(limit)
                except ValueError:
                    self.set_status(400)
                    self.write(json.dumps(
                        {"message": "Los parámetros 'page' y 'limit' deben ser números enteros válidos."}))
                    return

                data = await self.coverage_controller.get_dashboard_data(
                    user_data, event_id, status_filter, page, limit
                )

            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(data))

        except ValueError as e:
            self.set_status(400)
            self.write(json.dumps({"message": str(e)}))

        except Exception as e:
            print(f"!!!! ERROR NO MANEJADO EN COVERAGEHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write(json.dumps(
                {"message": f"Error interno del servidor. Consulte los logs del servidor para más detalles."}))

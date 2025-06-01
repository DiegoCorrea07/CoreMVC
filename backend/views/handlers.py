import json
import jwt
import tornado.web
import traceback
from backend.utils.config import Config
from backend.utils.serializers import model_to_dict
from peewee import IntegrityError
from backend.utils.auth import authenticated_user, require_permission
from backend.controllers.aircraft_controller import AircraftController
from backend.controllers.route_controller import RouteController
from backend.controllers.flight_controller import FlightController
from backend.controllers.user_controller import UserController
from backend.controllers.event_controller import EventController
from backend.controllers.event_route_controller import EventRouteController
from backend.controllers.real_coverage_controller import RealCoverageController
from backend.controllers.coverage_alert_controller import CoverageAlertController

class CORSRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class AircraftHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("gestionar_aeronaves")
    async def get(self, aircraft_id=None):
        try:
            if aircraft_id:
                aircraft = AircraftController.get_aircraft(int(aircraft_id))
                if aircraft:
                    self.write({"aircraft": model_to_dict(aircraft)})
                else:
                    self.set_status(404)
                    self.write({"message": "Aircraft not found"})
            else:
                aircrafts = AircraftController.list_aircrafts()
                self.write({"aircrafts": [model_to_dict(a) for a in aircrafts]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN AIRCRAFTHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener aeronaves: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_aeronaves")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            aircraft = AircraftController.create_aircraft(data["matricula"], data["modelo"], data["capacidad"])
            self.write({"aircraft": model_to_dict(aircraft)}) # Usar model_to_dict
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except IntegrityError as ie:
            self.set_status(409)
            self.write({"error": f"La matrícula ya existe: {str(ie)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN AIRCRAFTHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_aeronaves")
    async def delete(self, aircraft_id):
        try:
            success = AircraftController.delete_aircraft(int(aircraft_id))
            if success:
                self.write({"message": "Aircraft deleted"})
            else:
                self.set_status(404)
                self.write({"message": "Aircraft not found"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN AIRCRAFTHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar aeronave: {str(e)}. Verifique la consola del servidor."})


class RouteHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("gestionar_rutas")
    async def get(self, route_id=None): # Añadir id opcional
        try:
            if route_id:
                route = RouteController.get_route(int(route_id))
                if route:
                    self.write({"route": model_to_dict(route)})
                else:
                    self.set_status(404)
                    self.write({"message": "Route not found"})
            else:
                routes = RouteController.list_routes()
                self.write({"routes": [model_to_dict(r) for r in routes]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN ROUTEHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener rutas: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_rutas")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            route = RouteController.create_route(data["origen"], data["destino"], data["distancia"])
            self.write({"route": model_to_dict(route)})
        except IntegrityError as ie:
            self.set_status(409)
            self.write({"error": f"Error de integridad: {str(ie)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN ROUTEHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_rutas")
    async def delete(self, route_id):
        try:
            success = RouteController.delete_route(int(route_id))
            if success:
                self.write({"message": "Route deleted"})
            else:
                self.set_status(404)
                self.write({"message": "Route not found"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN ROUTEHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar ruta: {str(e)}. Verifique la consola del servidor."})


class FlightHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def get(self):
        try:
            flights = FlightController.list_flights()
            self.write({"flights": [model_to_dict(f) for f in flights]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN FLIGHTHANDLER.GET: {e} !!!!")
            traceback.print_exc() # Añadir traceback
            self.set_status(500)
            self.write({"error": f"Error al obtener vuelos: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            flight = FlightController.create_flight(
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
            traceback.print_exc() # Añadir traceback
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_vuelos")
    async def delete(self, flight_id):
        try:
            success = FlightController.delete_flight(int(flight_id))
            if success:
                self.write({"message": "Flight deleted"})
            else:
                self.set_status(404)
                self.write({"message": "Flight not found"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN FLIGHTHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar vuelo: {str(e)}. Verifique la consola del servidor."})


class UserHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("gestionar_usuarios")
    async def get(self, user_id=None):
        try:
            if user_id:
                user = UserController.get_user(int(user_id))
                if user:
                    self.write({"user": model_to_dict(user)})
                else:
                    self.set_status(404)
                    self.write({"message": "User not found"})
            else:
                users = UserController.list_users()
                self.write({"users": [model_to_dict(u) for u in users]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN USERHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener usuarios: {str(e)}. Verifique la consola del servidor."})

    async def post(self):
        try:
            data = json.loads(self.request.body)
            user = UserController.register(data["username"], data["password"], data["role"])
            self.write({"user": model_to_dict(user)}) # Usar model_to_dict
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except IntegrityError as ie:
            self.set_status(409)
            self.write({"error": f"El nombre de usuario ya existe: {str(ie)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN USERHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_usuarios")
    async def delete(self, user_id):
        try:
            success = UserController.delete_user(int(user_id))
            if success:
                self.write({"message": "User deleted"})
            else:
                self.set_status(404)
                self.write({"message": "User not found"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN USERHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar usuario: {str(e)}. Verifique la consola del servidor."})


class LoginHandler(CORSRequestHandler):
    async def post(self):
        try:
            data = json.loads(self.request.body)
            user = UserController.authenticate(data["username"], data["password"])
            if user:
                payload = {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role
                }
                token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
                self.write({"message": "Login successful", "token": token})
            else:
                self.set_status(401)
                self.write({"message": "Invalid credentials"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN LOGINHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error de autenticación: {str(e)}. Verifique la consola del servidor."})


class EventHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("gestionar_eventos")
    async def get(self, event_id=None):
        try:
            if event_id:
                event = EventController.get_event(int(event_id))
                if event:
                    self.write({"event": model_to_dict(event)})
                else:
                    self.set_status(404)
                    self.write({"message": "Event not found"})
            else:
                events = EventController.list_events()
                self.write({"events": [model_to_dict(e) for e in events]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener eventos: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_eventos")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            event = EventController.create_event(
                data["codigo_evento"],
                data["nombre_evento"],
                data["descripcion"],
                data["fecha_inicio"],
                data["fecha_fin"]
            )
            self.write({"event": model_to_dict(event)})
        except IntegrityError as ie:
            self.set_status(409)
            self.write({"error": f"El código de evento ya existe: {str(ie)}"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTHANDLER.POST: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_eventos")
    async def delete(self, event_id):
        try:
            success = EventController.delete_event(int(event_id))
            if success:
                self.write({"message": "Event deleted"})
            else:
                self.set_status(404)
                self.write({"message": "Event not found"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar evento: {str(e)}. Verifique la consola del servidor."})

class EventRouteHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("gestionar_demanda")
    async def get(self, event_route_id=None):
        try:
            if event_route_id:
                event_route = EventRouteController.get_event_route(int(event_route_id))
                if event_route:
                    self.write({"event_route": model_to_dict(event_route)})
                else:
                    self.set_status(404)
                    self.write({"message": "Event Route not found"})
            else:
                event_routes = EventRouteController.list_event_routes()
                self.write({"event_routes": [model_to_dict(er) for er in event_routes]})
        except Exception as e: # Este ya tenía el try-except completo.
            print(f"\n!!!! ERROR CAPTURADO EN EVENTROUTEHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener rutas de evento: {str(e)}. Verifique la consola del servidor para más detalles."})

    @authenticated_user
    @require_permission("gestionar_demanda")
    async def post(self):
        try:
            data = json.loads(self.request.body)
            event_route = EventRouteController.create_event_route(
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
            self.write({"error": f"Error interno del servidor: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_demanda")
    async def put(self, event_route_id):
        try:
            data = json.loads(self.request.body)
            event_route = EventRouteController.update_event_route(int(event_route_id), data["demanda_estimada"])
            self.write({"event_route": model_to_dict(event_route)})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTROUTEHANDLER.PUT: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error interno del servidor: {str(e)}. Verifique la consola del servidor."})

    @authenticated_user
    @require_permission("gestionar_demanda")
    async def delete(self, event_route_id):
        try:
            success = EventRouteController.delete_event_route(int(event_route_id))
            if success:
                self.write({"message": "Event Route deleted"})
            else:
                self.set_status(404)
                self.write({"message": "Event Route not found"})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN EVENTROUTEHANDLER.DELETE: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al eliminar ruta de evento: {str(e)}. Verifique la consola del servidor."})


class RealCoverageHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("consultar_panel")
    async def get(self, coverage_id=None):
        try:
            if coverage_id:
                coverage = RealCoverageController.get_real_coverage(int(coverage_id))
                if coverage:
                    self.write({"coverage": model_to_dict(coverage)})
                else:
                    self.set_status(404)
                    self.write({"message": "Real Coverage not found"})
            else:
                coverages = RealCoverageController.list_real_coverages()
                self.write({"coverages": [model_to_dict(c) for c in coverages]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN REALCOVERAGEHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener coberturas reales: {str(e)}. Verifique la consola del servidor."})


class CoverageAlertHandler(CORSRequestHandler):
    @authenticated_user
    @require_permission("ver_alertas")
    async def get(self, alert_id=None):
        try:
            if alert_id:
                alert = CoverageAlertController.get_alerta_cobertura(int(alert_id))
                if alert:
                    self.write({"alert": model_to_dict(alert)})
                else:
                    self.set_status(404)
                    self.write({"message": "Alert not found"})
            else:
                alerts = CoverageAlertController.list_alerta_coberturas()
                self.write({"alerts": [model_to_dict(a) for a in alerts]})
        except Exception as e:
            print(f"\n!!!! ERROR CAPTURADO EN COVERAGEALERTHANDLER.GET: {e} !!!!")
            traceback.print_exc()
            self.set_status(500)
            self.write({"error": f"Error al obtener alertas de cobertura: {str(e)}. Verifique la consola del servidor."})


# ---- HANDLER PRINCIPAL DEL CORE ----
class CoverageHandler(CORSRequestHandler):
    def initialize(self, coverage_controller):
        self.coverage_controller = coverage_controller

    @authenticated_user
    @require_permission("consultar_panel")
    async def get(self, ruta_evento_id=None):
        try:
            # Obtención de user_data (de tu BaseHandler o decorador @authenticated_user)
            user_data = self.current_user
            if not user_data:
                self.set_status(401)
                self.write(json.dumps({"message": "No autenticado."}))
                return

            if ruta_evento_id:
                # Si ruta_evento_id está presente, es la solicitud de detalle de ruta
                try:
                    ruta_evento_id = int(ruta_evento_id)
                except ValueError:
                    self.set_status(400)
                    self.write(json.dumps({"message": "El ID de la ruta de evento debe ser un número entero."}))
                    return

                data = await self.coverage_controller.get_route_detail_data(ruta_evento_id)

                if data is None:  # Si el servicio devuelve None, significa que no se encontró la ruta
                    self.set_status(404)
                    self.write(json.dumps({"message": f"Detalle de ruta con ID {ruta_evento_id} no encontrado."}))
                    return
            else:
                # Si ruta_evento_id es None, es la solicitud del dashboard
                event_id = self.get_query_argument("event_id", None)
                status_filter = self.get_query_argument("status", None)  # Tu frontend envía 'status'
                page = self.get_query_argument("page", "1")
                limit = self.get_query_argument("limit", "10")

                if not event_id:
                    self.set_status(400)
                    self.write(json.dumps({"message": "El parámetro 'event_id' es requerido para el dashboard."}))
                    return

                try:
                    event_id = int(event_id)
                    page = int(page)
                    limit = int(limit)
                except ValueError:
                    self.set_status(400)
                    self.write(json.dumps(
                        {"message": "Los parámetros 'event_id', 'page' y 'limit' deben ser números enteros válidos."}))
                    return

                data = await self.coverage_controller.get_dashboard_data(
                    user_data, event_id, status_filter, page, limit
                )

            # Establecer el tipo de contenido y enviar la respuesta JSON
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(data))

        except ValueError as e:  # Para errores de validación de IDs o formatos (adicionales a los try-except internos)
            self.set_status(400)
            self.write(json.dumps({"message": str(e)}))

        except Exception as e:
            # Captura cualquier otra excepción no manejada y devuelve un error 500
            print(f"!!!! ERROR NO MANEJADO EN COVERAGEHANDLER.GET: {e} !!!!")
            traceback.print_exc()  # Imprime el stack trace completo para depuración
            self.set_status(500)
            self.write(json.dumps(
                {"message": f"Error interno del servidor. Consulte los logs del servidor para más detalles."}))


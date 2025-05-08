import json
import jwt
import tornado.web
from backend.utils.config import Config
from backend.utils.serializers import model_to_dict

from backend.controllers.aircraft_controller import AircraftController
from backend.controllers.route_controller import RouteController
from backend.controllers.flight_controller import FlightController
from backend.controllers.demand_controller import DemandController
from backend.controllers.user_controller import UserController
from backend.controllers.event_controller import EventController

class CORSRequestHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()

class AircraftHandler(CORSRequestHandler):
    async def get(self):
        aircrafts = AircraftController.list_aircrafts()
        self.write({"aircrafts": [a.__data__ for a in aircrafts]})

    async def post(self):
        try:
            data = json.loads(self.request.body)
            aircraft = AircraftController.create_aircraft(data["matricula"], data["modelo"], data["capacidad"])
            self.write({"aircraft": aircraft.__data__})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})

    async def delete(self, aircraft_id):
        success = AircraftController.delete_aircraft(int(aircraft_id))
        if success:
            self.write({"message": "Aircraft deleted"})
        else:
            self.set_status(404)
            self.write({"message": "Aircraft not found"})

class RouteHandler(CORSRequestHandler):
    async def get(self):
        routes = RouteController.list_routes()
        self.write({"routes": [r.__data__ for r in routes]})

    async def post(self):
        data = json.loads(self.request.body)
        route = RouteController.create_route(data["origen"], data["destino"], data["distancia"])
        self.write({"route": route.__data__})

    async def delete(self, route_id):
        success = RouteController.delete_route(int(route_id))
        if success:
            self.write({"message": "Route deleted"})
        else:
            self.set_status(404)
            self.write({"message": "Route not found"})

class FlightHandler(CORSRequestHandler):
    async def get(self):
        flights = FlightController.list_flights()
        self.write({"flights": [model_to_dict(f) for f in flights]})

    async def post(self):
        try:
            data = json.loads(self.request.body)
            flight = FlightController.create_flight(
                data["codigo_vuelo"],
                data["aeronave_id"],
                data["ruta_id"],
                data["evento_id"],
                data["fecha_salida"],
                data["fecha_llegada"]
            )
            self.write({"flight": flight.__data__})
        except ValueError as ve:
            self.set_status(400)
            self.write({"error": str(ve)})

    async def delete(self, flight_id):
        success = FlightController.delete_flight(int(flight_id))
        if success:
            self.write({"message": "Flight deleted"})
        else:
            self.set_status(404)
            self.write({"message": "Flight not found"})

class DemandHandler(CORSRequestHandler):
    async def get(self):
        demands = DemandController.list_demands()
        self.write({"demands": [model_to_dict(d) for d in demands]})

    async def post(self):
        data = json.loads(self.request.body)
        demand = DemandController.create_demand(
            data["evento_id"],
            data["ruta_id"],
            data["demanda_esperada"]
        )
        self.write({"demand": demand.__data__})

    async def delete(self, demand_id):
        success = DemandController.delete_demand(int(demand_id))
        if success:
            self.write({"message": "Demand deleted"})
        else:
            self.set_status(404)
            self.write({"message": "Demand not found"})

class UserHandler(CORSRequestHandler):
    async def get(self):
        users = UserController.list_users()
        self.write({"users": [u.__data__ for u in users]})

    async def post(self):
        data = json.loads(self.request.body)
        user = UserController.register(data["username"], data["password"], data["role"])
        self.write({"user": user.__data__})

    async def delete(self, user_id):
        success = UserController.delete_user(int(user_id))
        if success:
            self.write({"message": "User deleted"})
        else:
            self.set_status(404)
            self.write({"message": "User not found"})

class LoginHandler(CORSRequestHandler):
    async def post(self):
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

class EventHandler(CORSRequestHandler):
    async def get(self):
        events = EventController.list_events()
        self.write({"events": [model_to_dict(e) for e in events]})

    async def post(self):
        data = json.loads(self.request.body)
        event = EventController.create_event(
            data["codigo_evento"],
            data["nombre_evento"],
            data["descripcion"],
            data["fecha_inicio"],
            data["fecha_fin"]
        )
        self.write({"event": event.__data__})

    async def delete(self, event_id):
        success = EventController.delete_event(int(event_id))
        if success:
            self.write({"message": "Event deleted"})
        else:
            self.set_status(404)
            self.write({"message": "Event not found"})


import tornado.ioloop
import tornado.web
import signal

# --- 1. IMPORTACIONES ---
from backend.views.handlers import (
    AircraftHandler, RouteHandler, FlightHandler, UserHandler, EventHandler,
    LoginHandler, EventRouteHandler, RealCoverageHandler, CoverageAlertHandler,
    CoverageHandler, CORSRequestHandler
)
from backend.controllers.aircraft_controller import AircraftController
from backend.controllers.route_controller import RouteController
from backend.controllers.flight_controller import FlightController
from backend.controllers.user_controller import UserController
from backend.controllers.event_controller import EventController
from backend.controllers.event_route_controller import EventRouteController
from backend.controllers.real_coverage_controller import RealCoverageController
from backend.controllers.coverage_alert_controller import CoverageAlertController
from backend.controllers.coverage_controller import CoverageController
from backend.repositories.aircraft_repository import AircraftRepository
from backend.repositories.route_repository import RouteRepository
from backend.repositories.flight_repository import FlightRepository
from backend.repositories.user_repository import UserRepository
from backend.repositories.event_repository import EventRepository
from backend.repositories.event_route_repository import EventRouteRepository
from backend.repositories.real_coverage_repository import RealCoverageRepository
from backend.repositories.coverage_alert_repository import CoverageAlertRepository
from backend.services.coverage_service import CoverageService
from backend.utils.init_db import initialize_tables
from backend.db.connection import db
from backend.utils.config import Config


def make_app():
    """
    Función principal que crea e inicializa todas las dependencias de la aplicación.
    Este es el "Composition Root" donde se ensambla todo.
    """
    # --- 2. CREACIÓN DE INSTANCIAS ---

    # Primero, se crean todas las dependencias de bajo nivel (repositorios)
    aircraft_repo = AircraftRepository()
    route_repo = RouteRepository()
    flight_repo = FlightRepository()
    user_repo = UserRepository()
    event_repo = EventRepository()
    event_route_repo = EventRouteRepository()
    real_coverage_repo = RealCoverageRepository()
    coverage_alert_repo = CoverageAlertRepository()
    coverage_service = CoverageService(
        real_coverage_repo=real_coverage_repo,
        coverage_alert_repo=coverage_alert_repo
    )

    # Finalmente, se crean los controladores, inyectando sus dependencias (repositorios o servicios)
    aircraft_controller = AircraftController(repository=aircraft_repo)
    route_controller = RouteController(repository=route_repo)
    flight_controller = FlightController(repository=flight_repo, event_route_repo=event_route_repo)
    user_controller = UserController(repository=user_repo, secret_key=Config.SECRET_KEY)
    event_controller = EventController(repository=event_repo)
    event_route_controller = EventRouteController(repository=event_route_repo)
    real_coverage_controller = RealCoverageController(repository=real_coverage_repo)
    coverage_alert_controller = CoverageAlertController(repository=coverage_alert_repo)
    coverage_controller = CoverageController(coverage_service=coverage_service)


    # --- 3. DEFINICIÓN DE RUTAS Y ENSAMBLAJE FINAL ---
    # A cada ruta se le pasa su handler y el controlador correspondiente.
    return tornado.web.Application([
        (r"/aircrafts", AircraftHandler, {"controller": aircraft_controller}),
        (r"/aircrafts/([0-9]+)", AircraftHandler, {"controller": aircraft_controller}),
        (r"/routes", RouteHandler, {"controller": route_controller}),
        (r"/routes/([0-9]+)", RouteHandler, {"controller": route_controller}),
        (r"/flights", FlightHandler, {"controller": flight_controller}),
        (r"/flights/([0-9]+)", FlightHandler, {"controller": flight_controller}),
        (r"/users", UserHandler, {"controller": user_controller}),
        (r"/users/([0-9]+)", UserHandler, {"controller": user_controller}),
        (r"/events", EventHandler, {"controller": event_controller}),
        (r"/events/([0-9]+)", EventHandler, {"controller": event_controller}),
        (r"/login", LoginHandler, {"controller": user_controller}),
        (r"/event_routes", EventRouteHandler, {"controller": event_route_controller}),
        (r"/event_routes/([0-9]+)", EventRouteHandler, {"controller": event_route_controller}),
        (r"/real_coverages", RealCoverageHandler, {"controller": real_coverage_controller}),
        (r"/real_coverages/([0-9]+)", RealCoverageHandler, {"controller": real_coverage_controller}),
        (r"/coverage_alert", CoverageAlertHandler, {"controller": coverage_alert_controller}),
        (r"/coverage_alert/([0-9]+)", CoverageAlertHandler, {"controller": coverage_alert_controller}),
        (r"/coverage/dashboard", CoverageHandler, {"coverage_controller": coverage_controller}),
        (r"/coverage/route_detail/([0-9]+)", CoverageHandler, {"coverage_controller": coverage_controller}),

        #Nueva Funcionalidad
        #(r"/api/flights/([0-9]+)/manifest", FlightHandler, {"controller": flight_controller}),
    ],
        default_handler_class=CORSRequestHandler,
        debug=True
    )


if __name__ == "__main__":
    initialize_tables()
    app = make_app()
    app.listen(8888)
    print("Servidor corriendo en http://localhost:8888")

    def shutdown_hook():
        if not db.is_closed():
            db.close()
        print("Cerrando la base de datos y deteniendo el servidor.")
        tornado.ioloop.IOLoop.current().stop()

    signal.signal(signal.SIGINT, lambda sig, frame: tornado.ioloop.IOLoop.current().add_callback_from_signal(shutdown_hook))
    signal.signal(signal.SIGTERM, lambda sig, frame: tornado.ioloop.IOLoop.current().add_callback_from_signal(shutdown_hook))

    tornado.ioloop.IOLoop.current().start()

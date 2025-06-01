import tornado.ioloop
import tornado.web
from backend.controllers.coverage_controller import CoverageController
from backend.views.handlers import (
    AircraftHandler,
    RouteHandler,
    FlightHandler,
    UserHandler,
    EventHandler,
    CORSRequestHandler,
    LoginHandler,
    EventRouteHandler,
    RealCoverageHandler,
    CoverageAlertHandler,
    CoverageHandler
)
from backend.utils.init_db import initialize_tables
from backend.db.connection import db
from backend.services.coverage_service import CoverageService

coverage_service = CoverageService()
coverage_controller_instance = CoverageController(coverage_service)

def make_app():

    return tornado.web.Application([
        (r"/aircrafts", AircraftHandler),
        (r"/aircrafts/([0-9]+)", AircraftHandler),
        (r"/routes", RouteHandler),
        (r"/routes/([0-9]+)", RouteHandler),
        (r"/flights", FlightHandler),
        (r"/flights/([0-9]+)", FlightHandler),
        (r"/users", UserHandler),
        (r"/users/([0-9]+)", UserHandler),
        (r"/events", EventHandler),
        (r"/events/([0-9]+)", EventHandler),
        (r"/login", LoginHandler),
        (r"/event_routes", EventRouteHandler),
        (r"/event_routes/([0-9]+)", EventRouteHandler),
        (r"/real_coverages", RealCoverageHandler),
        (r"/real_coverages/([0-9]+)", RealCoverageHandler),
        (r"/coverage_alert", CoverageAlertHandler),
        (r"/coverage_alert/([0-9]+)", CoverageAlertHandler),

        # Rutas del CORE de Cobertura
        (r"/coverage/dashboard", CoverageHandler, {"coverage_controller": coverage_controller_instance}),
        (r"/coverage/route_detail/([0-9]+)", CoverageHandler, {"coverage_controller": coverage_controller_instance}),
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

    import signal

    signal.signal(signal.SIGINT,
                  lambda sig, frame: tornado.ioloop.IOLoop.current().add_callback_from_signal(shutdown_hook))
    signal.signal(signal.SIGTERM,
                  lambda sig, frame: tornado.ioloop.IOLoop.current().add_callback_from_signal(shutdown_hook))

    tornado.ioloop.IOLoop.current().start()
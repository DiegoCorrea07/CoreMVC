
import tornado.ioloop
import tornado.web
from backend.views.handlers import (
    AircraftHandler,
    RouteHandler,
    FlightHandler,
    DemandHandler,
    UserHandler,
    EventHandler,
    CORSRequestHandler,
    LoginHandler
)
from backend.utils.init_db import initialize_tables

def make_app():
    return tornado.web.Application([
        (r"/aircrafts", AircraftHandler),
        (r"/aircrafts/([0-9]+)", AircraftHandler),
        (r"/routes", RouteHandler),
        (r"/routes/([0-9]+)", RouteHandler),
        (r"/flights", FlightHandler),
        (r"/flights/([0-9]+)", FlightHandler),
        (r"/demands", DemandHandler),
        (r"/demands/([0-9]+)", DemandHandler),
        (r"/users", UserHandler),
        (r"/users/([0-9]+)", UserHandler),
        (r"/events", EventHandler),
        (r"/events/([0-9]+)", EventHandler),
        (r"/login", LoginHandler),
    ], default_handler_class=CORSRequestHandler)

if __name__ == "__main__":
    initialize_tables()
    app = make_app()
    app.listen(8888)
    print("Servidor corriendo en http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

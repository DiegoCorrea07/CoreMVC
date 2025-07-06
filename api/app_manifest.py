import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import tornado.ioloop
import tornado.web
import signal

from controllers.flight_controller import FlightController
from repositories.flight_repository import FlightRepository
from repositories.real_coverage_repository import RealCoverageRepository
from views.handlers import FlightHandler
from utils.init_db import initialize_tables
from db.connection import db


def make_manifest_app():
    # Inyección de dependencias para este microservicio
    flight_repo = FlightRepository()
    real_coverage_repo = RealCoverageRepository()

    flight_controller = FlightController(
        repository=flight_repo,
        real_coverage_repo=real_coverage_repo
    )

    return tornado.web.Application([
        (r"/api/flights/([0-9]+)/manifest", FlightHandler, {"controller": flight_controller}),
    ])


if __name__ == "__main__":
    initialize_tables()
    app = make_manifest_app()
    app.listen(8889)
    print("Servidor de Manifiesto API corriendo en http://localhost:8889")
    tornado.ioloop.IOLoop.current().start()

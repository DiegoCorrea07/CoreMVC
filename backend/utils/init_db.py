from backend.db.connection import db
from backend.models.user import User
from backend.models.aircraft import Aircraft
from backend.models.route import Route
from backend.models.event import Event
from backend.models.event_route import EventRoute
from backend.models.flight import Flight
from backend.models.real_coverage import RealCoverage
from backend.models.coverage_alert import CoverageAlert


def initialize_tables():
    """
    Inicializa la conexión a la base de datos y crea las tablas si no existen.
    Asegura el orden correcto de creación para respetar las claves foráneas.
    """
    if db.is_closed():
        db.connect()

    print("Verificando/creando tablas de la base de datos...")

    db.create_tables([
        User,
        Aircraft,
        Route,
        Event,
        EventRoute,
        Flight,
        RealCoverage,
        CoverageAlert
    ], safe=True)
    print("Tablas de la base de datos verificadas/creadas exitosamente.")

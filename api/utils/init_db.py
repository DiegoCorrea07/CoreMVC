from api.db.connection import db
from api.models.user import User
from api.models.aircraft import Aircraft
from api.models.route import Route
from api.models.event import Event
from api.models.event_route import EventRoute
from api.models.flight import Flight
from api.models.real_coverage import RealCoverage
from api.models.coverage_alert import CoverageAlert


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

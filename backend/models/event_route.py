from peewee import Model, ForeignKeyField, DecimalField, PrimaryKeyField
from backend.db.connection import db
from backend.models.route import Route
from backend.models.event import Event

class EventRoute(Model):
    ruta = ForeignKeyField(Route, backref='rutas_en_eventos', on_delete='CASCADE')
    evento = ForeignKeyField(Event, backref='eventos_con_rutas', on_delete='CASCADE')
    demanda_estimada = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        database = db
        table_name = 'rutas_eventos'
        indexes = (
            # Asegura que no haya duplicados de la misma ruta en el mismo evento
            (('ruta', 'evento'), True),
        )
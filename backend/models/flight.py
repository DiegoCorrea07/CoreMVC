
from peewee import Model, CharField, DateTimeField, ForeignKeyField
from backend.db.connection import db
from backend.models.aircraft import Aircraft
from backend.models.route import Route
from backend.models.event import Event

class Flight(Model):
    codigo_vuelo = CharField(unique=True, max_length=20)
    fecha_salida = DateTimeField()
    fecha_llegada = DateTimeField()
    aeronave_id = ForeignKeyField(Aircraft, backref='vuelos', null=True)
    ruta_id = ForeignKeyField(Route, backref='vuelos', null=True)
    evento_id = ForeignKeyField(Event, backref='vuelos', null=True)

    class Meta:
        database = db
        table_name = 'vuelos'

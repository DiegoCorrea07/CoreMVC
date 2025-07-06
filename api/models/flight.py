from peewee import Model, CharField, DateTimeField, ForeignKeyField
from api.db.connection import db
from api.models.aircraft import Aircraft
from api.models.event_route import EventRoute

class Flight(Model):
    codigo_vuelo = CharField(unique=True, max_length=20)
    fecha_salida = DateTimeField()
    fecha_llegada = DateTimeField()
    aeronave = ForeignKeyField(Aircraft, backref='vuelos', null=True)
    ruta_evento = ForeignKeyField(EventRoute, backref='vuelos', null=True) 

    class Meta:
        database = db
        table_name = 'vuelos'
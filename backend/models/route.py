from peewee import Model, CharField, IntegerField
from backend.db.connection import db

class Route(Model):
    origen = CharField(max_length=100)
    destino = CharField(max_length=100)
    distancia = IntegerField()

    class Meta:
        database = db
        table_name = 'rutas'

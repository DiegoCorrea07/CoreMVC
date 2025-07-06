from peewee import Model, CharField, TextField, DateField
from api.db.connection import db

class Event(Model):
    codigo_evento = CharField(unique=True, max_length=20)
    nombre_evento = CharField(max_length=100)
    descripcion = TextField(null=True)
    ciudad_evento = TextField(null=True)
    fecha_inicio = DateField()
    fecha_fin = DateField()

    class Meta:
        database = db
        table_name = 'eventos'

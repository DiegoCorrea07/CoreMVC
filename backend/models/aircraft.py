
from peewee import Model, CharField, IntegerField
from backend.db.connection import db

class Aircraft(Model):
    matricula = CharField(unique=True, max_length=20)
    modelo = CharField(max_length=50)
    capacidad = IntegerField()

    class Meta:
        database = db
        table_name = 'aeronaves'

from peewee import Model, CharField
from api.db.connection import db

class User(Model):
    username = CharField(unique=True, max_length=50)
    password = CharField(max_length=100)
    role = CharField(max_length=20)  # administrador o planificador

    class Meta:
        database = db
        table_name = 'usuarios'

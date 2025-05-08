
from peewee import Model, ForeignKeyField, IntegerField, DecimalField
from backend.db.connection import db
from backend.models.flight import Flight

class Demand(Model):
    evento_id = ForeignKeyField(Flight, backref='demanda', on_delete='CASCADE')
    ruta_id = ForeignKeyField(Flight, backref='demanda', on_delete='CASCADE')
    demanda_esperada = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        database = db
        table_name = 'demanda_estimadas'

from peewee import Model, ForeignKeyField, IntegerField, DecimalField, CharField, DateTimeField
from api.db.connection import db
from api.models.event_route import EventRoute

class RealCoverage(Model):
    ruta_evento = ForeignKeyField(EventRoute, backref='coberturas_reales', on_delete='CASCADE')
    capacidad_real = IntegerField()
    porcentaje_cobertura = DecimalField(max_digits=5, decimal_places=2)
    estado_cobertura = CharField(max_length=20)
    fecha_calculo = DateTimeField()

    class Meta:
        database = db
        table_name = 'cobertura_real'
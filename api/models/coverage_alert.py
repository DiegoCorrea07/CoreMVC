from peewee import Model, ForeignKeyField, CharField, TextField, DateTimeField
from api.db.connection import db
from api.models.real_coverage import RealCoverage

class CoverageAlert(Model):
    cobertura = ForeignKeyField(RealCoverage, backref='alertas', on_delete='CASCADE')
    tipo_alerta = CharField(max_length=20)
    descripcion = TextField()
    fecha_generacion = DateTimeField()

    class Meta:
        database = db
        table_name = 'alertas_cobertura'
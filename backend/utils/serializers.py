import datetime
import decimal
from peewee import Model, ForeignKeyField

def model_to_dict(model_instance, exclude_fields=None, include_related=True):
    """
    Convierte una instancia de un modelo Peewee a un diccionario,
    manejando campos de clave foránea y tipos de datos especiales.
    """
    if not isinstance(model_instance, Model):
        return model_instance

    data = {}
    if exclude_fields is None:
        exclude_fields = set()

    if 'id' not in exclude_fields and hasattr(model_instance, 'id'):
        data['id'] = model_instance.id

    for field_name, field_obj in model_instance._meta.fields.items():
        if field_name in exclude_fields:
            continue

        value = getattr(model_instance, field_name)

        if isinstance(field_obj, ForeignKeyField):

            if value is not None:
                if isinstance(value, Model):
                    data[f"{field_name}_id"] = value.id
                else:
                    data[f"{field_name}_id"] = value
            else:
                data[f"{field_name}_id"] = None


            if include_related and isinstance(value, Model):
                data[field_name] = model_to_dict(value, exclude_fields={'id'}, include_related=False)
            elif isinstance(value, Model):
                data[field_name] = model_to_dict(value, exclude_fields={'id'}, include_related=False)
            else:
                data[field_name] = value
        else:
            if isinstance(value, (datetime.datetime, datetime.date)):
                data[field_name] = value.isoformat()
            elif isinstance(value, decimal.Decimal):
                data[field_name] = float(value)
            else:
                data[field_name] = value

    return data


def list_to_dicts(model_list):
    """
    Convierte una lista de instancias de modelos Peewee a una lista de diccionarios.
    Utiliza model_to_dict para cada elemento.
    """
    from peewee import ModelSelect
    if not isinstance(model_list, (list, ModelSelect)):
        raise TypeError("Se esperaba una lista o un objeto ModelSelect de Peewee.")

    return [model_to_dict(item) for item in model_list]
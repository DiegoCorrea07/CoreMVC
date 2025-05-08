import datetime
import decimal

def model_to_dict(obj):
    data = obj.__data__.copy()
    for k, v in data.items():
        if isinstance(v, (datetime.date, datetime.datetime)):
            data[k] = v.isoformat()
        elif isinstance(v, decimal.Decimal):
            data[k] = float(v)
    return data

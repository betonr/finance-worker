"""
validation of worker controllers schemas
"""

from cerberus import Validator
from api.utils.validators import to_date

def download_balance():
    return {
        'session_id': {"type": "string", "required": True, "empty": False}
    }

def quota():
    return {
        'start_date': {"type": "date", "coerce": to_date, "required": True, "empty": False},
        'last_date': {"type": "date", "coerce": to_date, "required": True, "empty": False},
        'only_last_quota': {"type": "boolean", "required": False, "default": False}
    }

def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))
    
    v = Validator(schema)
    if not v.validate(data):
        return v.errors, False
    return data, True

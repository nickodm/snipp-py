VERSION = "2.21.2"
from decimal import Decimal
from fastjsonschema import JsonSchemaValueException


NoneType = type(None)

def validate(data, custom_formats={}, name_prefix=None):
    if not isinstance(data, (dict)):
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be object", value=data, name="" + (name_prefix or "data") + "", definition={'$schema': 'https://json-schema.org/draft-07/schema', 'title': 'SnippFile Meta Index', 'description': 'The index of the parts of a snipp file.', 'type': 'object', 'additionalProperties': {'type': 'object', 'required': ['pos', 'size'], 'properties': {'pos': {'type': 'integer', 'description': 'The position where the part starts.', 'minimum': 0}, 'size': {'type': 'integer', 'description': 'The size of the part.', 'minimum': 0}}}}, rule='type')
    data_is_dict = isinstance(data, dict)
    if data_is_dict:
        data_keys = set(data.keys())
        for data_key in data_keys:
            if data_key not in []:
                data_value = data.get(data_key)
                if not isinstance(data_value, (dict)):
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".{data_key}".format(**locals()) + " must be object", value=data_value, name="" + (name_prefix or "data") + ".{data_key}".format(**locals()) + "", definition={'type': 'object', 'required': ['pos', 'size'], 'properties': {'pos': {'type': 'integer', 'description': 'The position where the part starts.', 'minimum': 0}, 'size': {'type': 'integer', 'description': 'The size of the part.', 'minimum': 0}}}, rule='type')
                data_value_is_dict = isinstance(data_value, dict)
                if data_value_is_dict:
                    data_value__missing_keys = set(['pos', 'size']) - data_value.keys()
                    if data_value__missing_keys:
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".{data_key}".format(**locals()) + " must contain " + (str(sorted(data_value__missing_keys)) + " properties"), value=data_value, name="" + (name_prefix or "data") + ".{data_key}".format(**locals()) + "", definition={'type': 'object', 'required': ['pos', 'size'], 'properties': {'pos': {'type': 'integer', 'description': 'The position where the part starts.', 'minimum': 0}, 'size': {'type': 'integer', 'description': 'The size of the part.', 'minimum': 0}}}, rule='required')
                    data_value_keys = set(data_value.keys())
                    if "pos" in data_value_keys:
                        data_value_keys.remove("pos")
                        data_value__pos = data_value["pos"]
                        if not isinstance(data_value__pos, (int)) and not (isinstance(data_value__pos, float) and data_value__pos.is_integer()) or isinstance(data_value__pos, bool):
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".{data_key}.pos".format(**locals()) + " must be integer", value=data_value__pos, name="" + (name_prefix or "data") + ".{data_key}.pos".format(**locals()) + "", definition={'type': 'integer', 'description': 'The position where the part starts.', 'minimum': 0}, rule='type')
                        if isinstance(data_value__pos, (int, float, Decimal)):
                            if data_value__pos < 0:
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".{data_key}.pos".format(**locals()) + " must be bigger than or equal to 0", value=data_value__pos, name="" + (name_prefix or "data") + ".{data_key}.pos".format(**locals()) + "", definition={'type': 'integer', 'description': 'The position where the part starts.', 'minimum': 0}, rule='minimum')
                    if "size" in data_value_keys:
                        data_value_keys.remove("size")
                        data_value__size = data_value["size"]
                        if not isinstance(data_value__size, (int)) and not (isinstance(data_value__size, float) and data_value__size.is_integer()) or isinstance(data_value__size, bool):
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".{data_key}.size".format(**locals()) + " must be integer", value=data_value__size, name="" + (name_prefix or "data") + ".{data_key}.size".format(**locals()) + "", definition={'type': 'integer', 'description': 'The size of the part.', 'minimum': 0}, rule='type')
                        if isinstance(data_value__size, (int, float, Decimal)):
                            if data_value__size < 0:
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".{data_key}.size".format(**locals()) + " must be bigger than or equal to 0", value=data_value__size, name="" + (name_prefix or "data") + ".{data_key}.size".format(**locals()) + "", definition={'type': 'integer', 'description': 'The size of the part.', 'minimum': 0}, rule='minimum')
    return data
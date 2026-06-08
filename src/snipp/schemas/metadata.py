VERSION = "2.21.2"
from decimal import Decimal
from fastjsonschema import JsonSchemaValueException


NoneType = type(None)

def validate(data, custom_formats={}, name_prefix=None):
    if not isinstance(data, (dict)):
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be object", value=data, name="" + (name_prefix or "data") + "", definition={'$schema': 'https://json-schema.org/draft-07/schema', 'title': 'Snippet Metadata Schema', 'type': 'object', 'additionalProperties': False, 'required': ['snippet-info', 'software-info'], 'properties': {'snippet-info': {'type': 'object', 'additionalProperties': False, 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'id': {'type': 'string', 'minLength': 36, 'maxLength': 36}, 'description': {'type': 'string'}, 'git_init': {'type': 'boolean', 'default': False}, 'creation_date': {'type': 'integer'}}}, 'software-info': {'type': 'object', 'additionalProperties': False, 'required': ['version'], 'properties': {'version': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}}}}}, rule='type')
    data_is_dict = isinstance(data, dict)
    if data_is_dict:
        data__missing_keys = set(['snippet-info', 'software-info']) - data.keys()
        if data__missing_keys:
            raise JsonSchemaValueException("" + (name_prefix or "data") + " must contain " + (str(sorted(data__missing_keys)) + " properties"), value=data, name="" + (name_prefix or "data") + "", definition={'$schema': 'https://json-schema.org/draft-07/schema', 'title': 'Snippet Metadata Schema', 'type': 'object', 'additionalProperties': False, 'required': ['snippet-info', 'software-info'], 'properties': {'snippet-info': {'type': 'object', 'additionalProperties': False, 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'id': {'type': 'string', 'minLength': 36, 'maxLength': 36}, 'description': {'type': 'string'}, 'git_init': {'type': 'boolean', 'default': False}, 'creation_date': {'type': 'integer'}}}, 'software-info': {'type': 'object', 'additionalProperties': False, 'required': ['version'], 'properties': {'version': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}}}}}, rule='required')
        data_keys = set(data.keys())
        if "snippet-info" in data_keys:
            data_keys.remove("snippet-info")
            data__snippetinfo = data["snippet-info"]
            if not isinstance(data__snippetinfo, (dict)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info must be object", value=data__snippetinfo, name="" + (name_prefix or "data") + ".snippet-info", definition={'type': 'object', 'additionalProperties': False, 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'id': {'type': 'string', 'minLength': 36, 'maxLength': 36}, 'description': {'type': 'string'}, 'git_init': {'type': 'boolean', 'default': False}, 'creation_date': {'type': 'integer'}}}, rule='type')
            data__snippetinfo_is_dict = isinstance(data__snippetinfo, dict)
            if data__snippetinfo_is_dict:
                data__snippetinfo__missing_keys = set(['name']) - data__snippetinfo.keys()
                if data__snippetinfo__missing_keys:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info must contain " + (str(sorted(data__snippetinfo__missing_keys)) + " properties"), value=data__snippetinfo, name="" + (name_prefix or "data") + ".snippet-info", definition={'type': 'object', 'additionalProperties': False, 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'id': {'type': 'string', 'minLength': 36, 'maxLength': 36}, 'description': {'type': 'string'}, 'git_init': {'type': 'boolean', 'default': False}, 'creation_date': {'type': 'integer'}}}, rule='required')
                data__snippetinfo_keys = set(data__snippetinfo.keys())
                if "name" in data__snippetinfo_keys:
                    data__snippetinfo_keys.remove("name")
                    data__snippetinfo__name = data__snippetinfo["name"]
                    if not isinstance(data__snippetinfo__name, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info.name must be string", value=data__snippetinfo__name, name="" + (name_prefix or "data") + ".snippet-info.name", definition={'type': 'string'}, rule='type')
                if "id" in data__snippetinfo_keys:
                    data__snippetinfo_keys.remove("id")
                    data__snippetinfo__id = data__snippetinfo["id"]
                    if not isinstance(data__snippetinfo__id, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info.id must be string", value=data__snippetinfo__id, name="" + (name_prefix or "data") + ".snippet-info.id", definition={'type': 'string', 'minLength': 36, 'maxLength': 36}, rule='type')
                    if isinstance(data__snippetinfo__id, str):
                        data__snippetinfo__id_len = len(data__snippetinfo__id)
                        if data__snippetinfo__id_len < 36:
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info.id must be longer than or equal to 36 characters", value=data__snippetinfo__id, name="" + (name_prefix or "data") + ".snippet-info.id", definition={'type': 'string', 'minLength': 36, 'maxLength': 36}, rule='minLength')
                        if data__snippetinfo__id_len > 36:
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info.id must be shorter than or equal to 36 characters", value=data__snippetinfo__id, name="" + (name_prefix or "data") + ".snippet-info.id", definition={'type': 'string', 'minLength': 36, 'maxLength': 36}, rule='maxLength')
                if "description" in data__snippetinfo_keys:
                    data__snippetinfo_keys.remove("description")
                    data__snippetinfo__description = data__snippetinfo["description"]
                    if not isinstance(data__snippetinfo__description, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info.description must be string", value=data__snippetinfo__description, name="" + (name_prefix or "data") + ".snippet-info.description", definition={'type': 'string'}, rule='type')
                if "git_init" in data__snippetinfo_keys:
                    data__snippetinfo_keys.remove("git_init")
                    data__snippetinfo__gitinit = data__snippetinfo["git_init"]
                    if not isinstance(data__snippetinfo__gitinit, (bool)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info.git_init must be boolean", value=data__snippetinfo__gitinit, name="" + (name_prefix or "data") + ".snippet-info.git_init", definition={'type': 'boolean', 'default': False}, rule='type')
                else: data__snippetinfo["git_init"] = False
                if "creation_date" in data__snippetinfo_keys:
                    data__snippetinfo_keys.remove("creation_date")
                    data__snippetinfo__creationdate = data__snippetinfo["creation_date"]
                    if not isinstance(data__snippetinfo__creationdate, (int)) and not (isinstance(data__snippetinfo__creationdate, float) and data__snippetinfo__creationdate.is_integer()) or isinstance(data__snippetinfo__creationdate, bool):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info.creation_date must be integer", value=data__snippetinfo__creationdate, name="" + (name_prefix or "data") + ".snippet-info.creation_date", definition={'type': 'integer'}, rule='type')
                if data__snippetinfo_keys:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".snippet-info must not contain "+str(data__snippetinfo_keys)+" properties", value=data__snippetinfo, name="" + (name_prefix or "data") + ".snippet-info", definition={'type': 'object', 'additionalProperties': False, 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'id': {'type': 'string', 'minLength': 36, 'maxLength': 36}, 'description': {'type': 'string'}, 'git_init': {'type': 'boolean', 'default': False}, 'creation_date': {'type': 'integer'}}}, rule='additionalProperties')
        if "software-info" in data_keys:
            data_keys.remove("software-info")
            data__softwareinfo = data["software-info"]
            if not isinstance(data__softwareinfo, (dict)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".software-info must be object", value=data__softwareinfo, name="" + (name_prefix or "data") + ".software-info", definition={'type': 'object', 'additionalProperties': False, 'required': ['version'], 'properties': {'version': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}}}, rule='type')
            data__softwareinfo_is_dict = isinstance(data__softwareinfo, dict)
            if data__softwareinfo_is_dict:
                data__softwareinfo__missing_keys = set(['version']) - data__softwareinfo.keys()
                if data__softwareinfo__missing_keys:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".software-info must contain " + (str(sorted(data__softwareinfo__missing_keys)) + " properties"), value=data__softwareinfo, name="" + (name_prefix or "data") + ".software-info", definition={'type': 'object', 'additionalProperties': False, 'required': ['version'], 'properties': {'version': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}}}, rule='required')
                data__softwareinfo_keys = set(data__softwareinfo.keys())
                if "version" in data__softwareinfo_keys:
                    data__softwareinfo_keys.remove("version")
                    data__softwareinfo__version = data__softwareinfo["version"]
                    if not isinstance(data__softwareinfo__version, (list, tuple)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".software-info.version must be array", value=data__softwareinfo__version, name="" + (name_prefix or "data") + ".software-info.version", definition={'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}, rule='type')
                    data__softwareinfo__version_is_list = isinstance(data__softwareinfo__version, (list, tuple))
                    if data__softwareinfo__version_is_list:
                        data__softwareinfo__version_len = len(data__softwareinfo__version)
                        if data__softwareinfo__version_len < 3:
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".software-info.version must contain at least 3 items", value=data__softwareinfo__version, name="" + (name_prefix or "data") + ".software-info.version", definition={'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}, rule='minItems')
                        if data__softwareinfo__version_len > 5:
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".software-info.version must contain less than or equal to 5 items", value=data__softwareinfo__version, name="" + (name_prefix or "data") + ".software-info.version", definition={'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}, rule='maxItems')
                    data__softwareinfo__version_is_dict = isinstance(data__softwareinfo__version, dict)
                    if data__softwareinfo__version_is_dict:
                        data__softwareinfo__version__missing_keys = set(['Major', 'Minor', 'Patch', 'Stage', 'Stage Number']) - data__softwareinfo__version.keys()
                        if data__softwareinfo__version__missing_keys:
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".software-info.version must contain " + (str(sorted(data__softwareinfo__version__missing_keys)) + " properties"), value=data__softwareinfo__version, name="" + (name_prefix or "data") + ".software-info.version", definition={'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}, rule='required')
                if data__softwareinfo_keys:
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".software-info must not contain "+str(data__softwareinfo_keys)+" properties", value=data__softwareinfo, name="" + (name_prefix or "data") + ".software-info", definition={'type': 'object', 'additionalProperties': False, 'required': ['version'], 'properties': {'version': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}}}, rule='additionalProperties')
        if data_keys:
            raise JsonSchemaValueException("" + (name_prefix or "data") + " must not contain "+str(data_keys)+" properties", value=data, name="" + (name_prefix or "data") + "", definition={'$schema': 'https://json-schema.org/draft-07/schema', 'title': 'Snippet Metadata Schema', 'type': 'object', 'additionalProperties': False, 'required': ['snippet-info', 'software-info'], 'properties': {'snippet-info': {'type': 'object', 'additionalProperties': False, 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'id': {'type': 'string', 'minLength': 36, 'maxLength': 36}, 'description': {'type': 'string'}, 'git_init': {'type': 'boolean', 'default': False}, 'creation_date': {'type': 'integer'}}}, 'software-info': {'type': 'object', 'additionalProperties': False, 'required': ['version'], 'properties': {'version': {'type': 'array', 'minItems': 3, 'maxItems': 5, 'required': ['Major', 'Minor', 'Patch', 'Stage', 'Stage Number'], 'prefixItems': [{'name': 'Major', 'type': 'integer'}, {'name': 'Minor', 'type': 'integer'}, {'name': 'Patch', 'type': 'integer'}, {'name': 'Stage', 'enum': ['alpha', 'beta', 'rc', 'final']}, {'name': 'Stage Number', 'type': 'integer'}]}}}}}, rule='additionalProperties')
    return data
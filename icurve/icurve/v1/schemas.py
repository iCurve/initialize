# -*- coding: utf-8 -*-

# TODO: datetime support

###
### DO NOT CHANGE THIS FILE
###
### The code is auto generated, your change will be overwritten by
### code generating.
###

base_path = '/v1'


DefinitionsCommonresponse = {'required': ['msg', 'server', 'traceId'], 'description': u'\u8fd4\u56de\u503c\u7684\u901a\u7528\u5b57\u6bb5', 'properties': {'msg': {'type': 'string'}, 'traceId': {'type': 'string'}, 'server': {'type': 'string'}}}
DefinitionsAction = {'properties': {'action': {'enum': ['foo'], 'type': 'string'}, 'name': {'enum': [u'\u5360\u4f4d\u64cd\u4f5c'], 'type': 'string'}}}
DefinitionsTrend = {'properties': {'type': {'type': 'string'}, 'data': {'xml': {'wrapped': True, 'name': 'point'}, 'items': {'xml': {'wrapped': True, 'name': 'value'}, 'minItems': 2, 'type': 'array', 'maxItems': 3, 'items': {'type': 'number'}}, 'type': 'array'}, 'name': {'type': 'string'}}}
DefinitionsTime = {'type': 'integer', 'description': u'unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7', 'format': 'int64'}
DefinitionsThumbresponse = {'required': ['data'], 'allOf': [DefinitionsCommonresponse, {'properties': {'data': DefinitionsTrend}}]}
DefinitionsTimeslot = {'required': ['start', 'end'], 'description': u'\u65f6\u95f4\u6bb5', 'properties': {'start': DefinitionsTime, 'end': DefinitionsTime}}
DefinitionsTrendresponse = {'required': ['data'], 'allOf': [DefinitionsCommonresponse, {'properties': {'data': {'items': DefinitionsTrend, 'type': 'array'}}}]}
DefinitionsTooltipresponse = {'required': ['data'], 'allOf': [DefinitionsCommonresponse, {'properties': {'data': {'xml': {'wrapped': True, 'name': 'tooltip'}, 'items': DefinitionsAction, 'type': 'array'}}}]}
DefinitionsBandtime = {'required': ['duration'], 'properties': {'duration': DefinitionsTimeslot, 'show': DefinitionsTimeslot}}
DefinitionsMeta = {'required': ['name'], 'description': u'\u6570\u636e\u7684\u5143\u4fe1\u606f', 'properties': {'updateTime': DefinitionsTime, 'name': {'type': 'string'}, 'uri': {'type': 'string', 'description': u'\u4e0b\u8f7d\u6570\u636e\u7684url'}, 'period': {'required': ['length', 'ratio'], 'description': u'\u6570\u636e\u7684\u5468\u671f', 'properties': {'length': {'type': 'integer', 'description': u'\u6570\u636e\u7684\u5468\u671f\uff0c\u5355\u4f4d\uff1a\u79d2', 'format': 'int64'}, 'ratio': {'type': 'number', 'description': u'\u7b26\u5408\u5468\u671f\u7684\u6570\u636e\u5360\u6bd4', 'format': 'float'}}}, 'labelRatio': {'type': 'number', 'description': u'\u6807\u6ce8\u6570\u636e\u7684\u5360\u6bd4', 'format': 'float'}, 'time': DefinitionsTimeslot, 'id': {'type': 'integer', 'format': 'int64'}, 'createTime': DefinitionsTime}}
DefinitionsBanditems = {'xml': {'wrapped': True, 'name': 'band'}, 'items': {'required': ['timeno', 'bandcount', 'time'], 'properties': {'nextTime': DefinitionsBandtime, 'bandCount': {'type': 'integer', 'format': 'int64'}, 'preTime': DefinitionsBandtime, 'reliablity': {'type': 'number', 'description': u'\u63cf\u8ff0\u6240\u751f\u6210 band \u7684\u53ef\u4fe1\u7a0b\u5ea6', 'format': 'float'}, 'currentTime': DefinitionsBandtime, 'timeNo': {'type': 'integer', 'format': 'int64'}}}, 'type': 'array'}
DefinitionsDatalistresponse = {'required': ['data'], 'allOf': [DefinitionsCommonresponse, {'properties': {'data': {'xml': {'wrapped': True, 'name': 'meta'}, 'items': DefinitionsMeta, 'type': 'array'}}}]}
DefinitionsBandcategory = {'properties': {'bands': DefinitionsBanditems, 'name': {'type': 'string'}}}
DefinitionsBandresponse = {'required': ['data'], 'allOf': [DefinitionsCommonresponse, {'properties': {'data': DefinitionsBanditems}}]}

validators = {
    ('data_dataName_label', 'PUT'): {'args': {'required': ['startTime', 'endTime'], 'properties': {'endTime': {'description': u'\u7ed3\u675f\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}, 'startTime': {'description': u'\u5f00\u59cb\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}}}, 'form': {'required': ['label'], 'properties': {'label': {'description': u'\u6807\u6ce8\u7c7b\u578b', 'format': 'int64', 'enum': [0, 1, -1], 'type': 'integer'}}}},
    ('data_dataName_band_bandName', 'GET'): {'args': {'required': ['startTime', 'endTime'], 'properties': {'endTime': {'description': u'\u7ed3\u675f\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}, 'order': {'description': u'\u6392\u5e8f\u4f9d\u636e', 'default': 'time', 'enum': ['time', 'reliablity'], 'type': 'string'}, 'startTime': {'description': u'\u5f00\u59cb\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}}}},
    ('data_dataName', 'PUT'): {'args': {'required': ['startTime', 'endTime'], 'properties': {'endTime': {'description': u'\u7ed3\u675f\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}, 'startTime': {'description': u'\u5f00\u59cb\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}}}, 'form': {'required': ['action'], 'properties': {'action': {'description': u'\u6570\u636e\u64cd\u4f5c\u540d\u79f0', 'enum': ['foo'], 'type': 'string'}}}},
    ('data_dataName', 'POST'): {'form': {'required': ['file'], 'properties': {'file': {'type': 'file', 'description': u'\u539f\u59cb\u6570\u636e\u6587\u4ef6'}}}},
    ('datas', 'GET'): {'args': {'required': [], 'properties': {'pattern': {'type': 'string', 'description': u'\u6570\u636e\u540d\u79f0\u5339\u914d\u89c4\u5219'}}}},
    ('data_dataName_curves', 'GET'): {'args': {'required': ['startTime', 'endTime'], 'properties': {'endTime': {'description': u'\u7ed3\u675f\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}, 'bandName': {'type': 'string', 'description': u'band\u540d\u79f0'}, 'startTime': {'description': u'\u5f00\u59cb\u65f6\u95f4(unix\u65f6\u95f4\u6233\uff0c\u6beb\u79d2\u7ea7)', 'format': 'int64', 'default': 0, 'type': 'integer'}}}},
}

filters = {
    ('data_dataName_label', 'PUT'): {200: {'headers': None, 'schema': DefinitionsCommonresponse}, 404: {'headers': None, 'schema': DefinitionsCommonresponse}, 422: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('data_dataName_band_bandName', 'GET'): {200: {'headers': None, 'schema': DefinitionsBandresponse}, 404: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('data_dataName_band_bandName', 'DELETE'): {200: {'headers': None, 'schema': DefinitionsCommonresponse}, 404: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('tooltips', 'GET'): {200: {'headers': None, 'schema': DefinitionsTooltipresponse}},
    ('data_dataName', 'PUT'): {200: {'headers': None, 'schema': DefinitionsCommonresponse}, 404: {'headers': None, 'schema': DefinitionsCommonresponse}, 422: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('data_dataName', 'POST'): {201: {'headers': {'Location': {'type': 'string', 'description': u'\u6570\u636e uri'}}, 'schema': DefinitionsCommonresponse}, 422: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('data_dataName', 'GET'): {200: {'headers': None, 'schema': {'type': 'file'}}, 404: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('data_dataName', 'DELETE'): {404: {'headers': None, 'schema': DefinitionsCommonresponse}, 405: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('datas', 'GET'): {200: {'headers': None, 'schema': DefinitionsDatalistresponse}},
    ('data_dataName_thumb', 'GET'): {200: {'headers': None, 'schema': DefinitionsThumbresponse}, 404: {'headers': None, 'schema': DefinitionsCommonresponse}},
    ('data_dataName_curves', 'GET'): {200: {'headers': None, 'schema': DefinitionsTrendresponse}, 404: {'headers': None, 'schema': DefinitionsCommonresponse}},
}

scopes = {
}


class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value, get_first=True):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    results = normalize(schema, value, type_defaults)
    if get_first:
        return results[0]
    return results


def normalize(schema, data, required_defaults=None):

    import six

    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            return getattr(self.data, key, default)

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

        def keys(self):
            if isinstance(self.data, dict):
                return list(self.data.keys())
            return list(getattr(self.data, '__dict__', {}).keys())

        def get_check(self, key, default=None):
            if isinstance(self.data, dict):
                value = self.data.get(key, default)
                has_key = key in self.data
            else:
                try:
                    value = getattr(self.data, key)
                except AttributeError:
                    value = default
                    has_key = False
                else:
                    has_key = True
            return value, has_key

    def _merge_dict(src, dst):
        for k, v in six.iteritems(dst):
            if isinstance(src, dict):
                if isinstance(v, dict):
                    r = _merge_dict(src.get(k, {}), v)
                    src[k] = r
                else:
                    src[k] = v
            else:
                src = {k: v}
        return src

    def _normalize_dict(schema, data):
        result = {}
        if not isinstance(data, DataWrapper):
            data = DataWrapper(data)

        for _schema in schema.get('allOf', []):
            rs_component = _normalize(_schema, data)
            _merge_dict(result, rs_component)

        for key, _schema in six.iteritems(schema.get('properties', {})):
            # set default
            type_ = _schema.get('type', 'object')

            # get value
            value, has_key = data.get_check(key)
            if has_key:
                result[key] = _normalize(_schema, value)
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                if type_ in required_defaults:
                    result[key] = required_defaults[type_]
                else:
                    errors.append(dict(name='property_missing',
                                       message='`%s` is required' % key))

        additional_properties_schema = schema.get('additionalProperties', False)
        if additional_properties_schema:
            aproperties_set = set(data.keys()) - set(result.keys())
            for pro in aproperties_set:
                result[pro] = _normalize(additional_properties_schema, data.get(pro))

        return result

    def _normalize_list(schema, data):
        result = []
        if hasattr(data, '__iter__') and not isinstance(data, dict):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize(schema, data):
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
        }
        type_ = schema.get('type', 'object')
        if not type_ in funcs:
            type_ = 'default'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors

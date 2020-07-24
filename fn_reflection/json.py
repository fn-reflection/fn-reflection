import json


class DatetimeJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if type(o).__name__ == 'datetime':
            return o.isoformat()
        else:
            return o


def extend_dumps(obj, **kwargs):
    kwargs['cls'] = DatetimeJSONEncoder
    return json.dumps(obj, **kwargs)

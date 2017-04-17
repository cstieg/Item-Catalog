import json


def success():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
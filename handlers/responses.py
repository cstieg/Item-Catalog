"""HTTP Responses"""

import json

def success():
    """Returns success HTTP response"""
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
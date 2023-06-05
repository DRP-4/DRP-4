from flask import Response, json


def json_response(payload, status=200):
    r = Response(json.dumps(payload))
    r.headers["Content-Type"] = "application/json"
    r.status_code = status
    return r

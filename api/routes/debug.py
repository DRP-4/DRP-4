from app import app, running_as_dev
from flask import request, abort
import util.now


@app.route("/api/debug/jump-seconds", methods=["POST"])
def jump():
    body = request.get_json()
    if (
        not running_as_dev
        or "seconds" not in body
        or not isinstance(body["seconds"], int)
    ):
        abort(400)
    util.now.delta = body["seconds"]
    return "", 204

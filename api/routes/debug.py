from app import app, running_as_dev
from flask import request, abort
import util.now

@app.route("/api/debug/jump-seconds", methods=["POST"])
def jump():
    if not running_as_dev:
        abort(400)
    body = request.get_json()
    util.now.delta += body["seconds"]
    return "", 204

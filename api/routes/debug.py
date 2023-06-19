from app import app, running_as_dev, socketio
from flask import request, abort
from util.response import json_response
from os import environ
import util.now

allow_jumps = running_as_dev or "ALLOW_JUMPS" in environ


@app.route("/api/debug/jump-seconds", methods=["GET"])
def get_delta():
    return json_response({"seconds": util.now.delta})


@app.route("/api/debug/jump-seconds", methods=["POST"])
def jump():
    body = request.get_json()
    if not allow_jumps:
        return "Forbidden", 403
    elif "seconds" not in body or not isinstance(body["seconds"], int):
        return "Bad Request", 400
    util.now.delta = body["seconds"]
    socketio.emit("jump-seconds", {"seconds": util.now.delta})
    return "", 204

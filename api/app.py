import flask

app = flask.Flask(__name__)


def json_responce(payload, status=200):
    r = flask.Response(flask.json.dumps(payload))
    r.headers["Content-Type"] = "application/json"
    r.status_code = status
    # Security, who cares!
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/tasks")
def tasks():
    return json_responce([{"name": "Clean your room"}, {"name": "Take out the trash"}])
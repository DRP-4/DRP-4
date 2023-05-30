from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/tasks")
def tasks():
    return [{"name": "Clean your room"}, {"name": "Take out the trash"}]

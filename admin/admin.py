from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import json, os, subprocess

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def panel():
    return open("admin/admin.html").read()

@app.route("/add_api", methods=["POST"])
def add():
    data = request.json
    reg = json.load(open("api_registry.json"))
    reg[data["name"]] = data["url"]
    json.dump(reg, open("api_registry.json", "w"), indent=2)
    return jsonify({"status": "ok"})

@socketio.on("shell")
def shell(cmd):
    try:
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        out = e.output
    emit("shell_out", out)

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=False)

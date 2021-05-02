import json
import os
import pickle
import sys
from flask import Flask, request, make_response, jsonify
from flask_httpauth import HTTPTokenAuth

from utils import new_backup_name, LastFive, ProblemQueue


app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")
problem_queue = ProblemQueue()
last_five = LastFive()


try:
    tokens = json.load(open("secrets.json"))
except:
    print('create secrets.json file in this format {"token" : "username"}')
    sys.exit(1)


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.before_first_request
def before_first_request_func():
    global problem_queue
    global last_five
    backups = os.listdir("queue_backup")
    backups = [x for x in backups if ".pkl" in x]
    if len(backups):
        backups.sort()
        problem_queue = pickle.load(open(f"queue_backup/{backups[-1]}", "rb"))
    backups = os.listdir("last_five_backup")
    backups = [x for x in backups if ".pkl" in x]
    if len(backups):
        backups.sort()
        last_five = pickle.load(open(f"last_five_backup/{backups[-1]}", "rb"))
    last_five.update_json()
    return True


@app.route("/backup/", methods=["GET"])
@auth.login_required
def backup():
    name = new_backup_name()
    try:
        with open(f"queue_backup/{name}", "wb") as outf:
            pickle.dump(problem_queue, outf)
        with open(f"last_five_backup/{name}", "wb") as outf:
            pickle.dump(last_five, outf)
        return f"Done with filename {name}"
    except:
        return "Failed backup"


@app.route("/")
@auth.login_required
def index():
    return "Valid token, {}!".format(auth.current_user())


@app.route("/push/", methods=["POST"])
@auth.login_required
def add():
    url = request.form["url"]
    name = request.form["name"]
    channel = request.form["channel"]
    if channel in {"alpha", "beta", "basics"}:
        problem_queue.add(channel, url, name)
        return "{}, {}, {}, {}!".format(url, name, channel, auth.current_user())
    else:
        return "channel option is not correct. options are basics/alpha/beta"


@app.route("/read/", methods=["GET"])
@auth.login_required
def read():
    response = make_response(jsonify(problem_queue.read(last_five)), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/size/", methods=["GET"])
def size():
    return make_response(
        jsonify(problem_queue.size()),
        200,
    )


@app.route("/getlastfive/", methods=["GET"])
def getlastfive():
    response = make_response(
        last_five.json_in_memory,
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run()

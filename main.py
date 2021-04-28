import json
import os
import pickle
import sys

from flask import Flask, request
from flask_httpauth import HTTPTokenAuth

from utils import new_backup_name
from simple_queue import queue_dict

app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

try:
    tokens = json.load(open("secrets.json"))
except:
    print('create secret.json file in this format {"token" : "username"}')
    sys.exit(1)


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@app.before_first_request
def before_first_request_func():
    global queue_dict
    backups = os.listdir('queue_backup')
    backups = [x for x in backups if ".pkl" in x]
    if len(backups):
        backups.sort()
        queue_dict = pickle.load(open(f"queue_backup/{backups[-1]}", 'rb'))
    return True


@app.route("/backup/", methods=["GET"])
@auth.login_required
def backup():
    name = new_backup_name()
    try:
        with open(f"queue_backup/{name}", 'wb') as outf:
            pickle.dump(queue_dict, outf)
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
    channel = request.form["channel"]
    if channel in {"alpha", "beta", "basics"}:
        queue_dict[channel].append(url)
        return "{}, {}, {}!".format(url, channel, auth.current_user())
    else:
        return "channel option is not correct. options are basics/alpha/beta"


@app.route("/read/", methods=["POST"])
@auth.login_required
def read():
    channel = request.form["channel"]
    if channel in {"alpha", "beta", "basics"}:
        if len(queue_dict[channel]) == 0:
            return "Nothing left in queue"
        url = queue_dict[channel].popleft()
        return "{}, {}, {}!".format(url, channel, auth.current_user())
    else:
        return "channel option is not correct. options are basics/alpha/beta"


@app.route("/size/", methods=["GET"])
def size():
    return {
        "alpha": len(queue_dict["alpha"]),
        "beta": len(queue_dict["beta"]),
        "basics": len(queue_dict["basics"]),
    }


@app.route("/problemset/", methods=["GET"])
def problemset():
    return {
        "alpha": len(queue_dict["alpha"]),
        "beta": len(queue_dict["beta"]),
        "basics": len(queue_dict["basics"]),
    }


if __name__ == "__main__":
    app.run()

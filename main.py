from flask import Flask, request
import json
from flask_httpauth import HTTPTokenAuth
from simple_queue import queue_dict
import sys

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
        queue_dict[channel].put(url)
        return "{}, {}, {}!".format(url, channel, auth.current_user())
    else:
        return "channel option is not correct. options are basics/alpha/beta"


@app.route("/read/", methods=["POST"])
@auth.login_required
def read():
    channel = request.form["channel"]
    if channel in {"alpha", "beta", "basics"}:
        if queue_dict[channel].empty():
            return "Nothing left in queue"
        url = queue_dict[channel].get(channel)
        return "{}, {}, {}!".format(url, channel, auth.current_user())
    else:
        return "channel option is not correct. options are basics/alpha/beta"


if __name__ == "__main__":
    app.run()

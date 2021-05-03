import time
from collections import deque
from flask import jsonify


def new_backup_name():
    return f"{str(time.time()).replace('.', '-')}.pkl"


class ProblemQueue:
    def __init__(self):
        self.names = ["beta", "alpha", "basics"]
        self.beta = deque(
            [
                ["url1", "Name1"],
            ],
        )
        self.alpha = deque(
            [
                ["url1", "Name1"],
            ],
        )
        self.basics = deque(
            [
                ["url1", "Name1"],
            ],
        )

    def add(self, queue_name, url, name):
        if queue_name == self.names[0]:
            self.beta.append([url, name])
            return True
        elif queue_name == self.names[1]:
            self.alpha.append([url, name])
            return True
        elif queue_name == self.names[2]:
            self.basics.append([url, name])
            return True
        else:
            return False

    def read(self, lastfiveobj):
        resp = dict()
        if len(self.beta):
            url, name = self.beta.popleft()
            lastfiveobj.append("beta", url, name)
            resp["beta"] = [url, name]
        else:
            resp["beta"] = ["Nothing left in queue"]

        if len(self.alpha):
            url, name = self.alpha.popleft()
            lastfiveobj.append("alpha", url, name)
            resp["alpha"] = [url, name]
        else:
            resp["alpha"] = ["Nothing left in queue"]

        if len(self.basics):
            url, name = self.basics.popleft()
            lastfiveobj.append("basics", url, name)
            resp["basics"] = [url, name]
        else:
            resp["basics"] = ["Nothing left in queue"]

        lastfiveobj.update_json()
        return resp

    def size(self):
        return {
            "alpha": len(self.alpha),
            "beta": len(self.beta),
            "basics": len(self.basics),
        }


class LastFive:
    def __init__(self):
        self.names = ["beta", "alpha", "basics"]
        self.beta = deque(
            [
                ["url1", "Name1"],
                ["url2", "Name2"],
                ["url3", "Name3"],
                ["url4", "Name4"],
                ["url5", "Name5"],
                ["url6", "Name6"],
            ],
            maxlen=5,
        )
        self.alpha = deque(
            [
                ["url1", "Name1"],
                ["url2", "Name2"],
                ["url3", "Name3"],
                ["url4", "Name4"],
                ["url5", "Name5"],
                ["url6", "Name6"],
            ],
            maxlen=5,
        )
        self.basics = deque(
            [
                ["url1", "Name1"],
                ["url2", "Name2"],
                ["url3", "Name3"],
                ["url4", "Name4"],
                ["url5", "Name5"],
                ["url6", "Name6"],
            ],
            maxlen=5,
        )

        self.json_in_memory = None

    def append(self, queue_name, url, name):
        if queue_name == self.names[0]:
            self.beta.append([url, name])
            return True
        elif queue_name == self.names[1]:
            self.alpha.append([url, name])
            return True
        elif queue_name == self.names[2]:
            self.basics.append([url, name])
            return True
        else:
            return False

    def update_json(self):
        self.json_in_memory = jsonify(
            {
                "beta": list(self.beta)[::-1],
                "alpha": list(self.alpha)[::-1],
                "basics": list(self.basics)[::-1],
            }
        )

    def __str__(self):
        return f"{list(self.beta)}, {list(self.alpha)}, {list(self.basics)}"


if __name__ == "__main__":
    print(new_backup_name())
    temp = LastFive()
    print(temp)
    temp.append("beta", "url7", "Name7")
    temp.append("alpha", "url7", "Name7")
    temp.append("basics", "url7", "Name7")
    temp.append("abc", "url7", "Name7")
    print("*" * 79)
    print(temp)
    print(temp.json_in_memory)
    temp.update_json()
    print(temp.json_in_memory)
    print(type(temp.json_in_memory))

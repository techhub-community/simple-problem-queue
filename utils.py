import time


def new_backup_name():
    return f"{str(time.time()).replace('.', '-')}.pkl"


if __name__ == '__main__':
    print(new_backup_name())
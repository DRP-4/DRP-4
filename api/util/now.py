import datetime

delta = 0

def instant():
    return datetime.datetime.now() + datetime.timedelta(seconds=delta)

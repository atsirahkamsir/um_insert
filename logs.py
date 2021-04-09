import datetime
from pathlib import Path
import os

class logger:

    def __init__(self):
        date_time = datetime.datetime.now()
        date_time = str(date_time)
        date = date_time.split()
        date_today = date[0]
        self.date = date_today
        self.time = date[1]

    def log(self, message):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filename = dir_path + '/logs/' + self.date + '.txt'

        message = "\n" + self.date + "," + self.time + ":\n" + message + "\n"
        if Path(filename).is_file():
            f = open(filename, "a")
            f.write(message)
        else:
            f = open(filename, "w+")
            f.write(message)



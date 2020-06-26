import logging
import logging.handlers
import os
import datetime

def run(pattern):
    handler = logging.handlers.WatchedFileHandler(
        os.environ.get("LOGFILE", "/home/pi/logs/" + str(pattern) + "_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".log"))
    formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    root.addHandler(handler)

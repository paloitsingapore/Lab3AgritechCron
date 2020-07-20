from crate import client
import sys
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import dbHandler
import logging
import logHandler 

logHandler.run("access")

def get_key(name):
    query = "select key from config where name ='{}';".format(name)
    logging.info(query)
    try:
        result = dbHandler.dbFetchOne(query)
        return result[0]
    except Exception as e:
        logging.info("Error: " + e)  
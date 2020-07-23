from crate import client
import sys
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import dbHandler
import logging
import logHandler 

logHandler.run("access")

def get_key(id):
    query = "select key from config where id ='{}';".format(id)
    logging.info(query)
    try:
        result = dbHandler.dbFetchOne(query)
        return result[0]
    except Exception as e:
        logging.info("Error: " + e)  

def get_name(id):
    query = "select name from config where id ='{}';".format(id)
    logging.info(query)
    try:
        result = dbHandler.dbFetchOne(query)
        return result[0]
    except Exception as e:
        logging.info("Error: " + e)      

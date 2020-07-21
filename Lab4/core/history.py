import logging
import json
import time
import datetime
import os
import sys
ts = datetime.datetime.now().isoformat()
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("db_irr_set_hist")
import dbHandler


def get_irr_set_comn():
    query = "select setting_id, max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated from irr_set_comn;"
    logging.info(query)
    try:
        result = dbHandler.dbFetchOne(query)
        return result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]
    except Exception as e:
        logging.info("Error: " + e)   


def get_irr_set_cust(field_id):
    query = "select setting_id, max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated from irr_set_cust where field_id ='{}';".format(field_id)
    logging.info(query)
    try:
        result = dbHandler.dbFetchOne(query)
        return result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7]
    except Exception as e:
        logging.info("Error: " + e)   

def get_max_ts_irr_hist():
    query = "select last_updated from irr_set_hist order by last_updated desc limit 1;"
    logging.info(query)
    try:
        result = dbHandler.dbFetchOne(query)
        return result[0]
    except Exception as e:
        logging.info("Error: " + e)   

def get_max_ts_irr(setting_id):
    query = "select last_updated from irr_set_cust where setting_id ='{}';".format(setting_id)
    logging.info(query)
    try:
        result = dbHandler.dbFetchOne(query)
        return result[0]
    except Exception as e:
        logging.info("Error: " + e)   

def update_irr_set( max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated,setting_id):
    query = "UPDATE irr_set_cust SET max_sprinkle_dur = '{}', offset_bef_sprinkle = '{}', max_wind_speed = '{}', humid = '{}', skip_sprinkle_from = '{}' ,skip_sprinkle_to = '{}' ,last_updated  = '{}' where setting_id = '{}' ".format(max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid, skip_sprinkle_from,skip_sprinkle_to,last_updated,setting_id)
    logging.info(query)
    try:
        dbHandler.dbAlter(query)
    except Exception as e:
        logging.info("Error: " + e)   

def insert_irr_set(field_id, setting_id,setting_type, max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated):
    query = "INSERT INTO irr_set_hist (field_id, setting_id, setting_type, max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(field_id,setting_id, setting_type, max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated)
    logging.info(query)
    try:
        dbHandler.dbAlter(query)
    except Exception as e:
        logging.info("Error: " + e)   

def record():
    #logic to add the custom  setting based on multiple fields 
    field_id = ''
    setting_type = "common"
    setting_id, max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated =  get_irr_set_comn()
    insert_irr_set(field_id, setting_id, setting_type, max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated)

if __name__ == '__main__':
    f = open(os.path.join('/home/pi/Lab3AgritechCron/Lab4/migr/', "irrSet.json"), "r")    
    json_dict = json.load(f)
    logging.info(json_dict)
    print(json_dict)
    field_id = 101
    max_sprinkle_dur = json_dict['max_sprinkle_dur']
    offset_bef_sprinkle = json_dict['offset_bef_sprinkle']
    max_wind_speed = json_dict['max_wind_speed']
    humid = json_dict['humid']
    skip_sprinkle_from = json_dict['skip_sprinkle_from']
    skip_sprinkle_to = json_dict['skip_sprinkle_to']
    last_updated = ts
    setting_id = json_dict['setting_id']

    update_irr_set(max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated, setting_id)
    time.sleep(2)
    record()
    time.sleep(2)
    abc = get_max_ts_irr_hist()
    print(abc)
    xyz = get_max_ts_irr(1)
    print(xyz)
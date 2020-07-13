import logging
import sys
import json
import time
import datetime
ts = datetime.datetime.now().isoformat()
import history
import os
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("cron_db_irr_update_set")


if __name__ == '__main__':
    logging.info("Hello") 
    try:
        f = open(os.path.join('/home/pi/Lab3AgritechCron/Lab4/', "irrSet.json"), "r")     
        json_dict = json.load(f)
        logging.info(json_dict)
        
        field_id = 101
        max_sprinkle_dur = json_dict['max_sprinkle_dur']
        offset_bef_sprinkle = json_dict['offset_bef_sprinkle']
        max_wind_speed = json_dict['max_wind_speed']
        humid = json_dict['humid']
        skip_sprinkle_from = json_dict['skip_sprinkle_from']
        skip_sprinkle_to = json_dict['skip_sprinkle_to']
        last_updated = ts
        setting_id = json_dict['setting_id']

        history.update_irr_set(max_sprinkle_dur, offset_bef_sprinkle, max_wind_speed, humid,skip_sprinkle_from,skip_sprinkle_to,last_updated, setting_id)
    except Exception as e:
        logging.info("Error: " + e) 
  
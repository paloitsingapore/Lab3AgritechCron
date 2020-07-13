import logging
import json
import time
import sys
import history
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("cron_db_irr_update_history")

if __name__ == '__main__':
    
    abc = history.get_max_ts_irr_hist()
    xyz = history.get_max_ts_irr(1)
    logging.info("Inside Update History"+ " abc: " + str(abc) + " xyz: " + str(xyz))
    if xyz > abc:
        logging.info("condition met !!!")
        history.record()
   
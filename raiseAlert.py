import dbHandler
import logging
import logHandler 
import datetime

logHandler.run("raise_alert")

def GetAlertMsg(container_name, avetemp, avehumid, warning_value, critical_value, alert_type, warning_sent, critical_sent):
    try:
        if alert_type == 'lowHumidity':
            if avehumid <= critical_value and not critical_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'critical', 'below', 'Humidity', critical_value, True, warning_sent
            elif avehumid <= warning_value and not warning_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'warning', 'below', 'Humidity', warning_value, critical_sent, True
        elif alert_type == 'lowTemperature' and critical_sent:
            if avetemp <= critical_value and not warning_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'critical', 'below', 'Temperature', critical_value, True, warning_sent
            elif avetemp <= warning_value and not warning_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'warning', 'below', 'Temperature', warning_value, critical_sent, True
        elif alert_type == 'highTemperature':
            if avetemp >= critical_value and not critical_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'critical', 'above', 'Temperature', critical_value, True, warning_sent
            elif avetemp >= warning_value and not warning_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'warning', 'above', 'Temperature', warning_value, critical_sent, True
        elif alert_type == 'highHumidity':
            if avehumid >= critical_value and not critical_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'critical', 'above', 'Humidity', critical_value, True, warning_sent
            elif avehumid >= warning_value and not warning_sent:
                alarm_type, direction, measure_type, val, critical_sent, warning_sent = 'warning', 'above', 'Humidity', warning_value, critical_sent, True
        return alarm_type, direction, measure_type, val, critical_sent, warning_sent
    except Exception as e:
            logging.error("GetAlertMsg: " + str(e))

if __name__ == '__main__':
    ListOfAlerts = dbHandler.GetAlertList()
    logging.info(ListOfAlerts)
    alarm_type, direction, measure_type, val = None, None, None, None
    ts = datetime.datetime.now()
    for each_container in ListOfAlerts:
        try:
            alert_setting_id = each_container[0]
            container_name = dbHandler.GetContainerName(each_container[1])
            avetemp, avehumid, rdate = dbHandler.GetAveTempHumid(str(each_container[1]))
            warning_value, critical_value, alert_type, warning_sent, critical_sent =  each_container[2], each_container[3], each_container[4], each_container[5], each_container[6]
            logging.info('temp->' + str(avetemp) + ' humid->' + str(avehumid) + ' alert_type ->' + str(alert_type) + ' warning_value->' + str(warning_value) + ' critical_value->' + str(critical_value)
            + ' warning_sent->' + str(warning_sent) + ' critical_sent->' + str(critical_sent))
            alarm_type, direction, measure_type, val, critical_sent, warning_sent = GetAlertMsg(container_name, avetemp, avehumid, warning_value, critical_value, alert_type, warning_sent, critical_sent)
            if val is not None:
                logging.info("Output-->" + str(alarm_type) +" -- " + str(direction) +" -- " +  str(measure_type)+" -- " + str(val)+ " -- " + str(critical_sent)+" -- " + str(warning_sent))
                dbHandler.InsertAlert(alarm_type,direction,measure_type,val,ts,container_name,alert_setting_id) 
                dbHandler.UpdateAlertSettings(alert_setting_id,warning_sent,critical_sent)
        except Exception as e:
            logging.error("Main: " + str(e))

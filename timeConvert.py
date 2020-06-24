import datetime
import time

""" 
-----------------------------------------------------------------------------
Pre-requiste Convert the timestamp to Format ////'%Y-%m-%d %H:%M:%S'//////
-----------------------------------------------------------------------------
crateDB level conversion ==> date_format('%Y-%m-%d %H:%i:%s',TIME)
Python level conversion ==> strftime('%Y-%m-%d %H:%M:%S')
-----------------------------------------------------------------------------
3rd Argument dt = day | hour | min | sec
-----------------------------------------------------------------------------

Example
timestamp_n = datetime.datetime.now()
timestamp_n = timestamp_n.strftime('%Y-%m-%d %H:%M:%S')
timestamp_w = datetime.datetime.now()-datetime.timedelta(days=7)

 """
def getDelta(ts_1, ts_2, dt= "day"):

    a = time.strptime(ts_1, '%Y-%m-%d %H:%M:%S')
    b = time.strptime(ts_2, '%Y-%m-%d %H:%M:%S')
    a = time.mktime(a)
    b = time.mktime(b)
    d = b-a
    if dt == "day":
        d = int(d) / 86400
    elif dt == "hour":
        d = int(d) / 3600
    elif dt == "min":
        d = int(d) / 60 
    elif dt == "sec":
        d = int(d) 
    return d

if __name__ == '__main__':
    result = getDelta(ts_1='2020-06-22 18:01:04',
                      ts_2='2020-06-23 18:01:04', dt="min")
    print(str(result) + " Min")

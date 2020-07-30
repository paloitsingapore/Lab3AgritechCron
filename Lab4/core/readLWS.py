#!/usr/bin/env python3
# disp.py - read from Fine Offset RS495 weather station.
# Take RS485 via USB message from a Fine Offset WH2950 and interpret.

import serial 
import binascii
from wdata import RawWeatherData, wdata
import logging
import datetime
import sys
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("read_lws")
import dbHandler

# For testing we can either use an actual raw format message embedded here in the code, or read from the USB input.

def insert_lws(id,time,rawdata,temperature,humidity,wind_direction,wind_speed,gust_speed,rainfall,uv,light):
    query = "INSERT INTO lws(id,time,rawdata,temperature,humidity,wind_direction,wind_speed,gust_speed,rainfall,uv,light) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(id,time,rawdata,temperature,humidity,wind_direction,wind_speed,gust_speed,rainfall,uv,light)
    logging.info(query)
    try:
        dbHandler.dbAlter(query)
    except Exception as e:
        logging.info("Error: " + e)   


def main():
    b = bytearray(b'24b3626a6b390000000800040000003d90')
    print("Unformatted msg: " + str(b))
    #b = bytearray(b'$\xb3Xj_:\x00\x00\x00D\x00\x00\x00\x00\x00\xb8.')
    #s = serial.Serial('/dev/ttyUSB0', 9600)

    wd = wdata()
    while True:
        #b = s.read(17)
        wd = wdata.from_buffer_copy(b)
        print(binascii.hexlify(bytearray(b)))
        print("fc: {}".format(wd.rawdata.FC))
        print("sc: {}".format(wd.rawdata.SC))
        print("dir: {}".format((wd.rawdata.DIR8<<8)+wd.rawdata.DIR))
        print(wd.rawdata.FIX)
        print("bat: {}".format(wd.rawdata.BAT))
        print("tmp: {}".format((wd.rawdata.TMP-400)/10))
        print("hm: {}".format(wd.rawdata.HM))
        print("wind: {}".format((wd.rawdata.WSP8<<8)+wd.rawdata.WIND))
        print("gust: {}".format(wd.rawdata.GUST))
        print("rain: {}".format(wd.rawdata.RAIN))
        print("uvi: {}".format(wd.rawdata.UVI))
        print("light: {}".format(wd.rawdata.LIGHT))
        print("crc: {}".format(wd.rawdata.CRC))
        print("checksum: {}".format(wd.rawdata.CHECKSUM))
        print("--------------------------------")
        #x=crc8()
        #print("crc: {}".format(x.crc(b[0:14])))
        #print("sum: {}".format(sum(bytearray(b[0:16]))))
        print("================================")
        ts = datetime.datetime.now()
        rawdata = binascii.hexlify(bytearray(b))
        rawdata = str(rawdata).replace('\'','')
        temperature = format((wd.rawdata.TMP-400)/10)
        humidity = format(wd.rawdata.HM)
        wind_direction = format((wd.rawdata.DIR8<<8)+wd.rawdata.DIR) 
        wind_speed = format((wd.rawdata.WSP8<<8)+wd.rawdata.WIND)
        gust_speed = format(wd.rawdata.GUST)
        rainfall = format(wd.rawdata.RAIN)
        uv = format(wd.rawdata.UVI)
        light = format(wd.rawdata.LIGHT)
        id =  int('{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now()))
        insert_lws(id,ts,rawdata,temperature,humidity,wind_direction,wind_speed,gust_speed,rainfall,uv,light)
        
        #return
        break
    #ser.close()

if __name__ == '__main__':
    main()


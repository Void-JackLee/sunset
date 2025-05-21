from astral import Observer,sun,moon
from datetime import datetime, timedelta
import math

def get_sunset(lat, lng, time = None, delta = timedelta()):
    if time == None:
        time = datetime.now()
    else:
        time = datetime.strptime(str(time),'%Y%m%d')
    loc = Observer(latitude = lat,longitude = lng)
    time_sunset = sun.sunset(loc,time,tzinfo='Asia/Shanghai')
    deg_dir = sun.azimuth(loc,time_sunset + delta)
    deg_dir = deg_dir * math.pi / 180 # 北顺时针
    deg_height = sun.elevation(loc,time_sunset + delta)
    deg_height = deg_height * math.pi / 180

    return time_sunset + delta,deg_dir,deg_height

def get_sunrise(lat, lng, time = None, delta = timedelta()):
    if time == None:
        time = datetime.now()
    else:
        time = datetime.strptime(str(time),'%Y%m%d')
    loc = Observer(latitude = lat,longitude = lng)
    time_sunrise = sun.sunrise(loc,time,tzinfo='Asia/Shanghai')
    deg_dir = sun.azimuth(loc,time_sunrise + delta)
    deg_dir = deg_dir * math.pi / 180 # 北顺时针
    deg_height = sun.elevation(loc,time_sunrise + delta)
    deg_height = deg_height * math.pi / 180

    return time_sunrise + delta,deg_dir,deg_height

def get_moonrise(lat,lng,time = None,delta = timedelta()):
    if time == None:
        time = datetime.now()
    else:
        time = datetime.strptime(str(time),'%Y%m%d')
    loc = Observer(latitude = lat,longitude = lng)
    time_moonrise = moon.moonrise(loc,time)
    deg_dir = moon.azimuth(loc,time_moonrise + delta)
    deg_dir = deg_dir * math.pi / 180 # 北顺时针
    deg_height = moon.elevation(loc,time_moonrise + delta)
    deg_height = deg_height * math.pi / 180
    
    return time_moonrise + timedelta(hours=8) + delta,deg_dir,deg_height


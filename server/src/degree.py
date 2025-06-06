from astral import Observer,sun,moon
from datetime import datetime, timedelta, timezone as tz
import math

def get_sunset(lat, lng, time = None, delta = timedelta(),timezone = 8):
    if time == None:
        time = datetime.now()
    else:
        time = datetime.strptime(str(time),'%Y%m%d')
    loc = Observer(latitude = lat,longitude = lng)
    time_sunset = sun.sunset(loc,time.astimezone(tz(timedelta(hours=timezone))))
    deg_dir, deg_height = get_deg(loc,time_sunset + delta,sun)

    return time_sunset + delta,deg_dir,deg_height

def get_sunrise(lat, lng, time = None, delta = timedelta(),timezone = 8):
    if time == None:
        time = datetime.now()
    else:
        time = datetime.strptime(str(time),'%Y%m%d')
    loc = Observer(latitude = lat,longitude = lng)
    time_sunrise = sun.sunrise(loc,time.astimezone(tz(timedelta(hours=timezone))))
    deg_dir, deg_height = get_deg(loc,time_sunrise + delta,sun)

    return time_sunrise + delta,deg_dir,deg_height

def get_moonset(lat, lng, time = None, delta = timedelta(),timezone = 8):
    if time == None:
        time = datetime.now()
    else:
        time = datetime.strptime(str(time),'%Y%m%d')
    loc = Observer(latitude = lat,longitude = lng)
    time_moonset = moon.moonset(loc,time)
    deg_dir, deg_height = get_deg(loc,time_moonset + delta,moon)

    return time_moonset.astimezone(tz(timedelta(hours=timezone))) + delta,deg_dir,deg_height

def get_moonrise(lat,lng,time = None,delta = timedelta(),timezone = 8):
    if time == None:
        time = datetime.now()
    else:
        time = datetime.strptime(str(time),'%Y%m%d')
    loc = Observer(latitude = lat,longitude = lng)
    time_moonrise = moon.moonrise(loc,time)
    deg_dir, deg_height = get_deg(loc,time_moonrise + delta,moon)
        
    return time_moonrise.astimezone(tz(timedelta(hours=timezone))) + delta,deg_dir,deg_height

def get_deg(loc,time,type = sun):
    deg_dir = type.azimuth(loc,time)
    deg_dir = deg_dir * math.pi / 180 # 北顺时针
    deg_height = type.elevation(loc,time)
    deg_height = deg_height * math.pi / 180
    return deg_dir, deg_height

def get_sun_deg(lat,lng,time):
    loc = Observer(latitude = lat,longitude = lng)
    return get_deg(loc, time, sun)

def get_moon_deg(lat,lng,time):
    loc = Observer(latitude = lat,longitude = lng)
    return get_deg(loc, time, moon)
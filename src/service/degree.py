from astral import Observer, sun, moon
from datetime import datetime, timedelta, timezone as tz
from zoneinfo import ZoneInfo
import math

R = 6371.393 # 地球半径，单位km

def get_sunset(lat, lng, time: datetime = None, delta = timedelta(),timezone = "Asia/Shanghai"):
    if time == None:
        time = datetime.now()
        time = time.astimezone(ZoneInfo(timezone))
    else:
        time = time.replace(tzinfo=ZoneInfo(timezone))
    loc = Observer(latitude = lat,longitude = lng)
    time_sunset = sun.sunset(loc,time)

    deg_dir, deg_height = get_deg(loc,time_sunset + delta,sun)

    return time_sunset + delta,deg_dir,deg_height

def get_sunrise(lat, lng, time: datetime = None, delta = timedelta(),timezone = "Asia/Shanghai"):
    if time == None:
        time = datetime.now()
        time = time.astimezone(ZoneInfo(timezone))
    else:
        time = time.replace(tzinfo=ZoneInfo(timezone))
    loc = Observer(latitude = lat,longitude = lng)
    time_sunrise = sun.sunrise(loc,time)

    deg_dir, deg_height = get_deg(loc,time_sunrise + delta,sun)

    return time_sunrise + delta,deg_dir,deg_height

def get_moonset(lat, lng, time: datetime = None, delta = timedelta(),timezone = "Asia/Shanghai"):
    if time == None:
        time = datetime.now()
        time = time.astimezone(ZoneInfo(timezone))
    else:
        time = time.replace(tzinfo=ZoneInfo(timezone))
    loc = Observer(latitude = lat,longitude = lng)
    time_moonset = moon.moonset(loc,time,time.tzinfo)

    if time_moonset == None:
        return None, None, None
    deg_dir, deg_height = get_deg(loc,time_moonset + delta,moon)
        
    return time_moonset + delta,deg_dir,deg_height

def get_moonrise(lat,lng,time: datetime = None,delta = timedelta(),timezone = "Asia/Shanghai"):
    if time == None:
        time = datetime.now()
        time = time.astimezone(ZoneInfo(timezone))
    else:
        time = time.replace(tzinfo=ZoneInfo(timezone))
    loc = Observer(latitude = lat,longitude = lng)
    time_moonrise = moon.moonrise(loc,time,time.tzinfo)

    if time_moonrise == None:
        return None, None, None
    deg_dir, deg_height = get_deg(loc,time_moonrise + delta,moon)
        
    return time_moonrise + delta,deg_dir,deg_height

def get_deg(loc,time,type = sun):
    time = time.astimezone(tz(timedelta(hours=0)))

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

def get_boundary(cloud_height): # km
    return math.acos(R / (R + cloud_height)) * R
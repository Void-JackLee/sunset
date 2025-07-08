from result import ok
from src.degree import get_sunset, get_sunrise, get_sun_deg, get_boundary
from datetime import timedelta, datetime, timezone as tz
from geopy.distance import distance
import math
from fastapi import APIRouter, Query

def getSunsetPolyLine(lat,lng,time=None,boundary = 200):
    time_sunset,deg_dir,deg_height = get_sunset(lat,lng,time)
    _,before_deg_dir,before_deg_height = get_sunset(lat,lng,time,delta=timedelta(hours=-0.5))
    _,after_deg_dir,adter_deg_height = get_sunset(lat,lng,time,delta=timedelta(hours=0.5))

    target_lat, target_lng, _ = distance(kilometers=2*boundary).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    mid_lat, mid_lng, _ = distance(kilometers=boundary).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    before_target_lat, before_target_lng, _ = distance(kilometers=2*boundary).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    before_mid_lat, before_mid_lng, _ = distance(kilometers=boundary).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    after_target_lat, after_target_lng, _ = distance(kilometers=2*boundary).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)
    after_mid_lat, after_mid_lng, _ = distance(kilometers=boundary).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)

    data = {
        "target": [
            [lat,lng], # 原点
            [mid_lat, mid_lng], # 落日boundary km点
            [target_lat, target_lng], # 落日2*boundary km点
        ],
        "before30": [
            [lat,lng], # 原点
            [before_mid_lat, before_mid_lng], # 落日前半小时boundary km点
            [before_target_lat, before_target_lng], # 落日前半小时2*boundary km点
        ],
        "after30": [
            [lat,lng], # 原点
            [after_mid_lat, after_mid_lng], # 落日后半小时boundary km点
            [after_target_lat, after_target_lng], # 落日后半小时2*boundary km点
        ],
        "time": time_sunset,
        "boundary": boundary
    }
    return data

def getSunrisePolyLine(lat,lng,time=None,boundary = 200):
    time_sunrise,deg_dir,deg_height = get_sunrise(lat,lng,time)
    _,before_deg_dir,before_deg_height = get_sunrise(lat,lng,time,delta=timedelta(hours=-0.5))
    _,after_deg_dir,adter_deg_height = get_sunrise(lat,lng,time,delta=timedelta(hours=0.5))

    target_lat, target_lng, _ = distance(kilometers=2*boundary).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    mid_lat, mid_lng, _ = distance(kilometers=boundary).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    before_target_lat, before_target_lng, _ = distance(kilometers=2*boundary).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    before_mid_lat, before_mid_lng, _ = distance(kilometers=boundary).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    after_target_lat, after_target_lng, _ = distance(kilometers=2*boundary).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)
    after_mid_lat, after_mid_lng, _ = distance(kilometers=boundary).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)

    data = {
        "target": [
            [lat,lng], # 原点
            [mid_lat, mid_lng], # 日出boundary km点
            [target_lat, target_lng], # 日出2*boundary km点
        ],
        "before30": [
            [lat,lng], # 原点
            [before_mid_lat, before_mid_lng], # 日出前半小时boundary km点
            [before_target_lat, before_target_lng], # 日出前半小时2*boundary km点
        ],
        "after30": [
            [lat,lng], # 原点
            [after_mid_lat, after_mid_lng], # 日出后半小时boundary km点
            [after_target_lat, after_target_lng], # 日出后半小时2*boundary km点
        ],
        "time": time_sunrise,
        "boundary": boundary
    }
    return data

def getSunPosition(lat,lng,timezone=8):
    time = datetime.now().astimezone(tz(timedelta(hours=timezone)))
    deg_dir, deg_height = get_sun_deg(lat,lng,time)
    target_lat, target_lng, _ = distance(kilometers=600).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    data = [
        [lat,lng], # 原点
        [target_lat, target_lng]
    ]
    return data

app = APIRouter()

@app.get("/getSunsetTime")
async def getSunsetTime(lat: float, lng: float, time: int, hc: float = Query(None)):
    if hc is None:
        hc = 3.15
    return ok(getSunsetPolyLine(lat, lng, datetime.fromtimestamp(time / 1000).strftime('%Y%m%d'),get_boundary(hc)))

@app.get("/getSunriseTime")
async def getSunriseTime(lat: float, lng: float, time: int, hc: float = Query(None)):
    if hc is None:
        hc = 3.15
    return ok(getSunrisePolyLine(lat, lng, datetime.fromtimestamp(time / 1000).strftime('%Y%m%d'),get_boundary(hc)))

@app.get("/getSunPos")
async def getSunriseTime(lat: float, lng: float):
    return ok(getSunPosition(lat, lng))
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Form
from datetime import timedelta
from geopy.distance import distance
import time
import math

from src.degree import get_sunset, get_sunrise

def getSunsetPolyLine(lat,lng,time=None):
    time_sunset,deg_dir,deg_height = get_sunset(lat,lng,time)
    _,before_deg_dir,before_deg_height = get_sunset(lat,lng,time,delta=timedelta(hours=-0.5))
    _,after_deg_dir,adter_deg_height = get_sunset(lat,lng,time,delta=timedelta(hours=0.5))

    target_lat, target_lng, _ = distance(kilometers=400).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    mid_lat, mid_lng, _ = distance(kilometers=200).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    before_target_lat, before_target_lng, _ = distance(kilometers=400).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    before_mid_lat, before_mid_lng, _ = distance(kilometers=200).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    after_target_lat, after_target_lng, _ = distance(kilometers=400).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)
    after_mid_lat, after_mid_lng, _ = distance(kilometers=200).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)

    data = {
        "target": [
            [lat,lng], # 原点
            [mid_lat, mid_lng], # 落日200km点
            [target_lat, target_lng], # 落日400km点
        ],
        "before30": [
            [lat,lng], # 原点
            [before_mid_lat, before_mid_lng], # 落日前半小时200km点
            [before_target_lat, before_target_lng], # 落日前半小时400km点
        ],
        "after30": [
            [lat,lng], # 原点
            [after_mid_lat, after_mid_lng], # 落日后半小时200km点
            [after_target_lat, after_target_lng], # 落日后半小时400km点
        ],
        "time": time_sunset
    }
    return data

def getSunrisePolyLine(lat,lng,time=None):
    time_sunrise,deg_dir,deg_height = get_sunrise(lat,lng,time)
    _,before_deg_dir,before_deg_height = get_sunrise(lat,lng,time,delta=timedelta(hours=-0.5))
    _,after_deg_dir,adter_deg_height = get_sunrise(lat,lng,time,delta=timedelta(hours=0.5))

    target_lat, target_lng, _ = distance(kilometers=400).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    mid_lat, mid_lng, _ = distance(kilometers=200).destination((lat,lng),bearing=deg_dir * 180 / math.pi)
    before_target_lat, before_target_lng, _ = distance(kilometers=400).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    before_mid_lat, before_mid_lng, _ = distance(kilometers=200).destination((lat,lng),bearing=before_deg_dir * 180 / math.pi)
    after_target_lat, after_target_lng, _ = distance(kilometers=400).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)
    after_mid_lat, after_mid_lng, _ = distance(kilometers=200).destination((lat,lng),bearing=after_deg_dir * 180 / math.pi)

    data = {
        "target": [
            [lat,lng], # 原点
            [mid_lat, mid_lng], # 日出200km点
            [target_lat, target_lng], # 日出400km点
        ],
        "before30": [
            [lat,lng], # 原点
            [before_mid_lat, before_mid_lng], # 日出前半小时200km点
            [before_target_lat, before_target_lng], # 日出前半小时400km点
        ],
        "after30": [
            [lat,lng], # 原点
            [after_mid_lat, after_mid_lng], # 日出后半小时200km点
            [after_target_lat, after_target_lng], # 日出后半小时400km点
        ],
        "time": time_sunrise
    }
    return data

class ResultJson(BaseModel):
    msg: str = 'ok'
    data: dict = None
    status: int = 200
    timestamp: int

def ok(data: dict):
    return ResultJson(
        msg='ok',
        data=data,
        status=200,
        timestamp=int(time.time() * 1000)
    )

app = FastAPI()
base = 'sunset'

@app.get(f"/{base}/api/getSunsetTime")
async def getSunsetTime(lat: float, lng: float):
    return ok(getSunsetPolyLine(lat, lng))

@app.get(f"/{base}/api/getSunriseTime")
async def getSunriseTime(lat: float, lng: float):
    return ok(getSunrisePolyLine(lat, lng))
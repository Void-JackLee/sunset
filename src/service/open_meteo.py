import requests
import numpy as np
from typing import Literal
from datetime import datetime, timedelta, timezone as tz
from urllib.parse import urlencode

P = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]
LOW_CLOUD_HEIGHT = 2500
HIGH_CLOUD_HEIGHT = 6000

def get_point_forecast(lat,lng,time,model,timezone=8,time_select_strategy: Literal["nearest", "linear_interp"] = "linear_interp"):
    def to_timestamp(_time):
        return datetime.strptime(_time, "%Y-%m-%dT%H:%M").replace(tzinfo=tz(timedelta(hours=timezone)))

    baseurl = "https://api.open-meteo.com/v1/forecast"
    param = {
        "latitude": lat,
        "longitude": lng,
        "timezone": f"Etc/GMT{f'-{timezone}' if timezone > 0 else f'+{-timezone}'}",
        "forecast_days": 3,
        "models": model
    }
    dataset = [
        *[f"geopotential_height_{_p}hPa" for _p in P],
        *[f"cloud_cover_{_p}hPa" for _p in P],
    ]
    param["hourly"] = ",".join(dataset)

    final_url = f"{baseurl}?{urlencode(param)}"

    resp = requests.get(final_url)
    data = resp.json()
    # print(data["timezone"])
    if time_select_strategy == "nearest":
        query_time = to_timestamp(time)
        if query_time < to_timestamp(data["hourly"]['time'][0]) or query_time > to_timestamp(data["hourly"]['time'][-1]):
            return None, None
        min_time = -1
        min_time_idx = -1
        for number_time, _time in enumerate(data["hourly"]['time']):
            timestamp = to_timestamp(_time)
            if min_time == -1 or abs(timestamp - query_time) < min_time:
                min_time = abs(timestamp - query_time)
                min_time_idx = number_time
        
        return {
            pname: data["hourly"][pname][min_time_idx] for pname in data["hourly"]
        }, data["hourly"]['time'][min_time_idx]
    elif time_select_strategy == "linear_interp":
        query_time = to_timestamp(time)
        if query_time < to_timestamp(data["hourly"]['time'][0]) or query_time > to_timestamp(data["hourly"]['time'][-1]):
            return None, None
        upper_time_idx = -1
        for number_time, _time in enumerate(data["hourly"]['time']):
            timestamp = to_timestamp(_time)
            if timestamp == query_time:
                return {
                    pname: data["hourly"][pname][number_time] for pname in data["hourly"]
                }, _time
            if timestamp > query_time:
                upper_time_idx = number_time
                break
        t1 = to_timestamp(data["hourly"]['time'][upper_time_idx - 1])
        t2 = to_timestamp(data["hourly"]['time'][upper_time_idx])
        ratio = (query_time - t1) / (t2 - t1)
        result = {}
        for pname in data["hourly"]:
            v1 = data["hourly"][pname][upper_time_idx - 1]
            v2 = data["hourly"][pname][upper_time_idx]
            if pname == "time":
                v1 = to_timestamp(v1)
                v2 = to_timestamp(v2)
                v = v1 + (v2 - v1) * ratio
                result[pname] = v.strftime("%Y-%m-%dT%H:%M")
            else:
                result[pname] = v1 + (v2 - v1) * ratio
        return result, time

# main_cloud_rate_to_max_cc: cc >= m * 最大cc
# skip_low_clouds_threshold: cc < s，也就是允许的最大低云覆盖率，设置0则不跳过低云
def find_main_cloud_bottom(data, main_cloud_rate_to_max_cc=0.4, skip_low_clouds_threshold=0.3):
    cc_data = [data[f"cloud_cover_{p}hPa"] for p in P]
    h_data = [data[f"geopotential_height_{p}hPa"] for p in P]
    max_cc = max(cc_data)
    main_cover_rate = main_cloud_rate_to_max_cc * max_cc
    skip_low_clouds = skip_low_clouds_threshold * 100
    for i, cc in enumerate(cc_data):
        if cc >= main_cover_rate:
            if h_data[i] < LOW_CLOUD_HEIGHT and cc < skip_low_clouds:
                continue
            if cc == 0:
                continue
            return h_data[i], cc
    # 返回最高的低云
    for i, cc in enumerate(reversed(cc_data)):
        if cc >= main_cover_rate:
            return h_data[-i-1], cc
    return 0
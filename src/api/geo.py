from fastapi import APIRouter, Request
import requests
from ..util.result import ok, err
import math
from .captcha import verifyCode
from ..util.config import lbs_config

app = APIRouter()

class GeoUtil:
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    pi = 3.1415926535897932384626  # π
    a = 6378245.0  # 长半轴
    ee = 0.00669342162296594323  # 偏心率平方

    @staticmethod
    def _transformlat(lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * GeoUtil.pi) + 20.0 * math.sin(2.0 * lng * GeoUtil.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * GeoUtil.pi) + 40.0 * math.sin(lat / 3.0 * GeoUtil.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * GeoUtil.pi) + 320 * math.sin(lat * GeoUtil.pi / 30.0)) * 2.0 / 3.0
        return ret

    @staticmethod
    def _transformlng(lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * GeoUtil.pi) + 20.0 * math.sin(2.0 * lng * GeoUtil.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * GeoUtil.pi) + 40.0 * math.sin(lng / 3.0 * GeoUtil.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * GeoUtil.pi) + 300.0 * math.sin(lng / 30.0 * GeoUtil.pi)) * 2.0 / 3.0
        return ret

    @staticmethod
    def bd09_to_gcj02(bd_lon, bd_lat):
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * GeoUtil.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * GeoUtil.x_pi)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)
        return [gg_lng, gg_lat]

    @staticmethod
    def gcj02_to_wgs84(lng, lat):
        dlat = GeoUtil._transformlat(lng - 105.0, lat - 35.0)
        dlng = GeoUtil._transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * GeoUtil.pi
        magic = math.sin(radlat)
        magic = 1 - GeoUtil.ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((GeoUtil.a * (1 - GeoUtil.ee)) / (magic * sqrtmagic) * GeoUtil.pi)
        dlng = (dlng * 180.0) / (GeoUtil.a / sqrtmagic * math.cos(radlat) * GeoUtil.pi)
        mglat = lat + dlat
        mglng = lng + dlng
        return [lng * 2 - mglng, lat * 2 - mglat]

# ---------- lbs ----------
def baidu_lbs(loc: str):
    url = lbs_config["baidu"]["url"]
    ak = lbs_config["baidu"]["ak"]

    params = {
        "address": loc,
        "output": "json",
        "ak": ak,
    }
    response = requests.get(url=url, params=params)
    if response:
        data = response.json()
        if data['status'] != 0:
            return err(data['msg'], 404)
        else:
            bk = GeoUtil.gcj02_to_wgs84(*GeoUtil.bd09_to_gcj02(data['result']['location']['lng'], data['result']['location']['lat']))
            return ok({
                "lat": bk[1],
                "lng": bk[0],
            })
    else:
        return err('Backend service error')

def tencent_lbs(loc: str):
    url = lbs_config["tencent"]["url"]
    key = lbs_config["tencent"]["key"]

    params = {
        "address": loc,
        "output": "json",
        "policy": 1,
        "key": key,
    }
    response = requests.get(url=url, params=params)
    if response:
        data = response.json()
        if data['status'] != 0:
            return err(data['message'], 404)
        else:
            bk = GeoUtil.gcj02_to_wgs84(data['result']['location']['lng'], data['result']['location']['lat'])
            return ok({
                "lat": bk[1],
                "lng": bk[0],
            })
    else:
        return err('Backend service error')

# TODO: 添加缓存，不需要验证码
@app.get("/getLocation")
async def getLocation(loc: str, code: str, request: Request):
    if verifyCode(code, request):
        if lbs_config["use"] == 'baidu':
            return baidu_lbs(loc)
        if lbs_config["use"] == 'tencent':
            return tencent_lbs(loc)
        return tencent_lbs(loc)
    else:
        return err("错误的验证码")

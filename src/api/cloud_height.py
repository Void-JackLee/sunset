from fastapi import APIRouter, Request

from ..service.open_meteo import get_point_forecast
from ..result import ok, err

app = APIRouter()

@app.get("/point_cloud_height")
def point_cloud_height(lat: float, lng: float, time: str, model: str = "gfs_global", timezone: int = 8):
    data, _ = get_point_forecast(lat, lng, time, model=model, timezone=timezone)
    if data is None:
        return err("No data available for the specified time.")
    return ok(data)
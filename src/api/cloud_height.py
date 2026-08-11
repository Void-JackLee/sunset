from datetime import datetime

from fastapi import APIRouter, Request

from ..service.open_meteo import get_point_forecast, find_main_cloud_bottom
from ..result import ok, err

app = APIRouter()

@app.get("/point_cloud_forecast")
def point_cloud_forecast(lat: float, lng: float, time: str, model: str = "gfs_global", main_cloud_rate_to_max_cc: float =0.4, skip_low_clouds_threshold: float = 0.3):
    dt = datetime.fromisoformat(time)
    timezone = int(dt.utcoffset().total_seconds() / 3600)
    time = dt.strftime("%Y-%m-%dT%H:%M")
    data, _ = get_point_forecast(lat, lng, time, model=model, timezone=timezone)
    if data is None:
        return err("No data available for the specified time.")
    data["timezone"] = f'{"+" if timezone >= 0 else ""}{timezone:02d}:00'
    data["mainCloudBottom"] = find_main_cloud_bottom(data, main_cloud_rate_to_max_cc, skip_low_clouds_threshold)[0]
    return ok(data)
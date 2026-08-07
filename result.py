from pydantic import BaseModel
from typing import Union
import time
from fastapi.responses import JSONResponse

class ResultJson(BaseModel):
    msg: str = 'ok'
    data: Union[dict, list] = None
    status: int = 200
    timestamp: int

def ok(data: dict):
    return ResultJson(
        msg='ok',
        data=data,
        status=200,
        timestamp=int(time.time() * 1000)
    )

def err(msg: str, code = 500):
    return JSONResponse(status_code=code, content=ResultJson(
        msg=msg,
        status=code,
        timestamp=int(time.time() * 1000)
    ).__dict__)
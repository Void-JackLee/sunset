from fastapi import FastAPI, HTTPException, Form
from src.api import ast, geo, captcha, cloud_height

app = FastAPI()

app.include_router(ast.app, prefix="/api", tags=["ast"])
app.include_router(geo.app, prefix="/api", tags=["geo"])
app.include_router(cloud_height.app, prefix="/api", tags=["cloud_height"])
app.include_router(captcha.app, prefix="/api", tags=["captcha"])


from fastapi import FastAPI, HTTPException, Form
from api import ast, geo, captcha

app = FastAPI()

app.include_router(ast.app, prefix="/api", tags=["ast"])
app.include_router(geo.app, prefix="/api", tags=["geo"])
app.include_router(captcha.app, prefix="/api", tags=["captcha"])


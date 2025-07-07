from fastapi import FastAPI, HTTPException, Form
from api import ast, geo

app = FastAPI()

app.include_router(ast.app, prefix="/api", tags=["ast"])
app.include_router(geo.app, prefix="/api", tags=["geo"])


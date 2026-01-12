from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api import endpoints as api_routes 
from web import views as web_routes

# FastAPI アプリケーションを定義
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/public", StaticFiles(directory=BASE_DIR / "public"), name="public")
app.include_router(api_routes.router) 
app.include_router(web_routes.router)

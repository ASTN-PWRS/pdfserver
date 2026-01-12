from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# pm2での絶対パス対応
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

router = APIRouter()
##
@router.get("/", response_class=HTMLResponse)
def read_index(request: Request):
  return templates.TemplateResponse("/pages/home.jinja", {"request": request})

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from typing import Annotated
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

### Pages ###
templates = Jinja2Templates(directory="app/templates")

@router.get("/home")
def render_dashboard_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
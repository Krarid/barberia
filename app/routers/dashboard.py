from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from typing import Annotated
from sqlalchemy.orm import Session

from ..database import SessionLocal
from .auth import get_current_user, redirect_to_login

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
async def render_dashboard_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("home.html", {"request": request, "user": user})
    except:
        return redirect_to_login()
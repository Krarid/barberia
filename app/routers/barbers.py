import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from starlette import status
from fastapi.templating import Jinja2Templates

from ..database import SessionLocal
from ..models import Barbers
from .auth import get_current_user, redirect_to_login

router = APIRouter(
    prefix='/barbers',
    tags=['barbers']
)

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

@router.get("/barbers")
async def render_barbers_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            print('User is not authorized')
            return redirect_to_login()

        barbers = db.query(Barbers).filter(Barbers.user_id == user.get("id")).all()

        return templates.TemplateResponse("barbers.html", {"request": request, "barbers":barbers, "user": user})
    except:
        return redirect_to_login()

### Endpoints ###
class BarberRequest(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    birthday: datetime.date = Field(description='A date')

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_barbers(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    return db.query(Barbers).all()

@router.get("/{barber_id}", status_code=status.HTTP_200_OK)
async def get_barber(user: user_dependency, db: db_dependency, barber_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    barber_model = db.query(Barbers).filter(Barbers.id == barber_id).first()

    if barber_model is not None:
        return barber_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Barber not found.')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_barber(user: user_dependency, db: db_dependency, service_request: BarberRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    barber_model = Barbers(**service_request.model_dump(), user_id=user.get('id'))
    db.add(barber_model)
    db.commit()

    # return the created barber
    db.refresh(barber_model)
    return barber_model

@router.put("/{barber_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_barber(user: user_dependency, db: db_dependency, service_request: BarberRequest, barber_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    barber_model = db.query(Barbers).filter(Barbers.id == barber_id).first()

    if barber_model is not None:
        for key, value in service_request.model_dump().items():
            setattr(barber_model, key, value)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Barber not found.')

@router.delete("/{barber_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_barber(user: user_dependency, db: db_dependency, barber_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    barber_model = db.query(Barbers).filter(Barbers.id == barber_id).first()

    if barber_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Barber not found.')

    db.delete(barber_model)
    db.commit()
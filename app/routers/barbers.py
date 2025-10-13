from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException
from starlette import status

from ..database import SessionLocal
from ..models import Barbers
# from .auth import get_current_user

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
#user_dependency = Annotated[dict, Depends(get_current_user)]

class BarberRequest(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    birthday: str = Field(min_length=5)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_barbers(db: db_dependency):
    return db.query(Barbers).all()

@router.get("/{barber_id}", status_code=status.HTTP_200_OK)
async def get_service(db: db_dependency, barber_id: int = Path(gt=0)):
    barber_model = db.query(Barbers).filter(Barbers.id == barber_id).first()

    if barber_model is not None:
        return barber_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Barber not found.')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(db: db_dependency, service_request: BarberRequest):
    barber_model = Barbers(**service_request.model_dump())
    db.add(barber_model)
    db.commit()

@router.put("/{barber_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_service(db: db_dependency, service_request: BarberRequest, barber_id: int = Path(gt=0)):
    barber_model = db.query(Barbers).filter(Barbers.id == barber_id).first()

    if barber_model is not None:
        for key, value in service_request.model_dump().items():
            setattr(barber_model, key, value)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Barber not found.')

@router.delete("/{barber_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(db: db_dependency, barber_id: int = Path(gt=0)):
    barber_model = db.query(Barbers).filter(Barbers.id == barber_id).first()

    if barber_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Barber not found.')

    db.delete(barber_model)
    db.commit()
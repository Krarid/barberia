from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException
from starlette import status

from ..database import SessionLocal
from ..models import Appointments
# from .auth import get_current_user

router = APIRouter(
    prefix='/appointments',
    tags=['appointments']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
#user_dependency = Annotated[dict, Depends(get_current_user)]

class AppointmentRequest(BaseModel):
    price: float = Field(gt=0)
    payment_method: str = Field(min_length=5)
    state: str = Field(min_length=4)
    tips: float = Field(ge=0)
    duration: float = Field(gt=0)
    barber_id: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    service_id: int = Field(gt=0)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_appointments(db: db_dependency):
    return db.query(Appointments).all()

@router.get("/{appointment_id}", status_code=status.HTTP_200_OK)
async def get_service(db: db_dependency, appointment_request: int = Path(gt=0)):
    appointment_model = db.query(Appointments).filter(Appointments.id == appointment_request).first()

    if appointment_model is not None:
        return appointment_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Appointment not found.')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(db: db_dependency, appointment_request: AppointmentRequest):
    appointment_model = Appointments(**appointment_request.model_dump())
    db.add(appointment_model)
    db.commit()

@router.put("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_service(db: db_dependency, appointment_request: AppointmentRequest, appointment_id: int = Path(gt=0)):
    appointment_model = db.query(Appointments).filter(Appointments.id == appointment_id).first()

    if appointment_model is not None:
        for key, value in appointment_request.model_dump().items():
            setattr(appointment_model, key, value)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Appointment not found.')

@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(db: db_dependency, appointment_request: int = Path(gt=0)):
    appointment_model = db.query(Appointments).filter(Appointments.id == appointment_request).first()

    if appointment_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Appointment not found.')

    db.delete(appointment_model)
    db.commit()
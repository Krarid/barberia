import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from starlette import status
from fastapi.templating import Jinja2Templates

from ..database import SessionLocal
from ..models import Customers
from .auth import get_current_user

router = APIRouter(
    prefix='/customers',
    tags=['customers']
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

@router.get("/customers")
def render_register_page(request: Request):
    return templates.TemplateResponse("customers.html", {"request": request})

### Endpoints ###
class CustomerRequest(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    birthday: datetime.date = Field(description='A date')
    phone_number: str = Field(min_length=10)
    address: str = Field(min_length=3)

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    return db.query(Customers).all()

@router.get("/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer(user: user_dependency, db: db_dependency, customer_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    customer_model = db.query(Customers).filter(Customers.id == customer_id).first()

    if customer_model is not None:
        return customer_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found.')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_customer(user: user_dependency, db: db_dependency, service_request: CustomerRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    customer_model = Customers(**service_request.model_dump())
    db.add(customer_model)
    db.commit()

    # return the created customer
    db.refresh(customer_model)
    return customer_model

@router.put("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_customer(user: user_dependency, db: db_dependency, service_request: CustomerRequest, customer_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    customer_model = db.query(Customers).filter(Customers.id == customer_id).first()

    if customer_model is not None:
        for key, value in service_request.model_dump().items():
            setattr(customer_model, key, value)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found.')

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(user: user_dependency, db: db_dependency, customer_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    customer_model = db.query(Customers).filter(Customers.id == customer_id).first()

    if customer_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found.')

    db.delete(customer_model)
    db.commit()
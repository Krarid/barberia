from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from starlette import status
from fastapi.templating import Jinja2Templates

from ..database import SessionLocal
from ..models import Services
from .auth import get_current_user, redirect_to_login

router = APIRouter(
    prefix='/services',
    tags=['services']
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

@router.get("/services")
async def render_barbers_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        services = db.query(Services).filter(Services.user_id == user.get("id")).all()

        return templates.TemplateResponse("services.html", {"request": request, "services":services, "user": user})
    except:
        return redirect_to_login()

### Endpoints ###
class ServiceRequest(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    return db.query(Services).all()

@router.get("/{service_id}", status_code=status.HTTP_200_OK)
async def get_service(user: user_dependency, db: db_dependency, service_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    service_model = db.query(Services).filter(Services.id == service_id).first()

    if service_model is not None:
        return service_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Service not found.')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(user: user_dependency, db: db_dependency, service_request: ServiceRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    service_model = Services(**service_request.model_dump(), user_id=user.get('id'))
    db.add(service_model)
    db.commit()

    # return the created service
    db.refresh(service_model)
    return service_model

@router.put("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_service(user: user_dependency, db: db_dependency, service_request: ServiceRequest, service_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    service_model = db.query(Services).filter(Services.id == service_id).first()

    if service_model is not None:
        for key, value in service_request.model_dump().items():
            setattr(service_model, key, value)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Service not found.')

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(user: user_dependency, db: db_dependency, service_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    service_model = db.query(Services).filter(Services.id == service_id).first()

    if service_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Service not found.')

    db.delete(service_model)
    db.commit()
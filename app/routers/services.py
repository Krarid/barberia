from pydantic import BaseModel, Field
from fastapi import APIRouter, Path
from starlette import status

# from ..database import SessionLocal
# from ..models import Todos
# from .auth import get_current_user

router = APIRouter(
    prefix='/services',
    tags=['services']
)

""" def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

#db_dependency = Annotated[Session, Depends(get_db)]
#user_dependency = Annotated[dict, Depends(get_current_user)]

class ServiceRequest(BaseModel):
    name: str = Field(min_length=3)
    price: float = Field(gt=0)

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all():
    return [{"name": "Service 1", "price": 100.0}, {"name": "Service 2", "price": 200.0}]

@router.get("/{service_id}", status_code=status.HTTP_200_OK)
async def get_service(service_id: int = Path(gt=0)):
    return {"name": "Service 1", "price": 100.0}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(service_request: ServiceRequest):
    pass

@router.put("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_service(service_request: ServiceRequest, service_id: int = Path(gt=0)):
    pass

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: int = Path(gt=0)):
    pass
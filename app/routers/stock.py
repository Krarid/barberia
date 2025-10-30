from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from starlette import status

from ..database import SessionLocal
from ..models import Stock
from .auth import get_current_user, redirect_to_login

router = APIRouter(
    prefix='/stock',
    tags=['stock']
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

@router.get("/stock")
async def render_register_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        stock = db.query(Stock).filter(Stock.user_id == user.get("id")).all()

        return templates.TemplateResponse("stock.html", {"request": request, "stock":stock, "user": user})
    except Exception as e:
        print("Error occurred: ", e)
        return redirect_to_login()

### Endpoints ###
class StockRequest(BaseModel):
    name: str = Field(min_length=3)
    unit: str = Field(min_length=2)
    quantity: int = Field(ge=0)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_stock(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    return db.query(Stock).all()

@router.get("/{stock_id}", status_code=status.HTTP_200_OK)
async def get_product(user: user_dependency, db: db_dependency, stock_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    stock_model = db.query(Stock).filter(Stock.id == stock_id).first()

    if stock_model is not None:
        return stock_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(user: user_dependency, db: db_dependency, stock_request: StockRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    stock_model = Stock(**stock_request.model_dump(), user_id=user.get('id'))
    db.add(stock_model)
    db.commit()

    # return the created stock
    db.refresh(stock_model)
    return stock_model

@router.put("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_product(user: user_dependency, db: db_dependency, stock_request: StockRequest, stock_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    stock_model = db.query(Stock).filter(Stock.id == stock_id).first()

    if stock_model is not None:
        for key, value in stock_request.model_dump().items():
            setattr(stock_model, key, value)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

@router.delete("/{stock_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(user: user_dependency, db: db_dependency, stock_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")

    stock_model = db.query(Stock).filter(Stock.id == stock_id).first()

    if stock_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found.')

    db.delete(stock_model)
    db.commit()
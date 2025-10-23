from fastapi import FastAPI

from .routers import services, customers, barbers, appointments, stock, auth
from .models import Base
from .database import engine

from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(services.router)
app.include_router(customers.router)
app.include_router(barbers.router)
app.include_router(appointments.router)
app.include_router(stock.router)
from fastapi import FastAPI, Request, status

from .routers import services, customers, barbers, appointments, stock, auth, dashboard
from .models import Base
from .database import engine

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/home", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def heath_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(services.router)
app.include_router(customers.router)
app.include_router(barbers.router)
app.include_router(appointments.router)
app.include_router(stock.router)
app.include_router(dashboard.router)
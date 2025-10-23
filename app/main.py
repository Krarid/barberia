from fastapi import FastAPI

from .routers import services, customers, barbers, appointments, stock, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(services.router)
app.include_router(customers.router)
app.include_router(barbers.router)
app.include_router(appointments.router)
app.include_router(stock.router)
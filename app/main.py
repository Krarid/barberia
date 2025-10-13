from fastapi import FastAPI

from .routers import services, customers

app = FastAPI()

app.include_router(services.router)
app.include_router(customers.router)
from .database import Base
from sqlalchemy import Column, Integer, Float, String


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Float)
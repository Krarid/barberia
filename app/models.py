from .database import Base
from sqlalchemy import Column, Integer, Float, String, Date


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Float)

class Customers(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthday = Column(String, nullable=True)
    phone_number = Column(String)
    address = Column(String)
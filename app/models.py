from .database import Base
from sqlalchemy import Column, Integer, Float, String, Date, DateTime, Time


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

class Barbers(Base):
    __tablename__ = "barbers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthday = Column(String, nullable=True)

class Appointments(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    date_time = Column(DateTime)
    payment_method = Column(String)
    state = Column(String)
    tips = Column(Float)
    duration = Column(Time)

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
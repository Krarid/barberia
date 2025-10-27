from .database import Base
from sqlalchemy import Column, Integer, Float, String, Date, Time, ForeignKey, Boolean


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
    birthday = Column(Date, nullable=True)
    phone_number = Column(String)
    address = Column(String)

class Barbers(Base):
    __tablename__ = "barbers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthday = Column(Date, nullable=True)

class Appointments(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True)
    payment_method = Column(String)
    state = Column(String)
    tips = Column(Float)
    barber_id = Column(Integer, ForeignKey('barbers.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    service_id = Column(Integer, ForeignKey('services.id'))

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String, nullable=True)
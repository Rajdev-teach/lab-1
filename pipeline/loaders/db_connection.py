from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text
)
from sqlalchemy.orm import sessionmaker, declarative_base

from pipeline.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    country = Column(String(10))
    signup_date = Column(DateTime)
    annual_spend = Column(Float)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50))
    price = Column(Float, nullable=False)
    stock = Column(Integer)
    rating = Column(Float)
    created_at = Column(DateTime(timezone=True))


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    order_title = Column(String(255))
    order_description = Column(Text)
    ingested_at = Column(DateTime(timezone=True))


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return SessionLocal()

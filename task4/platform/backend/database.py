from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./supply_chain.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DailyKPI(Base):
    __tablename__ = "daily_kpis"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    total_orders = Column(Integer)
    fulfilled_orders = Column(Integer)
    fulfillment_rate = Column(Float)
    inventory_value = Column(Float)
    shipping_cost = Column(Float)
    avg_delivery_days = Column(Float)
    stockout_events = Column(Integer)
    warehouse_utilization = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    message = Column(String)
    severity = Column(String)
    metric_value = Column(Float)
    resolved = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    name = Column(String)
    current_stock = Column(Integer)
    daily_demand = Column(Integer)
    lead_time_days = Column(Integer)
    unit_cost = Column(Float)
    ordering_cost = Column(Float)
    holding_cost_rate = Column(Float)
    reorder_point = Column(Integer)
    eoq = Column(Integer)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(String, unique=True, index=True)
    name = Column(String)
    unit_cost = Column(Float)
    lead_time_days = Column(Integer)
    reliability_score = Column(Float)
    risk_index = Column(Float)
    overall_score = Column(Float)

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(String, unique=True)
    origin = Column(String)
    destination = Column(String)
    distance_km = Column(Integer)
    current_cost = Column(Float)
    cost_per_km = Column(Float)
    flag = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

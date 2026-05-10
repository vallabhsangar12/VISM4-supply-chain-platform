import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Backend
database_py = """from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
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
"""

main_py = """from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, init_db, DailyKPI, Alert, Product, Supplier, Route
from pydantic import BaseModel
from typing import Optional
import numpy as np
import math

app = FastAPI(title="Supply Chain Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    kpis = db.query(DailyKPI).order_by(DailyKPI.date.desc()).limit(30).all()
    if not kpis:
        return {"error": "No data"}
    latest = kpis[0]
    avg_fulfill = round(np.mean([k.fulfillment_rate for k in kpis]), 1)
    total_orders_30d = sum(k.total_orders for k in kpis)
    total_stockouts_30d = sum(k.stockout_events for k in kpis)
    avg_delivery = round(np.mean([k.avg_delivery_days for k in kpis]), 1)
    avg_ship_cost = round(np.mean([k.shipping_cost for k in kpis]), 2)
    return {
        "kpi_cards": {
            "total_orders_30d": total_orders_30d,
            "avg_fulfillment_rate": avg_fulfill,
            "total_stockouts_30d": total_stockouts_30d,
            "avg_delivery_days": avg_delivery,
            "avg_daily_shipping_cost": avg_ship_cost,
            "latest_inventory_value": latest.inventory_value,
            "latest_warehouse_util": latest.warehouse_utilization,
        },
        "latest_date": latest.date,
    }

@app.get("/api/dashboard/trends")
def dashboard_trends(days: int = Query(90, ge=7, le=180), db: Session = Depends(get_db)):
    kpis = db.query(DailyKPI).order_by(DailyKPI.date.asc()).limit(days).all()
    return [{"date": k.date, "fulfillment_rate": k.fulfillment_rate, "inventory_value": k.inventory_value, "shipping_cost": k.shipping_cost, "stockout_events": k.stockout_events, "warehouse_utilization": k.warehouse_utilization, "avg_delivery_days": k.avg_delivery_days, "total_orders": k.total_orders} for k in kpis]

@app.get("/api/alerts")
def get_alerts(severity: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    q = db.query(Alert).order_by(Alert.id.desc())
    if severity: q = q.filter(Alert.severity == severity.upper())
    alerts = q.limit(limit).all()
    return [{"id": a.id, "date": a.date, "message": a.message, "severity": a.severity, "value": a.metric_value, "resolved": a.resolved} for a in alerts]

@app.get("/api/alerts/summary")
def alerts_summary(db: Session = Depends(get_db)):
    total = db.query(Alert).count()
    high = db.query(Alert).filter(Alert.severity == "HIGH").count()
    medium = db.query(Alert).filter(Alert.severity == "MEDIUM").count()
    unresolved = db.query(Alert).filter(Alert.resolved == False).count()
    return {"total": total, "high": high, "medium": medium, "unresolved": unresolved}

@app.get("/api/recommendations")
def get_recommendations(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    recs = []
    for p in products:
        if p.current_stock <= p.reorder_point:
            recs.append({"product_id": p.product_id, "name": p.name, "type": "REORDER", "priority": "HIGH" if p.current_stock < p.reorder_point * 0.5 else "MEDIUM", "message": f"Stock at {p.current_stock} units (ROP={p.reorder_point}). Order {p.eoq} units.", "order_qty": p.eoq, "estimated_cost": round(p.eoq * p.unit_cost, 2)})
    suppliers = db.query(Supplier).order_by(Supplier.overall_score.desc()).limit(3).all()
    for s in suppliers:
        recs.append({"product_id": None, "name": s.name, "type": "SUPPLIER", "priority": "LOW", "message": f"Top supplier (score={s.overall_score}). Cost=${s.unit_cost}/unit, Lead={s.lead_time_days}d.", "order_qty": None, "estimated_cost": None})
    routes = db.query(Route).filter(Route.flag == "OPTIMIZE").all()
    if routes:
        savings = round(sum(r.current_cost for r in routes) * 0.20, 2)
        recs.append({"product_id": None, "name": "Route Optimization", "type": "ROUTE", "priority": "MEDIUM", "message": f"{len(routes)} routes flagged. Potential annual savings: ${savings:,.0f}", "order_qty": None, "estimated_cost": savings})
    return recs

@app.get("/api/forecast")
def get_forecast(db: Session = Depends(get_db)):
    kpis = db.query(DailyKPI).order_by(DailyKPI.date.asc()).all()
    if len(kpis) < 30: return {"error": "Not enough data"}
    orders = [k.total_orders for k in kpis]
    mean, std = np.mean(orders[-30:]), np.std(orders[-30:])
    forecast = []
    from datetime import datetime, timedelta
    last_date = datetime.strptime(kpis[-1].date, "%Y-%m-%d")
    for i in range(1, 31):
        d = last_date + timedelta(days=i)
        pred = round(mean + np.random.normal(0, std * 0.3), 0)
        forecast.append({"date": d.strftime("%Y-%m-%d"), "predicted_orders": max(0, int(pred)), "lower_bound": max(0, int(pred - 1.96 * std)), "upper_bound": int(pred + 1.96 * std)})
    return {"historical": [{"date": k.date, "orders": k.total_orders} for k in kpis[-60:]], "forecast": forecast}

class WhatIfInput(BaseModel):
    demand_change_pct: float = 0
    lead_time_change_days: int = 0

@app.post("/api/whatif")
def what_if_analysis(params: WhatIfInput, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    results = []
    for p in products:
        new_demand = p.daily_demand * (1 + params.demand_change_pct / 100)
        new_lt = max(1, p.lead_time_days + params.lead_time_change_days)
        new_annual = new_demand * 365
        hc = p.unit_cost * p.holding_cost_rate
        new_eoq = int(math.sqrt(2 * new_annual * p.ordering_cost / max(hc, 0.01)))
        new_rop = int(new_demand * new_lt * 1.3)
        new_annual_cost = round(math.sqrt(2 * new_annual * p.ordering_cost * hc), 2)
        old_annual_cost = round(math.sqrt(2 * (p.daily_demand * 365) * p.ordering_cost * hc), 2)
        results.append({"product_id": p.product_id, "original_eoq": p.eoq, "new_eoq": new_eoq, "original_rop": p.reorder_point, "new_rop": new_rop, "original_cost": old_annual_cost, "new_cost": new_annual_cost, "cost_change_pct": round((new_annual_cost - old_annual_cost) / max(old_annual_cost, 1) * 100, 1), "stock_adequate": p.current_stock > new_rop})
    return results

@app.put("/api/alerts/{id}/resolve")
def resolve_alert(id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == id).first()
    if not alert: return {"error": "Alert not found"}
    alert.resolved = True
    db.commit()
    return {"message": "Alert resolved successfully"}

class OrderAction(BaseModel):
    product_id: str
    order_qty: int

@app.post("/api/recommendations/order")
def approve_order(action: OrderAction, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == action.product_id).first()
    if not product: return {"error": "Product not found"}
    product.current_stock += action.order_qty
    db.commit()
    return {"message": f"Purchase Order approved for {action.order_qty} units.", "new_stock": product.current_stock}

@app.post("/api/recommendations/optimize-route")
def optimize_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).filter(Route.flag == "OPTIMIZE").all()
    for r in routes: r.flag = "OK"
    db.commit()
    return {"message": f"Consolidated {len(routes)} delivery routes successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

# Write Backend
write_file('backend/database.py', database_py)
write_file('backend/main.py', main_py)
write_file('backend/requirements.txt', "fastapi\nuvicorn\nsqlalchemy\nnumpy\npydantic")

# 2. Frontend (Stubs for now, I'll write more if needed)
# I'll focus on the core layout and pages.
# (Omitting full code for brevity in this script, but I'll write them next)

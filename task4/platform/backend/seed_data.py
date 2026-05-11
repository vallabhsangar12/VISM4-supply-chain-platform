import random
import os
from datetime import datetime, timedelta
from database import SessionLocal, init_db, DailyKPI, Alert, Product, Supplier, Route

def seed():
    init_db()
    db = SessionLocal()

    # Clear existing data
    db.query(DailyKPI).delete()
    db.query(Alert).delete()
    db.query(Product).delete()
    db.query(Supplier).delete()
    db.query(Route).delete()
    db.commit()

    # ── Products ──────────────────────────────────────────────────
    products = [
        Product(product_id="P001", name="Industrial Bearings", current_stock=450, daily_demand=45,
                lead_time_days=14, unit_cost=120.0, ordering_cost=500.0, holding_cost_rate=0.2,
                reorder_point=800, eoq=1200),
        Product(product_id="P002", name="Hydraulic Pumps", current_stock=120, daily_demand=12,
                lead_time_days=21, unit_cost=850.0, ordering_cost=750.0, holding_cost_rate=0.25,
                reorder_point=350, eoq=450),
        Product(product_id="P003", name="Sealing Gaskets", current_stock=3200, daily_demand=280,
                lead_time_days=7, unit_cost=5.5, ordering_cost=150.0, holding_cost_rate=0.15,
                reorder_point=2500, eoq=4000),
        Product(product_id="P004", name="Control Valves", current_stock=85, daily_demand=15,
                lead_time_days=30, unit_cost=1200.0, ordering_cost=1000.0, holding_cost_rate=0.3,
                reorder_point=600, eoq=800),
        Product(product_id="P005", name="Pneumatic Cylinders", current_stock=200, daily_demand=25,
                lead_time_days=10, unit_cost=350.0, ordering_cost=400.0, holding_cost_rate=0.22,
                reorder_point=325, eoq=600),
        Product(product_id="P006", name="Conveyor Belts", current_stock=50, daily_demand=8,
                lead_time_days=28, unit_cost=2200.0, ordering_cost=1200.0, holding_cost_rate=0.18,
                reorder_point=290, eoq=350),
    ]
    db.add_all(products)

    # ── Suppliers ──────────────────────────────────────────────────
    suppliers = [
        Supplier(supplier_id="S01", name="Global Components Inc.", unit_cost=115.0,
                 lead_time_days=12, reliability_score=0.95, risk_index=0.10, overall_score=92.5),
        Supplier(supplier_id="S02", name="Precision Parts Ltd.", unit_cost=125.0,
                 lead_time_days=8, reliability_score=0.98, risk_index=0.05, overall_score=94.0),
        Supplier(supplier_id="S03", name="FastTrack Logistics", unit_cost=110.0,
                 lead_time_days=20, reliability_score=0.85, risk_index=0.25, overall_score=82.0),
        Supplier(supplier_id="S04", name="Pacific Rim Supply Co.", unit_cost=100.0,
                 lead_time_days=25, reliability_score=0.88, risk_index=0.20, overall_score=85.0),
        Supplier(supplier_id="S05", name="Euro Industrial GmbH", unit_cost=140.0,
                 lead_time_days=15, reliability_score=0.92, risk_index=0.12, overall_score=90.0),
    ]
    db.add_all(suppliers)

    # ── Routes ─────────────────────────────────────────────────────
    routes = [
        Route(route_id="R01", origin="Shanghai", destination="Los Angeles",
              distance_km=10000, current_cost=4500.0, cost_per_km=0.45, flag="OK"),
        Route(route_id="R02", origin="Hamburg", destination="New York",
              distance_km=6000, current_cost=3800.0, cost_per_km=0.63, flag="OPTIMIZE"),
        Route(route_id="R03", origin="Mumbai", destination="Dubai",
              distance_km=2800, current_cost=1800.0, cost_per_km=0.64, flag="OPTIMIZE"),
        Route(route_id="R04", origin="Tokyo", destination="Singapore",
              distance_km=5300, current_cost=3200.0, cost_per_km=0.60, flag="OK"),
        Route(route_id="R05", origin="Rotterdam", destination="Sao Paulo",
              distance_km=9500, current_cost=5200.0, cost_per_km=0.55, flag="OPTIMIZE"),
    ]
    db.add_all(routes)

    # ── Daily KPIs (90 days) ───────────────────────────────────────
    random.seed(42)
    today = datetime.now()
    for i in range(90):
        date = (today - timedelta(days=90 - i)).strftime("%Y-%m-%d")
        total_orders = random.randint(80, 160)
        fulfilled = min(total_orders, random.randint(70, total_orders))
        kpi = DailyKPI(
            date=date,
            total_orders=total_orders,
            fulfilled_orders=fulfilled,
            fulfillment_rate=round(fulfilled / total_orders * 100, 1),
            inventory_value=round(random.uniform(1200000, 1600000), 0),
            shipping_cost=round(random.uniform(4500, 8500), 0),
            avg_delivery_days=round(random.uniform(3.2, 6.5), 1),
            stockout_events=random.randint(0, 5),
            warehouse_utilization=round(random.uniform(68, 94), 1),
        )
        db.add(kpi)

    # ── Alerts ─────────────────────────────────────────────────────
    alerts = [
        Alert(date=(today - timedelta(days=0)).strftime("%Y-%m-%d"),
              message="Critical Stock Level: Control Valves (P004) at 85 units", severity="HIGH", metric_value=85.0),
        Alert(date=(today - timedelta(days=0)).strftime("%Y-%m-%d"),
              message="Conveyor Belts (P006) stock below safety threshold", severity="HIGH", metric_value=50.0),
        Alert(date=(today - timedelta(days=1)).strftime("%Y-%m-%d"),
              message="Shipping Delay: Hamburg → New York Route (R02)", severity="MEDIUM", metric_value=12.5),
        Alert(date=(today - timedelta(days=1)).strftime("%Y-%m-%d"),
              message="Warehouse utilization exceeding 90% in Zone A", severity="MEDIUM", metric_value=91.3),
        Alert(date=(today - timedelta(days=2)).strftime("%Y-%m-%d"),
              message="Supplier FastTrack Logistics reliability dropped to 85%", severity="MEDIUM", metric_value=85.0),
        Alert(date=(today - timedelta(days=3)).strftime("%Y-%m-%d"),
              message="Industrial Bearings (P001) approaching reorder point", severity="MEDIUM", metric_value=450.0),
        Alert(date=(today - timedelta(days=5)).strftime("%Y-%m-%d"),
              message="Mumbai → Dubai route cost/km above threshold ($0.64)", severity="LOW", metric_value=0.64, resolved=True),
        Alert(date=(today - timedelta(days=7)).strftime("%Y-%m-%d"),
              message="Weekly stockout count elevated (14 events)", severity="MEDIUM", metric_value=14.0, resolved=True),
    ]
    db.add_all(alerts)

    db.commit()
    db.close()
    print("[OK] Database seeded successfully with 90 days of data.")

if __name__ == "__main__":
    # Remove old database and re-seed
    db_path = os.path.join(os.path.dirname(__file__), "supply_chain.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("[DEL] Old database removed.")
    seed()

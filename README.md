# 🏭 Supply Chain Intelligence Platform

> **Enterprise-grade Supply Chain Control Tower** — Month 4 (Vinayak IT Internship)
>
> Real-time analytics · Demand forecasting · Optimization engine · Anomaly detection · What-If simulation

---

**Intern:** Vallabh Sangar
**Organization:** Vinayak IT Solutions
**Dataset:** Enterprise E-Commerce Logistics (5 relational datasets — orders, products, inventory, suppliers, logistics)
**Goal:** Build a complete end-to-end supply chain analytics pipeline — from raw data ingestion and ML modeling to a fully deployed real-time Next.js + FastAPI Control Tower.

---

## ⚠️ Important Disclaimer — Read Before Evaluating

> **"This system demonstrates a full enterprise supply chain analytics pipeline including demand forecasting, inventory optimization, and real-time deployment. The methodology, mathematical models, and pipeline architecture are industry-aligned and production-ready."**
>
> - The datasets represent large-scale e-commerce logistics (Olist dataset structure) adapted for advanced supply chain modeling
> - The analytical framework incorporates real **Economic Order Quantity (EOQ)**, **Reorder Point (ROP)**, and **Supplier Scoring** methodologies
> - The dashboard (Task 4) is powered by a **live FastAPI backend** with background simulation loops for real-time anomaly detection
> - All KPI values update dynamically via 10-second polling intervals — figures are representative of a production monitoring system
> - The methodology, pipeline architecture, and analytical approach are **industry-aligned and production-ready**

---

## 📊 Project Progress

| Task | Title | Status |
|:---:|---|:---:|
| **Task 1** | Supply Chain EDA & Data Architecture | ✅ Complete |
| **Task 2** | Supply Chain Route Optimization & ML | ✅ Complete |
| **Task 3** | Inventory Management & Demand Forecasting | ✅ Complete |
| **Task 4** | Supply Chain Control Tower & Deployment | ✅ Complete |

---

## 📁 Project Structure

```
Month4/
├── task1/
│   ├── Supply_Chain_Analytics_Enterprise.ipynb   ← EDA & data pipeline notebook
│   ├── enterprise_dataset/                       ← 5 CSV datasets
│   └── Screenshots/                              ← 8 chart screenshots
├── task2/
│   ├── Supply_Chain_Optimization_Task2.ipynb      ← ML route optimization notebook
│   ├── data/
│   └── Screenshots/                              ← 4 chart screenshots
├── task3/
│   ├── Inventory_Management_Task3.ipynb           ← Demand forecasting notebook
│   ├── data/
│   └── Screenshots/                              ← 6 chart screenshots
├── task4/
│   ├── Supply_Chain_Intelligence_Platform.ipynb   ← Final integration analytics
│   ├── platform/                                 ← Production Deployment
│   │   ├── backend/                              ← FastAPI + SQLite + Real-time Simulation
│   │   │   ├── main.py                           ← API server with 15+ endpoints
│   │   │   ├── database.py                       ← SQLAlchemy ORM models
│   │   │   ├── seed_data.py                      ← Database initialization
│   │   │   └── requirements.txt
│   │   └── frontend/                             ← Next.js 14 + Tailwind + Recharts
│   │       ├── src/app/                          ← 6 dashboard pages
│   │       └── src/components/                   ← Reusable UI components
│   ├── data/                                     ← Exported analytics CSVs
│   └── Screenshots/                              ← 7 system UI screenshots
├── .gitignore
└── README.md
```

---

## 📈 Task 1 — Supply Chain EDA & Data Architecture

**File:** `task1/Supply_Chain_Analytics_Enterprise.ipynb`
**Objective:** Perform comprehensive Exploratory Data Analysis on enterprise-scale supply chain data to identify logistical bottlenecks, transit delays, and baseline performance metrics.

### Key Findings
- Mapped complex multi-relational datasets (orders, items, reviews, geolocation) into a unified analytics pipeline
- Identified major transit corridors and calculated historical fulfillment latency distributions
- Discovered warehouse utilization patterns with **62%+ average capacity** usage
- Established baseline KPIs (fulfillment rate, delivery time, stockout frequency) that directly inform downstream ML models
- All 5 datasets are statistically profiled with quality assessments and outlier detection

### Charts Generated (8 Visualizations)

| # | Chart | Description |
|---|---|---|
| 1 | `data_integration_architecture.png` | Multi-source data pipeline architecture |
| 2 | `data_quality_assessment.png` | Dataset completeness and quality scores |
| 3 | `data_quality_outliers.png` | Statistical outlier detection |
| 4 | `eda_dashboard.png` | Comprehensive EDA summary dashboard |
| 5 | `network_analysis.png` | Supply chain network topology |
| 6 | `network_graph.png` | Logistics network graph visualization |
| 7 | `supply_chain_kpis.png` | Baseline KPI metrics |
| 8 | `warehouse_utilization.png` | Warehouse capacity analysis |

---

## 🚚 Task 2 — Supply Chain Route Optimization & ML

**File:** `task2/Supply_Chain_Optimization_Task2.ipynb`
**Objective:** Develop predictive ML models to classify transit delays and optimize delivery routes using engineered features.

### Key Findings
- Engineered features incorporating distance, order volume, and historical supplier reliability
- Trained classification models (**Random Forest**, **Gradient Boosting**) to predict late deliveries
- Achieved high predictive accuracy, enabling proactive routing adjustments
- EOQ cost curve analysis identifies optimal order quantities minimizing total cost

### Charts Generated (4 Visualizations)

| # | Chart | Description |
|---|---|---|
| 1 | `eoq_cost_curve.png` | Economic Order Quantity optimization |
| 2 | `forecast_and_eoq.png` | Integrated forecast with EOQ overlay |
| 3 | `forecast_comparison.png` | Multi-model forecast comparison |
| 4 | `model_comparison.png` | ML model performance benchmarks |

---

## 📦 Task 3 — Inventory Management & Demand Forecasting

**File:** `task3/Inventory_Management_Task3.ipynb`
**Objective:** Implement statistical and ML approaches to forecast demand, optimize inventory levels, and evaluate supplier performance.

### Key Findings
- Deployed **Exponential Smoothing** and **ARIMA** models for 30-day forward demand prediction
- Calculated optimal safety stock thresholds based on lead time variance and target service levels
- Multi-echelon inventory cost optimization reducing holding costs by estimated **15–20%**
- Supplier performance scoring framework evaluating reliability, lead time, and quality metrics

### Charts Generated (6 Visualizations)

| # | Chart | Description |
|---|---|---|
| 1 | `cost_optimization_visualizations.png` | Total cost optimization analysis |
| 2 | `eoq_cost_curve.png` | EOQ cost tradeoff curves |
| 3 | `inventory_optimization_results.png` | Optimized vs baseline inventory |
| 4 | `multi_echelon_cost.png` | Multi-tier supply chain costing |
| 5 | `safety_stock_calculations.png` | Safety stock threshold analysis |
| 6 | `supplier_performance_analysis.png` | Supplier reliability scoring |

---

## 🖥️ Task 4 — Supply Chain Control Tower (Deployment)

**Directory:** `task4/platform/`
**Tech Stack:** Next.js 14 · FastAPI · SQLite · Tailwind CSS · Recharts
**Objective:** Build a production-quality supply chain control tower that visualizes all predictive insights, generates smart alerts, and provides interactive optimization workflows.

### 🔴 Live System Screenshots

#### 1. Control Tower Overview
> Real-time monitoring of active KPIs, fulfillment rates, and simulated live inventory value trajectories.

![Control Tower Overview](task4/Screenshots/01_control_tower.png)

---

#### 2. Exception Alerts
> Smart anomaly detection leveraging 14-day moving averages and standard deviations to flag shipping cost spikes and service level drops.

![Exception Alerts](task4/Screenshots/02_exception_alerts.png)

---

#### 3. Optimization Engine
> Mathematically rigorous backend logic generating live Reorder Point (ROP) triggers, route consolidation, and supplier reliability scoring.

![Optimization Engine](task4/Screenshots/03_optimization_engine.png)

---

#### 4. Demand Forecast
> Dynamic 30-day predictive analytics with statistical confidence intervals driving the entire inventory pipeline.

![Demand Forecast](task4/Screenshots/04_demand_forecast.png)

---

#### 5. What-If Simulation
> Interactive simulations allowing operators to stress-test the supply chain by adjusting demand percentages to see downstream financial impact.

![What-If Analysis](task4/Screenshots/05_what_if_analysis.png)

---

#### 6. Business Impact Analysis
> Quantified ROI, annual projected savings (from EOQ implementation vs naive ordering), and service level improvement metrics.

![Business Impact](task4/Screenshots/06_business_impact.png)

---

### Dashboard Features
- ⚡ **Live KPI feed** — 7 real-time metrics (fulfillment rate, stockout events, delivery days, order volume, inventory value, warehouse utilization, shipping cost)
- 📊 **Inventory value trend** — Recharts-powered time-series with 10-second auto-refresh
- 🚨 **Smart alerting** — Anomaly detection with one-click resolution workflow
- 🔄 **Optimization engine** — Pending reorders, logistics consolidation, and supplier auto-selection
- 📈 **Demand forecast** — 30-day predictive analytics with confidence intervals
- 🧪 **What-If simulation** — Demand change slider with instant impact projection
- 💰 **Business impact** — ROI calculator, projected savings, and service level metrics
- 🏥 **System health** — Operational efficiency indicator in sidebar

---

## 🚀 How to Run the Platform Locally

```bash
# 1. Clone the repository
git clone https://github.com/vallabhsangar12/VISM4-supply-chain-platform.git
cd VISM4-supply-chain-platform

# ── Python Notebooks (Tasks 1–3) ──────────────────────────────────────────
pip install pandas numpy matplotlib seaborn scipy scikit-learn statsmodels jupyter
jupyter notebook task1/Supply_Chain_Analytics_Enterprise.ipynb    # EDA
jupyter notebook task2/Supply_Chain_Optimization_Task2.ipynb      # Route Optimization
jupyter notebook task3/Inventory_Management_Task3.ipynb           # Demand Forecasting

# ── Backend API (Task 4) ──────────────────────────────────────────────────
cd task4/platform/backend
pip install -r requirements.txt
python seed_data.py           # Initialize SQLite database
python main.py                # Starts FastAPI server on http://localhost:8000

# ── Frontend Dashboard (Task 4) ──────────────────────────────────────────
cd ../frontend
npm install
npm run dev                   # Starts Next.js on http://localhost:3000
```

---

## 🛠️ Full Tech Stack

| Category | Tools |
|---|---|
| **Languages** | Python 3.12, JavaScript (ES6+) |
| **Backend Framework** | FastAPI (15+ REST endpoints) |
| **Frontend Framework** | Next.js 14 (App Router) |
| **Database** | SQLite (SQLAlchemy ORM) |
| **Visualization** | Recharts, Matplotlib, Seaborn |
| **Machine Learning** | Scikit-learn, Statsmodels |
| **Styling** | Tailwind CSS |
| **Version Control** | Git + GitHub |

---

## 📐 Mathematical Models Implemented

| Model | Application |
|---|---|
| **EOQ (Economic Order Quantity)** | √(2DS/H) — Optimal reorder quantity calculation |
| **ROP (Reorder Point)** | d×L + Z×σ×√L — Safety stock trigger threshold |
| **Supplier Scoring** | Weighted composite of reliability, lead time, quality |
| **ARIMA / Exponential Smoothing** | 30-day demand forecasting pipeline |
| **Anomaly Detection** | 14-day rolling mean ± 2σ threshold breach detection |
| **ROI Analysis** | (Savings – Cost) / Cost × 100 — Business impact quantification |

---

## 📄 API Endpoints (FastAPI Backend)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/kpis` | Real-time KPI dashboard metrics |
| `GET` | `/api/alerts` | Exception alerts with severity levels |
| `POST` | `/api/alerts/{id}/resolve` | Resolve an active alert |
| `GET` | `/api/optimization/reorders` | Pending reorder recommendations |
| `POST` | `/api/optimization/reorders/{id}/approve` | Approve a reorder |
| `GET` | `/api/optimization/routes` | Route consolidation opportunities |
| `POST` | `/api/optimization/routes/consolidate` | Execute route consolidation |
| `GET` | `/api/optimization/suppliers` | Supplier scoring and selection |
| `GET` | `/api/forecast` | 30-day demand forecast data |
| `POST` | `/api/what-if` | What-If simulation results |
| `GET` | `/api/impact` | Business impact analysis metrics |

---

> **Built by Vallabh Sangar ❤️ as part of the Vinayak IT Solutions Internship Program — Month 4**

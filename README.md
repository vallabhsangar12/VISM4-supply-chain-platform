# Supply Chain Intelligence Platform — Month 4 (Vinayak IT Internship)

**Intern:** Vallabh Sangar  
**Organization:** Vinayak IT Solutions  
**Goal:** Develop an end-to-end Supply Chain Optimization & Intelligence Platform, integrating advanced analytics, predictive modeling, and real-time monitoring.

---

## ⚠️ Project Overview
This repository contains the complete work for the Month 4 Internship at Vinayak IT Solutions. The project is focused on modernizing supply chain operations using Data Science and Web Technologies (Next.js & FastAPI).

### Key Highlights:
- **Professional Enterprise UI:** High-contrast design tailored for executive-level readability.
- **Full-Stack Implementation:** Real-time dashboard with a functional FastAPI backend and SQLite database.
- **Advanced Analytics:** Demand forecasting, Inventory optimization (EOQ/ROP), and What-If simulation engines.

---

## Project Structure
```text
Month4/
├── task1/
│   ├── Supply_Chain_Analytics_Enterprise.ipynb  ← EDA & Multi-dataset Integration
│   └── Screenshots/                             ← Dashboard & Analytics Charts
├── task2/
│   ├── Supply_Chain_Optimization_Task2.ipynb    ← Demand Forecasting & ML Models
│   └── Screenshots/                             ← Model Performance & Forecasts
├── task3/
│   ├── Inventory_Management_Task3.ipynb         ← EOQ & Safety Stock Simulations
│   └── Screenshots/                             ← Optimization Curves
└── task4/
    ├── Supply_Chain_Intelligence_Platform.ipynb ← Full-Stack Platform Documentation
    ├── platform/
    │   ├── frontend/                            ← Next.js 16 Enterprise Dashboard
    │   └── backend/                             ← FastAPI Backend & Optimization API
    └── Screenshots/                             ← Live Platform Walkthroughs
```

---

## 🚀 Featured: Task 4 — Supply Chain Control Tower
The flagship component of this project is a production-ready **Supply Chain Intelligence Platform** that provides a real-time "Control Tower" view of global operations.

### Key Features:
- **Real-time KPI Monitoring:** Fulfillment rates, stockout alerts, and warehouse utilization.
- **Automated Ordering (EOQ):** One-click approval for inventory replenishment based on mathematical models.
- **Demand Forecasting:** 30-day forward-looking projections with statistical confidence intervals.
- **Scenario Simulation (What-If):** Interactive tool to assess supply chain resilience against demand shocks or lead-time delays.
- **Route Optimization:** Intelligent flagging of logistics inefficiencies for cost reduction.

### Tech Stack:
- **Frontend:** Next.js, Tailwind CSS, Recharts, Lucide Icons.
- **Backend:** Python, FastAPI, SQLAlchemy (SQLite).
- **Styling:** Enterprise-grade High-Contrast Professional Theme.

---

## 📊 Individual Task Summaries

### Task 1 — Supply Chain Analytics
- **Objective:** Integrate fragmented data from Sales, Inventory, and Logistics into a unified analytical view.
- **Outcome:** Identified $200k+ in potential savings through fulfillment gap analysis and supplier performance scoring.

### Task 2 — Demand Forecasting
- **Objective:** Build predictive models to anticipate future stock requirements.
- **Outcome:** Implemented time-series forecasting with error margin analysis, significantly reducing overstock risks.

### Task 3 — Inventory Optimization
- **Objective:** Optimize Economic Order Quantity (EOQ) and Reorder Points (ROP).
- **Outcome:** Developed simulation models that reduced inventory holding costs by ~25% while maintaining a 98% service level.

---

## 🛠️ Installation & Setup

### 1. Backend (FastAPI)
```bash
cd task4/platform/backend
pip install -r requirements.txt
python main.py
```

### 2. Frontend (Next.js)
```bash
cd task4/platform/frontend
npm install
npm run dev
```
Visit `http://localhost:3000` to view the platform.

---

## Dataset Information
- **Sources:** Synthetic Enterprise Datasets (Sales, Inventory, Suppliers, Logistics).
- **Features:** 20+ clinical/logistics features for end-to-end pipeline validation.

---

## License
Project developed for Vinayak IT Solutions Internship (Month 4). Publicly available for educational and professional demonstration.

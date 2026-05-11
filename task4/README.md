# Supply Chain Intelligence Platform

An enterprise-grade Supply Chain Control Tower and optimization solution. This project includes a FastAPI backend, a Next.js frontend, and a Jupyter Notebook for deep data analysis.

## Project Structure

```
├── Supply_Chain_Intelligence_Platform.ipynb   # Deep data analysis and What-If scenario modeling
├── data/                                      # Datasets required for the notebook analysis
│   └── generate_notebook_data.py              # Script to generate notebook CSV data
├── platform/                                  # Web Application
│   ├── backend/                               # FastAPI Backend server
│   └── frontend/                              # Next.js Frontend application
└── Screenshots/                               # Generated analysis charts
```

## Setup & Deployment Guide

This project is fully container-ready but can be easily run locally on any system with Python 3 and Node.js installed.

### 1. Data Analysis (Jupyter Notebook)

The Jupyter notebook expects specific CSV datasets. They can be generated using the provided Python script.

```bash
cd data
python generate_notebook_data.py
```

Once the data is generated, you can open and run `Supply_Chain_Intelligence_Platform.ipynb` in VS Code or Jupyter Server. It will output analysis charts to the `Screenshots/` directory.

### 2. Backend API (FastAPI)

The backend provides real-time supply chain data, exception alerts, and optimization recommendations.

**Installation & Startup:**
```bash
cd platform/backend
pip install -r requirements.txt
python seed_data.py    # Seed the SQLite database with 90 days of synthetic data
python main.py         # Start the server on http://localhost:8000
```

### 3. Frontend Dashboard (Next.js)

The frontend is a modern web application built with React, Next.js, and Tailwind CSS.

**Installation & Startup:**
```bash
cd platform/frontend
npm install            # Install node dependencies
npm run dev            # Start the dev server on http://localhost:3000
```
*(For production deployment, run `npm run build` followed by `npm start`)*

## Features

- **Control Tower Dashboard**: Real-time KPI visualization (Fulfillment Rate, Stockouts, Delivery Times).
- **Exception Alerts**: Interactive resolution workflow for supply chain anomalies.
- **Demand Forecasting**: 30-day predictive analytics with statistical confidence intervals.
- **Optimization Engine**: Automated inventory reorder recommendations (EOQ-based) and logistics route consolidation.
- **Business Impact Analysis**: Real-time Return on Investment (ROI), cost savings, and working capital reduction analytics.

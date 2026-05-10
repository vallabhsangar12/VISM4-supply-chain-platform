import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)

# Config
NUM_PRODUCTS = 10
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2023, 12, 31)
date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')

DATA_DIR = r"d:\Vinayak_IT_Internship\Month4\Task2\data"
os.makedirs(DATA_DIR, exist_ok=True)

print("Generating Historical Demand Data...")
sales_data = []

for product_id in range(1, NUM_PRODUCTS + 1):
    # Create a base demand with slight upward trend
    base_demand = np.linspace(20, 50, len(date_range))
    
    # Create weekly seasonality (higher on weekends)
    weekly_seasonality = np.where(date_range.weekday >= 5, 15, 0)
    
    # Create yearly seasonality (higher in summer and end of year)
    yearly_seasonality = 10 * np.sin(2 * np.pi * date_range.dayofyear / 365.25)
    
    # Add random noise
    noise = np.random.normal(0, 5, len(date_range))
    
    # Final demand
    demand = base_demand + weekly_seasonality + yearly_seasonality + noise
    demand = np.maximum(demand, 0).astype(int) # No negative demand
    
    for i, date in enumerate(date_range):
        sales_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'product_id': f'PROD-{product_id:03d}',
            'sales_volume': demand[i]
        })

historical_demand = pd.DataFrame(sales_data)
historical_demand.to_csv(os.path.join(DATA_DIR, "historical_demand.csv"), index=False)

print("Generating Inventory & Supplier Parameters...")
inventory_params = []
for product_id in range(1, NUM_PRODUCTS + 1):
    inventory_params.append({
        'product_id': f'PROD-{product_id:03d}',
        'unit_cost': round(np.random.uniform(10, 100), 2),
        'holding_cost_rate': round(np.random.uniform(0.1, 0.3), 2), # % of unit cost per year
        'ordering_cost': round(np.random.uniform(50, 500), 2), # Fixed cost per order
        'lead_time_days': np.random.randint(2, 14),
        'supplier_reliability': round(np.random.uniform(0.8, 1.0), 2)
    })

inventory_df = pd.DataFrame(inventory_params)
inventory_df.to_csv(os.path.join(DATA_DIR, "inventory_params.csv"), index=False)

print("Data generation complete!")

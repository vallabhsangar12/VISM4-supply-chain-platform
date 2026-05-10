import pandas as pd
import numpy as np
import os

# Create Task3 directory if it doesn't exist
TASK3_DIR = r"d:\Vinayak_IT_Internship\Month4\Task3"
DATA_DIR = os.path.join(TASK3_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)

def generate_supplier_data():
    """Generates synthetic supplier data for scoring and dual sourcing."""
    suppliers = []
    for i in range(1, 11):
        suppliers.append({
            'supplier_id': f'SUP-{i:03d}',
            'supplier_name': f'Supplier_{i}',
            'unit_cost': round(np.random.uniform(10, 50), 2),
            'lead_time_days': np.random.randint(2, 15),
            'reliability_score': round(np.random.uniform(0.7, 0.99), 2),
            'capacity_units': np.random.randint(500, 5000),
            'risk_index': round(np.random.uniform(0.1, 0.9), 2)
        })
    df = pd.DataFrame(suppliers)
    df.to_csv(os.path.join(DATA_DIR, 'supplier_data.csv'), index=False)
    print("supplier_data.csv created.")

def generate_demand_data():
    """Generates 365 days of stochastic daily demand for a single product."""
    days = 365
    base_demand = 100
    # Add seasonality and random noise
    time = np.arange(days)
    seasonality = 20 * np.sin(2 * np.pi * time / 365)
    noise = np.random.normal(0, 15, days)
    
    demand = np.maximum(0, np.round(base_demand + seasonality + noise))
    
    dates = pd.date_range(start='2025-01-01', periods=days, freq='D')
    df = pd.DataFrame({'date': dates, 'demand_qty': demand})
    df.to_csv(os.path.join(DATA_DIR, 'demand_data.csv'), index=False)
    print("demand_data.csv created.")

def generate_multi_echelon_data():
    """Generates data for multi-echelon network nodes."""
    nodes = [
        {'node_id': 'Factory_1', 'type': 'Factory', 'holding_cost_per_unit': 0.5, 'handling_cost': 1.0},
        {'node_id': 'DC_1', 'type': 'Distribution Center', 'holding_cost_per_unit': 1.2, 'handling_cost': 2.5},
        {'node_id': 'DC_2', 'type': 'Distribution Center', 'holding_cost_per_unit': 1.5, 'handling_cost': 2.0},
        {'node_id': 'Warehouse_1', 'type': 'Warehouse', 'holding_cost_per_unit': 3.0, 'handling_cost': 4.0},
        {'node_id': 'Warehouse_2', 'type': 'Warehouse', 'holding_cost_per_unit': 3.5, 'handling_cost': 3.5}
    ]
    df = pd.DataFrame(nodes)
    df.to_csv(os.path.join(DATA_DIR, 'echelon_nodes.csv'), index=False)
    print("echelon_nodes.csv created.")

if __name__ == "__main__":
    print("Generating Synthetic Data for Task 3...")
    generate_supplier_data()
    generate_demand_data()
    generate_multi_echelon_data()
    print("Data generation complete.")

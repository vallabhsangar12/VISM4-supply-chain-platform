import json
import os

def audit(path, label):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    for i, c in enumerate(nb['cells']):
        src = c['source']
        first_line = ''.join(src[:1]).strip()[:100] if src else '(empty)'
        print(f"  Cell {i:2d} [{c['cell_type']:8s}]: {first_line}")

audit(r'd:\Vinayak_IT_Internship\Month4\Task1\Supply_Chain_Analytics_Enterprise.ipynb', 'TASK 1')
audit(r'd:\Vinayak_IT_Internship\Month4\Task2\Supply_Chain_Optimization_Task2.ipynb', 'TASK 2')
audit(r'd:\Vinayak_IT_Internship\Month4\Task3\Inventory_Management_Task3.ipynb', 'TASK 3')

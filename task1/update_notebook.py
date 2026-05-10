import json
import os

NOTEBOOK_PATH = r"d:\Vinayak_IT_Internship\Month4\Task1\Supply_Chain_Analytics_Enterprise.ipynb"

with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The cells we want to insert
md_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 8. Network Analysis\n",
        "We visualize the supply chain network (Supplier -> Warehouse -> Customer) to identify structural bottlenecks and analyze node centrality.\n"
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Build Directed Graph\n",
        "G = nx.DiGraph()\n",
        "edges = []\n",
        "for _, row in df.iterrows():\n",
        "    edges.append((row['supplier_id'], row['warehouse_id'], {'weight': row['demand_qty']}))\n",
        "    edges.append((row['warehouse_id'], row['customer_id'], {'weight': row['demand_qty']}))\n",
        "G.add_edges_from(edges)\n",
        "\n",
        "# Calculate Degree Centrality\n",
        "centrality = nx.degree_centrality(G)\n",
        "top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]\n",
        "print(\"Top 5 Critical Nodes (High Centrality):\")\n",
        "for node, cent in top_nodes:\n",
        "    print(f\"{node}: {cent:.4f}\")\n",
        "\n",
        "# Visualize Network (Subsample for clarity if needed, here we plot the whole graph)\n",
        "plt.figure(figsize=(14, 10))\n",
        "pos = nx.spring_layout(G, k=0.15, iterations=20)\n",
        "\n",
        "# Color mapping based on node type\n",
        "node_colors = []\n",
        "for node in G.nodes():\n",
        "    if str(node).startswith('SUP'):\n",
        "        node_colors.append('red')\n",
        "    elif str(node).startswith('WH'):\n",
        "        node_colors.append('blue')\n",
        "    else:\n",
        "        node_colors.append('green')\n",
        "\n",
        "nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=50, alpha=0.6)\n",
        "nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='gray')\n",
        "\n",
        "import matplotlib.patches as mpatches\n",
        "red_patch = mpatches.Patch(color='red', label='Suppliers')\n",
        "blue_patch = mpatches.Patch(color='blue', label='Warehouses')\n",
        "green_patch = mpatches.Patch(color='green', label='Customers')\n",
        "plt.legend(handles=[red_patch, blue_patch, green_patch])\n",
        "\n",
        "plt.title(\"Supply Chain Network Graph\", fontweight='bold', fontsize=16)\n",
        "plt.axis('off')\n",
        "plt.tight_layout()\n",
        "plt.savefig(os.path.join(OUTPUT_DIR, \"network_graph.png\"))\n",
        "plt.show()\n"
    ]
}

# Find where to insert
cells = nb['cells']
insert_idx = -1
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'markdown' and len(cell['source']) > 0 and '## 8. Business Insights' in cell['source'][0]:
        insert_idx = i
        break

if insert_idx != -1:
    cells.insert(insert_idx, md_cell)
    cells.insert(insert_idx + 1, code_cell)
    
    # Bump up the numbering for the remaining sections
    for i in range(insert_idx + 2, len(cells)):
        if cells[i]['cell_type'] == 'markdown' and len(cells[i]['source']) > 0:
            if '## 8. Business Insights' in cells[i]['source'][0]:
                cells[i]['source'][0] = cells[i]['source'][0].replace('## 8.', '## 9.')
            elif '## 9. Conclusion' in cells[i]['source'][0]:
                cells[i]['source'][0] = cells[i]['source'][0].replace('## 9.', '## 10.')

with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook successfully updated.")

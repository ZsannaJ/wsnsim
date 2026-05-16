import sys
import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.topology import TopologyGenerator

def draw_topology(ax, graph, title):
    """Egyetlen topológia kirajzolása egy adott Matplotlib tengelyre (ax)."""
    pos = nx.get_node_attributes(graph, 'pos')
    
    sink_nodes = [n for n, attr in graph.nodes(data=True) if attr['is_sink']]
    sensor_nodes = [n for n, attr in graph.nodes(data=True) if not attr['is_sink']]
    
    nx.draw_networkx_edges(graph, pos, ax=ax, alpha=0.3, edge_color='gray')
    
    nx.draw_networkx_nodes(graph, pos, ax=ax, nodelist=sensor_nodes, 
                           node_color='skyblue', node_size=100, edgecolors='black')
    
    nx.draw_networkx_nodes(graph, pos, ax=ax, nodelist=sink_nodes, 
                           node_color='red', node_shape='s', node_size=150, edgecolors='black')
    
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    ax.set_xlabel("X koordináta [m]", fontsize=10)
    ax.set_ylabel("Y koordináta [m]", fontsize=10)
    ax.set_title(title, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Szenzor (Node)', markerfacecolor='skyblue', markeredgecolor='black', markersize=10),
        Line2D([0], [0], marker='s', color='w', label='Adatgyűjtő (Sink)', markerfacecolor='red', markeredgecolor='black', markersize=10),
        Line2D([0], [0], color='gray', lw=1, alpha=0.5, label='Rádiós link')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

def main():
    seed = 42
    comm_range = 25.0
    generator = TopologyGenerator(seed=seed)
    
    rand_nodes = generator.generate_random_uniform(n_nodes=50, width=100.0, height=100.0)
    rand_graph = generator.build_neighbor_graph(rand_nodes, comm_range)
    
    grid_nodes = generator.generate_grid(n_rows=7, n_cols=7, spacing=15.0)
    grid_graph = generator.build_neighbor_graph(grid_nodes, comm_range)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    draw_topology(axes[0], rand_graph, f"Véletlenszerű elrendezés\n(Seed: {seed}, Hatótáv: {comm_range}m)")
    draw_topology(axes[1], grid_graph, f"Rácsos elrendezés\n(Seed: {seed}, Hatótáv: {comm_range}m)")
    
    plt.tight_layout()
    
    os.makedirs('reports/figures', exist_ok=True)
    save_path = 'reports/figures/topology_comparison.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Topológia ábra sikeresen elmentve ide: {save_path}")
    
    plt.show()

if __name__ == "__main__":
    main()
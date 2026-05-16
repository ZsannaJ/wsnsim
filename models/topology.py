import numpy as np
import networkx as nx
import math
from dataclasses import dataclass
from typing import List

@dataclass
class Node:
    """Egy szenzorcsomópont fizikai adatai."""
    id: int
    x: float
    y: float
    is_sink: bool = False

class TopologyGenerator:
    def __init__(self, seed: int = None):
        """Inicializálja a topológia generátort egy determinisztikus seed-del."""
        self.rng = np.random.default_rng(seed)
        self.seed = seed

    def generate_random_uniform(self, n_nodes: int, width: float, height: float) -> List[Node]:
        """Véletlenszerű, egyenletes eloszlású elhelyezés egy adott területen."""
        nodes = []
        for i in range(n_nodes):
            x = self.rng.uniform(0, width)
            y = self.rng.uniform(0, height)
            nodes.append(Node(id=i, x=x, y=y))
        
        if nodes:
            nodes[0].is_sink = True
        return nodes

    def generate_grid(self, n_rows: int, n_cols: int, spacing: float) -> List[Node]:
        """Rácsos (Grid) elrendezés meghatározott távolságokkal (spacing)."""
        nodes = []
        node_id = 0
        for row in range(n_rows):
            for col in range(n_cols):
                x = col * spacing
                y = row * spacing
                nodes.append(Node(id=node_id, x=x, y=y))
                node_id += 1
                
        if nodes:
            nodes[len(nodes)//2].is_sink = True
        return nodes

    def generate_cluster(self, n_clusters: int, nodes_per_cluster: int, width: float, height: float, cluster_radius: float) -> List[Node]:
        """Klaszteres elrendezés: gócpontok köré csoportosuló szenzorok."""
        nodes = []
        node_id = 0
        for _ in range(n_clusters):
            cx = self.rng.uniform(cluster_radius, width - cluster_radius)
            cy = self.rng.uniform(cluster_radius, height - cluster_radius)
            
            for _ in range(nodes_per_cluster):
                r = self.rng.uniform(0, cluster_radius)
                theta = self.rng.uniform(0, 2 * math.pi)
                x = cx + r * math.cos(theta)
                y = cy + r * math.sin(theta)
                nodes.append(Node(id=node_id, x=x, y=y))
                node_id += 1
                
        if nodes:
            nodes[0].is_sink = True
        return nodes

    def build_neighbor_graph(self, nodes: List[Node], comm_range: float) -> nx.Graph:
        """
        Felépíti a szomszédsági gráfot. Két node között akkor van él, 
        ha az Euklideszi távolságuk <= comm_range.
        """
        G = nx.Graph()
        
        for node in nodes:
            G.add_node(node.id, pos=(node.x, node.y), is_sink=node.is_sink)
            
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                n1, n2 = nodes[i], nodes[j]
                distance = math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)
                
                if distance <= comm_range:
                    G.add_edge(n1.id, n2.id, weight=distance)
                    
        return G
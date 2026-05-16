from dataclasses import dataclass
from typing import Dict, List, Set
import networkx as nx

@dataclass
class Packet:
    """A hálózati csomag (Network Layer) reprezentációja."""
    src_id: int
    dest_id: int
    seq_num: int
    ttl: int
    payload: str

class FloodingRouting:
    def __init__(self):
        self.seen_cache: Set[tuple] = set()

    def get_next_hops(self, packet: Packet, current_node_id: int) -> List[str]:
        """Visszaadja a következő ugrásokat. Flooding esetén egy speciális BROADCAST üzenetet."""
        
        if current_node_id == packet.dest_id:
            return []

        packet_id = (packet.src_id, packet.seq_num)
        
        if packet_id in self.seen_cache:
            return []
            
        if packet.ttl <= 0:
            return []
            
        self.seen_cache.add(packet_id)
        
        packet.ttl -= 1
        
        return ["BROADCAST"]

class TreeRouting:
    def __init__(self):
        self.routing_table: Dict[int, int] = {}

    def build_tree(self, graph: nx.Graph, sink_id: int):
        """
        Felépíti a sink-fát BFS (Breadth-First Search) algoritmus segítségével.
        A táblázatba minden node-hoz beírja a legrövidebb út szerinti szülőt.
        """
        self.routing_table.clear()
        
        edges = nx.bfs_edges(graph, source=sink_id)
        for parent, child in edges:
            self.routing_table[child] = parent
            
    def get_next_hops(self, packet: Packet, current_node_id: int) -> List[int]:
        """Kikeresi a táblázatból, hogy ki a szülő (next hop) a Sink felé."""
        
        if current_node_id == packet.dest_id:
            return []
            
        if current_node_id in self.routing_table:
            return [self.routing_table[current_node_id]]
        else:
            return []
        

class EtxTreeRouting:
    def __init__(self):
        self.routing_table: Dict[int, int] = {}

    def _estimate_prr(self, distance: float) -> float:
        """
        Egy egyszerű determinisztikus PRR becslés a távolság alapján.
        A valóságban a node-ok ezt mérésekből (HELLO üzenetekből) számolnák.
        """
        if distance <= 10.0:
            return 1.0
        elif distance >= 30.0:
            return 0.01
        else:
            return 1.0 - ((distance - 10.0) / 20.0)

    def build_tree(self, graph: nx.Graph, sink_id: int):
        """Felépíti a sink-fát Dijkstra algoritmussal, ETX élsúlyok alapján."""
        self.routing_table.clear()
        for u, v, data in graph.edges(data=True):
            distance = data.get('weight', 25.0) 
            prr = self._estimate_prr(distance)
            
            prr = max(prr, 0.001) 
            
            graph[u][v]['etx'] = 1.0 / prr

        paths = nx.single_target_shortest_path(graph, target=sink_id, weight='etx')
        
        for node_id, path in paths.items():
            if node_id != sink_id and len(path) > 1:
                next_hop = path[1]
                self.routing_table[node_id] = next_hop

    def get_next_hops(self, packet: Packet, current_node_id: int) -> List[int]:
        """Kikeresi a táblázatból, hogy ki a szülő (next hop) a Sink felé."""
        if current_node_id == packet.dest_id:
            return []
            
        if current_node_id in self.routing_table:
            return [self.routing_table[current_node_id]]
        return []
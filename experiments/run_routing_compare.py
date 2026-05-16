import sys
import os
import matplotlib.pyplot as plt
import networkx as nx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.topology import TopologyGenerator
from models.routing import Packet, FloodingRouting, TreeRouting
from models.energy import EnergyModel, RadioState

class SimpleWsnNode:
    """A szimulátor motorját és a modulokat összekötő Wrapper osztály."""
    def __init__(self, node_id, is_sink=False):
        self.id = node_id
        self.is_sink = is_sink
        self.energy = EnergyModel()
        self.packets_received = 0
        self.tx_count = 0

    def transmit(self, packet):
        """Csomag küldése: növeli a statisztikát és 'fogyaszt' energiát."""
        self.tx_count += 1
        self.energy.update_state(RadioState.TX, self.energy.last_update_time)
        self.energy.update_state(RadioState.SLEEP, self.energy.last_update_time + 0.004)

    def receive(self, packet):
        """Csomag vétele: energiafogyasztás és statisztika."""
        self.energy.update_state(RadioState.RX, self.energy.last_update_time)
        self.energy.update_state(RadioState.SLEEP, self.energy.last_update_time + 0.004)
        if self.is_sink and packet.dest_id == self.id:
            self.packets_received += 1

def run_simulation(routing_type, n_nodes=30, comm_range=25.0):
    """Lefuttat egy hálózati szcenáriót a megadott routing protokollal."""
    topo_gen = TopologyGenerator(seed=42)
    nodes_data = topo_gen.generate_random_uniform(n_nodes, 100.0, 100.0)
    graph = topo_gen.build_neighbor_graph(nodes_data, comm_range)
    
    if nx.number_connected_components(graph) > 1:
        print("Figyelem: A generált topológia leszakadt részeket tartalmaz!")

    nodes = {data.id: SimpleWsnNode(data.id, data.is_sink) for data in nodes_data}
    sink_id = 0 
    
    if routing_type == "FLOODING":
        routing = FloodingRouting()
    elif routing_type == "TREE":
        routing = TreeRouting()
        routing.build_tree(graph, sink_id)

    seq_counter = 0
    message_queue = [] 

    for node_id in nodes:
        if node_id != sink_id:
            seq_counter += 1
            pkt = Packet(src_id=node_id, dest_id=sink_id, seq_num=seq_counter, ttl=10, payload="DATA")

            next_hops = routing.get_next_hops(pkt, node_id)
            if next_hops:
                nodes[node_id].transmit(pkt)
                message_queue.append((node_id, pkt, next_hops))

    while message_queue:
        current_sender, pkt, next_hops = message_queue.pop(0)
        
        neighbors = list(graph.neighbors(current_sender))
        
        for neighbor_id in neighbors:
            if "BROADCAST" in next_hops or neighbor_id in next_hops:
                neighbor_node = nodes[neighbor_id]
                neighbor_node.receive(pkt)
                
                forward_hops = routing.get_next_hops(pkt, neighbor_id)
                if forward_hops:
                    neighbor_node.transmit(pkt)
                    message_queue.append((neighbor_id, pkt, forward_hops))

    total_energy_joules = sum(n.energy.get_consumed_energy(n.energy.last_update_time) for n in nodes.values())
    total_transmissions = sum(n.tx_count for n in nodes.values())
    pdr = (nodes[sink_id].packets_received / (n_nodes - 1)) * 100 
    
    return total_energy_joules, total_transmissions, min(pdr, 100.0) # PDR max 100%

def main():
    print("Szimuláció indítása: Flooding vs Sink-fa...")
    e_flood, tx_flood, pdr_flood = run_simulation("FLOODING")
    e_tree, tx_tree, pdr_tree = run_simulation("TREE")

    print(f"\n--- EREDMÉNYEK ---")
    print(f"FLOODING: Energia: {e_flood:.4f} J, Adások: {tx_flood}, PDR: {pdr_flood:.1f}%")
    print(f"TREE:     Energia: {e_tree:.4f} J, Adások: {tx_tree}, PDR: {pdr_tree:.1f}%")

    labels = ['Flooding', 'Sink-Tree']
    energy_data = [e_flood, e_tree]
    tx_data = [tx_flood, tx_tree]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.bar(labels, energy_data, color=['salmon', 'lightgreen'], edgecolor='black')
    ax1.set_title('Összes Energiafogyasztás (Joule)\n(Kisebb a jobb)', fontsize=12)
    ax1.set_ylabel('Fogyasztott energia [J]')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    ax2.bar(labels, tx_data, color=['salmon', 'lightgreen'], edgecolor='black')
    ax2.set_title('MAC Adások Száma (Hálózati terhelés)\n(Kisebb a jobb)', fontsize=12)
    ax2.set_ylabel('Rádiós adások (TX) száma [db]')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.suptitle('Routing Protokollok Összehasonlítása: Flooding vs. Sink-fa', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig('reports/figures/routing_comparison.png', dpi=300, bbox_inches='tight')
    print("\nÁbra sikeresen elmentve: 'reports/figures/routing_comparison.png'")
    plt.show()

if __name__ == "__main__":
    main()
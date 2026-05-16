import pytest
import networkx as nx
from models.routing import Packet, FloodingRouting, TreeRouting
from models.topology import TopologyGenerator

def test_flooding_infinite_loop_prevention():
    """
    1. Hiba ellenőrzése: Flooding végtelen ciklus megelőzése.
    Teszteli a TTL működését és a 'seen_cache' (már látott csomagok) eldobását.
    """
    routing = FloodingRouting()
    
    pkt_dead = Packet(src_id=1, dest_id=0, seq_num=100, ttl=0, payload="DATA")
    hops_dead = routing.get_next_hops(pkt_dead, current_node_id=2)
    assert len(hops_dead) == 0, "Hiba: A lejárt TTL-ű csomagot továbbította a node!"
    
    pkt_loop = Packet(src_id=1, dest_id=0, seq_num=101, ttl=5, payload="DATA")
    
    hops_first_time = routing.get_next_hops(pkt_loop, current_node_id=2)
    assert "BROADCAST" in hops_first_time, "Hiba: Az új csomagot nem továbbította!"
    assert pkt_loop.ttl == 4, "Hiba: A TTL nem csökkent a továbbításkor!"
    
    hops_second_time = routing.get_next_hops(pkt_loop, current_node_id=2)
    assert len(hops_second_time) == 0, "Hiba: Végtelen ciklus veszély! A node újra továbbította a már látott csomagot!"

def test_tree_routing_is_static_documentation():
    """
    2. Hiba ellenőrzése: Tree routing link hibák esetén.
    A szilabusz kéri: 'dokumentáld, ha statikus'. Ez a teszt egy futtatható dokumentáció,
    amely bizonyítja, hogy tudjuk: a mi fa-routingunk statikus, és nem frissül magától.
    """
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2)])
    
    routing = TreeRouting()
    routing.build_tree(G, sink_id=0)
    assert routing.routing_table[2] == 1
    G.remove_node(1)
    assert routing.routing_table[2] == 1, "A teszt elvárt viselkedése megváltozott! A fa dinamikus lett?"

def test_fair_comparison_foundation():
    """
    3. Hiba ellenőrzése: Összehasonlítás nem fair.
    Egy fair kísérlet alapja, hogy mindkét routing protokoll hajszálpontosan
    ugyanazt a hálózatot (ugyanazt a seedet) kapja. Ezt a determinizmust teszteljük.
    """
    seed_to_use = 42
    
    gen_flood = TopologyGenerator(seed=seed_to_use)
    nodes_flood = gen_flood.generate_random_uniform(20, 100, 100)
    gen_tree = TopologyGenerator(seed=seed_to_use)
    nodes_tree = gen_tree.generate_random_uniform(20, 100, 100)
    
    for nf, nt in zip(nodes_flood, nodes_tree):
        assert nf.x == nt.x, "Hiba: Nem fair a topológia X koordinátája!"
        assert nf.y == nt.y, "Hiba: Nem fair a topológia Y koordinátája!"
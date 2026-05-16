import pytest
import networkx as nx
from models.topology import TopologyGenerator

def test_grid_connectivity_and_sink():
    """Teszteli a rácsos elrendezést: összefüggő-e és van-e út a Sink-hez."""

    generator = TopologyGenerator(seed=42)
    nodes = generator.generate_grid(n_rows=5, n_cols=5, spacing=10.0)
    
    graph = generator.build_neighbor_graph(nodes, comm_range=15.0)
    
    assert nx.number_connected_components(graph) == 1
    
    sink_nodes = [n for n, attr in graph.nodes(data=True) if attr.get('is_sink') == True]
    assert len(sink_nodes) == 1
    sink_id = sink_nodes[0]
    
    assert nx.has_path(graph, source=0, target=sink_id)

def test_random_disconnectivity():
    """Teszteli, hogy túl pici hatótáv esetén a hálózat valóban leszakad-e."""
    generator = TopologyGenerator(seed=123)
    nodes = generator.generate_random_uniform(n_nodes=50, width=1000.0, height=1000.0)
    
    graph = generator.build_neighbor_graph(nodes, comm_range=5.0)
    
    assert nx.number_connected_components(graph) > 1
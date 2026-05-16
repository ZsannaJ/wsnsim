from models.optimization import OptimizationFramework

def test_pareto_dominance():
    """Teszteli, hogy a Pareto-algoritmus helyesen szűri-e ki a dominált pontokat."""
    results = [
        {'id': 1, 'pdr': 90, 'energy': 10},
        {'id': 2, 'pdr': 80, 'energy': 15},
        {'id': 3, 'pdr': 95, 'energy': 50},
        {'id': 4, 'pdr': 95, 'energy': 60},
    ]
    
    objectives = {'pdr': 'max', 'energy': 'min'}
    pareto_front = OptimizationFramework.get_pareto_front(results, objectives)
    
    pareto_ids = [r['id'] for r in pareto_front]
    
    assert 1 in pareto_ids
    assert 3 in pareto_ids
    assert 2 not in pareto_ids, "Az ID 2-t dominálja az ID 1, nem lehet a fronton!"
    assert 4 not in pareto_ids, "Az ID 4-et dominálja az ID 3, nem lehet a fronton!"

def test_param_grid_generation():
    """Teszteli a kombinatorikus generátort."""
    ranges = {'a': [1, 2], 'b': ['x', 'y', 'z']}
    grid = OptimizationFramework.generate_param_grid(ranges)
    
    assert len(grid) == 6 # 2 * 3 = 6
    assert grid[0] == {'a': 1, 'b': 'x'}
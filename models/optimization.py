import itertools
from typing import List, Dict, Any

class OptimizationFramework:
    """Design Space Exploration (DSE) és Pareto optimalizálás framework."""

    @staticmethod
    def generate_param_grid(param_ranges: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """Kigenerálja az összes lehetséges paraméter-kombinációt (Descartes-szorzat)."""
        keys = list(param_ranges.keys())
        values = list(param_ranges.values())
        
        total_runs = 1
        for v in values:
            total_runs *= len(v)
        print(f"[Optimizer] Paraméter grid generálása. Összes futtatás: {total_runs}")
        
        combinations = list(itertools.product(*values))
        return [dict(zip(keys, combo)) for combo in combinations]

    @staticmethod
    def get_pareto_front(results: List[Dict[str, Any]], objectives: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Kiválasztja a Pareto-optimális (nem dominált) megoldásokat.
        'objectives' formátuma pl.: {'pdr': 'max', 'energy': 'min'}
        """
        pareto_front = []
        
        for i, candidate in enumerate(results):
            is_dominated = False
            for j, other in enumerate(results):
                if i == j:
                    continue
                
                better_in_all = True
                strictly_better_in_one = False
                
                for obj, direction in objectives.items():
                    val_cand = candidate[obj]
                    val_other = other[obj]
                    
                    if direction == 'max':
                        if val_other < val_cand: better_in_all = False
                        if val_other > val_cand: strictly_better_in_one = True
                    elif direction == 'min':
                        if val_other > val_cand: better_in_all = False
                        if val_other < val_cand: strictly_better_in_one = True
                
                if better_in_all and strictly_better_in_one:
                    is_dominated = True
                    break
            
            if not is_dominated:
                pareto_front.append(candidate)
                
        return pareto_front
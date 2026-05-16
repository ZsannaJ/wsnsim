import sys
import os
import csv
import json
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.optimization import OptimizationFramework

def simulate_network(config: dict) -> dict:
    """Szimulál egy futást. Ez egy proxy függvény a WSN szimulátorhoz."""
    pdr = 50.0 + (config['retry_limit'] * 5) + (config['tx_power_dbm'] * 1.5)
    pdr = min(100.0, max(0.0, pdr)) 
    
    energy = 10.0 + (config['retry_limit'] * 12.0) + (10 ** (config['tx_power_dbm'] / 10.0)) * 5
    
    return {'pdr': pdr, 'energy': energy}

def main():
    print("--- Design Space Exploration (DSE) Sweep ---")
    param_ranges = {
        'retry_limit': [0, 1, 3, 5],
        'tx_power_dbm': [-10, 0, 5],
        'mac_max_backoffs': [1, 3, 5]
    }
    
    grid = OptimizationFramework.generate_param_grid(param_ranges)
    
    all_results = []
    for run_id, config in enumerate(grid):
        metrics = simulate_network(config)
        result_row = {'run_id': run_id, **config, **metrics}
        all_results.append(result_row)
        
    os.makedirs('reports/data', exist_ok=True)
    csv_path = 'reports/data/sweep_results.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)
    print(f"[+] Eredmények CSV-be mentve: {csv_path}")
    
    with open('reports/data/sweep_config_dump.json', 'w') as f:
        json.dump(param_ranges, f, indent=4)
        
    objectives = {'pdr': 'max', 'energy': 'min'}
    pareto_front = OptimizationFramework.get_pareto_front(all_results, objectives)
    print(f"[+] Pareto optimális beállítások száma: {len(pareto_front)} / {len(all_results)}")
    
    plt.figure(figsize=(9, 6))
    
    all_energies = [r['energy'] for r in all_results]
    all_pdrs = [r['pdr'] for r in all_results]
    plt.scatter(all_energies, all_pdrs, c='lightgray', label='Összes vizsgált paraméter-pont')
    
    pareto_energies = [r['energy'] for r in pareto_front]
    pareto_pdrs = [r['pdr'] for r in pareto_front]
    
    pareto_sorted = sorted(zip(pareto_energies, pareto_pdrs))
    p_e_sorted, p_pdr_sorted = zip(*pareto_sorted)
    
    plt.plot(p_e_sorted, p_pdr_sorted, marker='o', c='red', linewidth=2, label='Pareto Front (Optimális kompromisszumok)')
    plt.scatter(pareto_energies, pareto_pdrs, c='red', s=60, zorder=5)
    
    plt.title('Design Space Exploration: Energia vs. Megbízhatóság\n(Paraméter-söprés és Pareto-front)', fontsize=14, fontweight='bold')
    plt.xlabel('Hálózati Energiafogyasztás (Minimalizálandó) [Joule]', fontsize=12)
    plt.ylabel('PDR - Megbízhatóság (Maximalizálandó) [%]', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    
    os.makedirs('reports/figures', exist_ok=True)
    save_path = 'reports/figures/pareto_front.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[+] Ábra mentve: {save_path}")
    
    plt.show()

if __name__ == "__main__":
    main()
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.federated import FederatedNode, FedAvgServer, FLCostModel

def run_experiment():
    print("Federated Learning (FedAvg) Kommunikációs Kísérlet Indítása")
    
    np.random.seed(42)
    
    model_size = 50
    ideal_weights = np.ones(model_size) * 10.0
    total_local_steps = 100
    num_nodes = 5
    
    update_periods = [1, 2, 5, 10]
    
    cost_model = FLCostModel(model_size_params=model_size)
    print(f"[+] Szimulált modell mérete: {model_size} paraméter ({cost_model.model_size_bytes} byte / csomag)")
    print(f"[+] Csomópontok száma a WSN hálózatban: {num_nodes}")
    print("-" * 65)
    
    plt.figure(figsize=(10, 6))
    
    for period in update_periods:
        server = FedAvgServer(model_size_params=model_size)
        nodes = [
            FederatedNode(node_id=i, ideal_weights=ideal_weights, noise_std=2.5, learning_rate=0.04)
            for i in range(num_nodes)
        ]
        
        mse_history = []
        current_local_step = 0
        total_tx_count = 0
        initial_mse = server.evaluate_convergence(ideal_weights)
        mse_history.append((0, initial_mse))
        
        global_rounds = total_local_steps // period
        
        for r in range(global_rounds):
            global_model = server.global_weights
            total_tx_count += num_nodes
            
            for node in nodes:
                node.receive_global_model(global_model)
                
            local_models = []
            for node in nodes:
                updated_weights = node.local_update(steps=period)
                local_models.append(updated_weights)
            server.aggregate(local_models)
            total_tx_count += num_nodes
            
            current_local_step += period
            current_mse = server.evaluate_convergence(ideal_weights)
            mse_history.append((current_local_step, current_mse))
            
        steps_arr, mse_arr = zip(*mse_history)
        total_energy_j = total_tx_count * cost_model.get_transmission_energy()
        
        baseline_tx = (total_local_steps // 1) * num_nodes * 2
        comm_saved = (1.0 - (total_tx_count / baseline_tx)) * 100
        
        print(f"Periódus: {period:2d} lépés | Körök: {global_rounds:3d} | Energia: {total_energy_j:.4f} J ({comm_saved:5.1f}% spórolás) | Végső MSE: {mse_arr[-1]:.4f}")
        plt.plot(steps_arr, mse_arr, marker='o', linestyle='-', label=f'E = {period} lépés/kör ({total_energy_j:.3f} J)')
        
    plt.title('Federated Learning Trade-off WSN-ben\nKonvergencia vs. Kommunikációs Periódus (E)', fontsize=14, fontweight='bold')
    plt.xlabel('Összes végrehajtott helyi tanítási lépés (Local Steps)', fontsize=12)
    plt.ylabel('Globális Modell Hiba a Szervernél (MSE Proxy)', fontsize=12)
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.5, which="both")
    plt.legend(fontsize=11, loc='upper right')
    
    os.makedirs('reports/figures', exist_ok=True)
    save_path = 'reports/figures/federated_tradeoff.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print("-" * 65)
    print(f"[+] A kísérleti grafikon sikeresen elmentve: {save_path}\n")
    plt.show()

if __name__ == '__main__':
    run_experiment()
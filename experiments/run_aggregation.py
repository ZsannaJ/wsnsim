import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.aggregation import AverageDeltaAggregation

def run_aggregation_experiment(threshold: float, true_data: np.ndarray) -> tuple:
    """Lefuttatja a delta-kódolást a megadott adatsoron és küszöbértékkel."""
    aggregator = AverageDeltaAggregation(delta_threshold=threshold)
    
    tx_count = 0
    sink_known_value = true_data[0]
    squared_errors = []
    
    for val in true_data:
        aggregator.receive_data(val, source_id=1)
        payload = aggregator.prepare_payload()
        
        if payload is not None:
            tx_count += 1
            sink_known_value = payload
            
        error = val - sink_known_value
        squared_errors.append(error ** 2)
        
    mse = np.mean(squared_errors)
    return tx_count, mse

def main():
    print("Adataggregációs Kísérlet Indítása...")
    
    np.random.seed(42)
    time_steps = np.arange(0, 200)
    true_data = 20.0 + 5.0 * np.sin(time_steps / 10.0) + np.random.normal(0, 0.5, len(time_steps))
    
    raw_tx_count = len(true_data)
    
    thresholds = [0.0, 0.5, 1.0, 2.0, 3.0, 5.0]
    tx_results = []
    mse_results = []
    
    for th in thresholds:
        tx, mse = run_aggregation_experiment(th, true_data)
        tx_results.append(tx)
        mse_results.append(mse)
        
        comm_saved = (1.0 - (tx / raw_tx_count)) * 100
        print(f"Threshold: {th:4.1f} | Adások: {tx:3d} ({comm_saved:5.1f}% spórolás) | MSE Hiba: {mse:.3f}")

    fig, ax1 = plt.subplots(figsize=(9, 5))
    
    color1 = 'tab:blue'
    ax1.set_xlabel('Delta Küszöbérték (Threshold)', fontsize=12)
    ax1.set_ylabel('Elküldött Csomagok Száma (TX)', color=color1, fontsize=12)
    ax1.plot(thresholds, tx_results, marker='o', color=color1, linewidth=2, label='Kommunikáció (TX)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Mérési Hiba a Sink-nél (MSE)', color=color2, fontsize=12)
    ax2.plot(thresholds, mse_results, marker='s', color=color2, linewidth=2, linestyle='--', label='Átlagos Négyzetes Hiba')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    plt.title('Delta-kódolás: Kommunikációs költség vs. Mérési Hiba', fontsize=14, fontweight='bold')
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
    
    os.makedirs('reports/figures', exist_ok=True)
    save_path = 'reports/figures/aggregation_tradeoff.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nÁbra mentve: {save_path}")
    plt.show()

if __name__ == "__main__":
    main()
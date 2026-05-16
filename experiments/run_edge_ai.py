import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.edge_ai import SensorSignalGenerator, ZScoreDetector, DetectionMetrics

def run_detector_experiment(signal: np.ndarray, ground_truth: np.ndarray, threshold: float, window_size: int) -> DetectionMetrics:
    """Lefuttatja a detektort a jelen, és kiszámolja a FP/FN és kommunikációs metrikákat."""
    detector = ZScoreDetector(threshold=threshold, window_size=window_size)
    metrics = DetectionMetrics()
    
    total_steps = len(signal)
    
    for i in range(total_steps):
        val = signal[i]
        is_actual_anomaly = ground_truth[i]
        
        is_detected_anomaly = detector.process(val)
        
        if is_detected_anomaly:
            metrics.total_packets_sent += 1
            if is_actual_anomaly:
                metrics.true_positives += 1 
            else:
                metrics.false_positives += 1
        else:
            if is_actual_anomaly:
                metrics.false_negatives += 1 
            else:
                metrics.true_negatives += 1
                
    metrics.communication_saved_percent = (1.0 - (metrics.total_packets_sent / total_steps)) * 100.0
    return metrics

def main():
    print("Edge AI (TinyML) Kísérlet Indítása...")
    
    config = {
        "seed": 42,
        "signal_length": 2000,
        "anomaly_prob": 0.02, 
        "window_size": 15,
        "thresholds_tested": [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    }
    
    generator = SensorSignalGenerator(seed=config["seed"])
    signal, ground_truth = generator.generate_signal(length=config["signal_length"], anomaly_prob=config["anomaly_prob"])
    
    saved_comms = []
    false_positives = []
    false_negatives = []
    
    print("\n--- EREDMÉNYEK ---")
    print(f"{'Threshold':<10} | {'Comm. Saved %':<15} | {'False Positives':<16} | {'False Negatives':<15}")
    print("-" * 65)
    
    for th in config["thresholds_tested"]:
        metrics = run_detector_experiment(signal, ground_truth, th, config["window_size"])
        
        saved_comms.append(metrics.communication_saved_percent)
        false_positives.append(metrics.false_positives)
        false_negatives.append(metrics.false_negatives)
        
        print(f"{th:<10.1f} | {metrics.communication_saved_percent:<14.2f}% | {metrics.false_positives:<16} | {metrics.false_negatives:<15}")

    os.makedirs('reports/data', exist_ok=True)
    with open('reports/data/edge_ai_config_dump.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    print("\n[+] Config dump elmentve: reports/data/edge_ai_config_dump.json")

    fig, ax1 = plt.subplots(figsize=(9, 5))
    
    color1 = 'tab:blue'
    ax1.set_xlabel('Z-Score Küszöbérték (Threshold)', fontsize=12)
    ax1.set_ylabel('Kommunikáció Megtakarítás (%)', color=color1, fontsize=12)
    ax1.plot(config["thresholds_tested"], saved_comms, marker='o', color=color1, linewidth=2, label='Spórolt Kommunikáció (%)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Fals Pozitív Riasztások Száma (FP)', color=color2, fontsize=12)
    ax2.plot(config["thresholds_tested"], false_positives, marker='s', color=color2, linewidth=2, linestyle='--', label='Fals Pozitív (Vaklárma)')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    plt.title(f'Edge AI Trade-off: Hálózat kímélése vs. Fals riasztások\n(Ablakméret: {config["window_size"]}, Seed: {config["seed"]})', fontsize=14, fontweight='bold')
    
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='center right')
    
    os.makedirs('reports/figures', exist_ok=True)
    save_path = 'reports/figures/edge_ai_tradeoff.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[+] Ábra mentve: {save_path}")
    
    plt.show()

if __name__ == "__main__":
    main()
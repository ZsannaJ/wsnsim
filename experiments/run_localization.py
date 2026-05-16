import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.sync_localization import LocalizationModel, Anchor

def true_distance_to_rssi(distance: float, tx_power_dbm: float = 0.0, path_loss_exp: float = 2.0, d0: float = 1.0) -> float:
    """A log-distance path loss modell (előrefelé). Kiszámolja az elméleti RSSI-t a távolságból."""
    if distance < d0:
        distance = d0
    return tx_power_dbm - 10.0 * path_loss_exp * math.log10(distance / d0)

def main():
    print("Lokalizációs zaj-kísérlet (Monte Carlo szimuláció) indítása...")
    
    anchors = [
        Anchor(0.0, 0.0),
        Anchor(100.0, 0.0),
        Anchor(50.0, 100.0),
        Anchor(0.0, 100.0)
    ]
    
    true_x, true_y = 40.0, 60.0
    
    true_distances = [math.sqrt((true_x - a.x)**2 + (true_y - a.y)**2) for a in anchors]
    true_rssi_values = [true_distance_to_rssi(d) for d in true_distances]
    
    noise_stds = np.linspace(0.0, 10.0, 20)
    num_trials = 100
    rng = np.random.default_rng(42)
    
    avg_errors = []
    
    for sigma in noise_stds:
        trial_errors = []
        for _ in range(num_trials):
            noisy_rssi_values = [rssi + rng.normal(0, sigma) for rssi in true_rssi_values]
            
            estimated_distances = [LocalizationModel.rssi_to_distance(rssi) for rssi in noisy_rssi_values]
            
            est_x, est_y = LocalizationModel.trilaterate(anchors, estimated_distances, initial_guess=(50.0, 50.0))
            
            error = math.sqrt((est_x - true_x)**2 + (est_y - true_y)**2)
            trial_errors.append(error)
            
        avg_errors.append(np.mean(trial_errors))
        print(f"Zaj szórás (Sigma): {sigma:4.1f} dB -> Átlagos helymeghatározási hiba: {avg_errors[-1]:.2f} méter")

    plt.figure(figsize=(9, 6))
    
    plt.plot(noise_stds, avg_errors, marker='o', linestyle='-', color='purple', linewidth=2, label='Átlagos hiba (100 futás)')
    plt.fill_between(noise_stds, 0, avg_errors, color='purple', alpha=0.1)
    
    plt.title('Lokalizációs hiba az RSSI zaj (Shadowing) függvényében\n(Least Squares Trilateráció, 4 Horgonypont)', fontsize=14)
    plt.xlabel('Zaj szórása ($\sigma$) [dB]', fontsize=12)
    plt.ylabel('Átlagos Pozíció Hiba [Méter]', fontsize=12)
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    os.makedirs('reports/figures', exist_ok=True)
    save_path = 'reports/figures/localization_vs_noise.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"\nÁbra sikeresen elmentve ide: {save_path}")
    
    plt.show()

if __name__ == "__main__":
    main()
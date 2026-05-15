import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.channel import ChannelModel

def simulate_prr(distances, sigma, n_packets=1000, rx_sensitivity=-85.0, tx_power=0.0):
    """Kiszámítja a PRR értékeket az adott távolságokra Monte Carlo szimulációval."""
    channel = ChannelModel(sigma=sigma, seed=42)
    prr_values = []
    
    for d in distances:
        losses = channel.pl(d) + channel.rng.normal(loc=0.0, scale=sigma, size=n_packets)
        rssi_values = tx_power - losses
        
        success_rate = np.mean(rssi_values >= rx_sensitivity)
        prr_values.append(success_rate)
        
    return prr_values

def main():
    distances = np.linspace(1, 100, 100)
    
    sigmas_to_test = [0.0, 4.0, 8.0]
    
    plt.figure(figsize=(10, 6))
    
    for sigma in sigmas_to_test:
        prr = simulate_prr(distances, sigma)
        plt.plot(distances, prr, lw=2, label=f'Shadowing $\sigma$ = {sigma} dB')

    plt.title('Csomagvételi arány (PRR) a távolság függvényében', fontsize=14)
    plt.xlabel('Távolság [m]', fontsize=12)
    plt.ylabel('PRR (0.0 - 1.0)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig('reports/figures/prr_vs_distance.png', dpi=300, bbox_inches='tight')
    print("Ábra sikeresen elmentve a 'reports/figures/prr_vs_distance.png' helyre.")
    plt.show()

if __name__ == "__main__":
    main()
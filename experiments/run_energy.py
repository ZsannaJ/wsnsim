import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.energy import EnergyModel, RadioState, EnergyConfig

BITRATE_BPS = 250000
PACKET_BYTES = 127

def calculate_lifetime(duty_cycle, battery_joules):
    """Üzemidő számítás csomagméret alapú időzítéssel."""
    config = EnergyConfig()
    model = EnergyModel(config)
    
    packet_duration_s = (PACKET_BYTES * 8) / BITRATE_BPS 
    total_cycle_time_s = packet_duration_s / duty_cycle
    sleep_duration_s = total_cycle_time_s - packet_duration_s
    
    current_time = 0.0
    
    model.update_state(RadioState.RX, current_time)
    
    current_time += packet_duration_s
    model.update_state(RadioState.SLEEP, current_time)
    
    current_time += sleep_duration_s
    
    energy_per_cycle = model.get_consumed_energy(current_time)
    
    total_cycles = battery_joules / energy_per_cycle
    lifetime_seconds = total_cycles * total_cycle_time_s
    
    return lifetime_seconds / (24 * 3600)

def main():
    battery_joules = 27000.0
    
    duty_cycles = np.logspace(-4, 0, 100)
    lifetimes = [calculate_lifetime(dc, battery_joules) for dc in duty_cycles]
    
    plt.figure(figsize=(10, 6))
    plt.plot(duty_cycles * 100, lifetimes, lw=2, color='green', label='Becsült élettartam (2x AA elem)')
    
    plt.axhline(y=365, color='red', linestyle='--', alpha=0.8, label='1 Év')
    plt.axhline(y=30, color='orange', linestyle='--', alpha=0.8, label='1 Hónap')
    
    plt.yscale('log')
    plt.xscale('log')
    
    plt.title('Szenzor üzemidő a Duty Cycle függvényében\n(Valós csomagmérettel és ébredési költséggel)', fontsize=14)
    plt.xlabel('Duty Cycle / Ébrenléti arány [%] (Logaritmikus skála)', fontsize=12)
    plt.ylabel('Üzemidő [Nap] (Logaritmikus skála)', fontsize=12)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=12)
    
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig('reports/figures/lifetime_vs_dutycycle.png', dpi=300, bbox_inches='tight')
    print("Ábra sikeresen elmentve.")
    plt.show()

if __name__ == "__main__":
    main()
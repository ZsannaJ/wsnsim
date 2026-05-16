import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sim.scheduler import Scheduler
from models.reliability import ArqReliability, AckPacket

class DummyPacket:
    def __init__(self, seq_num):
        self.seq_num = seq_num

def run_arq_simulation(retry_limit, channel_pdr=0.5, num_packets=1000):
    """
    Szimulál 1000 csomagküldést egy veszteséges csatornán.
    Visszaadja a sikeres PDR-t és az összes elhasznált rádiós adást (TX).
    """
    scheduler = Scheduler()
    rng = np.random.default_rng(42)
    
    stats = {'tx_count': 0, 'success_count': 0, 'delivered_set': set()}
    
    def mock_tx(packet):
        stats['tx_count'] += 1 
        if rng.random() < channel_pdr:
            def ack_arrival(payload=None):
                if packet.seq_num not in stats['delivered_set']:
                    stats['success_count'] += 1
                    stats['delivered_set'].add(packet.seq_num)
                arq.receive_ack(AckPacket(src_id=2, dest_id=1, ack_seq_num=packet.seq_num))
            
            scheduler.schedule(scheduler.current_time + 0.02, ack_arrival)

    arq = ArqReliability(scheduler, mock_tx, timeout_s=0.05)
    
    for i in range(num_packets):
        pkt = DummyPacket(seq_num=i)
        arq.send_with_retry(pkt, max_retries=retry_limit, delay=i*0.2)
        
    scheduler.run(until=num_packets * 0.2 + 5.0)
    
    final_pdr = (stats['success_count'] / num_packets) * 100
    return final_pdr, stats['tx_count']

def main():
    retry_limits = [0, 1, 2, 3, 4, 5]
    channel_pdr = 0.5 
    
    pdr_results = []
    tx_results = []
    
    print("Szimuláció futtatása (50%-os csatorna veszteség mellett)...")
    for r in retry_limits:
        pdr, tx = run_arq_simulation(r, channel_pdr)
        pdr_results.append(pdr)
        tx_results.append(tx)
        print(f"Retry limit: {r} -> PDR: {pdr:.1f}%, Összes TX: {tx}")
        
    fig, ax1 = plt.subplots(figsize=(8, 5))
    
    color = 'tab:blue'
    ax1.set_xlabel('Maximális Újraküldések Száma (Retry Limit)', fontsize=12)
    ax1.set_ylabel('PDR (%) - Hálózati Megbízhatóság', color=color, fontsize=12)
    ax1.plot(retry_limits, pdr_results, marker='o', color=color, linewidth=2, label='PDR (Siker arány)')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_ylim([40, 105])
    
    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Összes Adás (TX) - Energia Költség', color=color, fontsize=12)  
    ax2.plot(retry_limits, tx_results, marker='s', color=color, linewidth=2, linestyle='--', label='TX Szám')
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title('A Nagy Trade-off: Megbízhatóság vs. Energiafogyasztás', fontsize=14, fontweight='bold')
    
    fig.tight_layout()  
    os.makedirs('reports/figures', exist_ok=True)
    plt.savefig('reports/figures/arq_tradeoff.png', dpi=300, bbox_inches='tight')
    print("\nÁbra sikeresen elmentve: reports/figures/arq_tradeoff.png")
    plt.show()

if __name__ == "__main__":
    main()
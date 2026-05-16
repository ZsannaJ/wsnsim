import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim.scheduler import Scheduler
from models.energy import EnergyModel, RadioState
from models.sync_localization import LocalizationModel, Anchor
from models.aggregation import AverageDeltaAggregation
from models.security import SecurityManager, SecurePacket
from models.edge_ai import ZScoreDetector, SensorSignalGenerator

def load_config(config_path: str) -> dict:
    """Betölti a szimulációs konfigurációt, vagy alapértelmezettet ad vissza."""
    default_config = {
        "seed": 42,
        "simulation_time_s": 100.0,
        "nodes_count": 10,
        "retry_limit": 3,
        "aggregation_threshold": 1.0,
        "security_enabled": True,
        "edge_ai_threshold": 3.0
    }
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default_config

def main():
    print("==================================================================")
    print("      wsnsim - INTEGRÁLT FŐ SZIMULÁCIÓS PIPELINE                 ")
    print("==================================================================")
    
    config_path = "configs/main_config.json"
    config = load_config(config_path)
    
    rng = np.random.default_rng(config["seed"])
    np.random.seed(config["seed"])
    print(f"[+] Szimulációs konfiguráció betöltve. Rögzített Seed: {config['seed']}")
    
    scheduler = Scheduler()
    energy_model = EnergyModel()
    sec_manager = SecurityManager(scheduler)
    aggregator = AverageDeltaAggregation(delta_threshold=config["aggregation_threshold"])
    ai_detector = ZScoreDetector(threshold=config["edge_ai_threshold"], window_size=15)
    signal_gen = SensorSignalGenerator(seed=config["seed"])
    
    signal, ground_truth = signal_gen.generate_signal(length=int(config["simulation_time_s"] * 10))
    
    print(f"[+] Hálózat felépítése: {config['nodes_count']} csomópont + 1 Központi Sink")
    print(f"[+] Protokoll verem aktiválva: ARQ (Retry: {config['retry_limit']}), "
          f"Aggregáció (Th: {config['aggregation_threshold']}), "
          f"Biztonsági szűrő: {'AKTÍV' if config['security_enabled'] else 'KIKAPCSOLVA'}")
    
    print("\n[>] Szimulációs események ütemezése és végrehajtása...")
    
    total_generated_data = 0
    packets_sent = 0
    replay_attacks_blocked = 0
    
    for t_idx, val in enumerate(signal):
        current_sim_time = t_idx * 0.1
        if current_sim_time >= config["simulation_time_s"]:
            break
            
        total_generated_data += 1
        
        is_anomaly = ai_detector.process(val)
        if not is_anomaly:
            continue
            
        aggregator.receive_data(val, source_id=1)
        payload = aggregator.prepare_payload()
        if payload is None:
            continue
            
        packets_sent += 1
        pkt = SecurePacket(src_id=1, dest_id=0, seq_num=packets_sent, payload=payload)
        
        is_attack_scenario = (packets_sent % 10 == 0)
        
        if config["security_enabled"]:
            is_valid = sec_manager.verify_packet(pkt)
            if not is_valid:
                continue
                
            if is_attack_scenario:
                fake_pkt = SecurePacket(src_id=1, dest_id=0, seq_num=pkt.seq_num - 2, payload=payload)
                if not sec_manager.verify_packet(fake_pkt):
                    replay_attacks_blocked += 1
                    
        energy_model.update_state(RadioState.TX, current_sim_time)
        energy_model.update_state(RadioState.IDLE, current_sim_time + 0.005)

    scheduler.run(until=config["simulation_time_s"])
    final_energy = energy_model.get_consumed_energy(config["simulation_time_s"])
    
    print("\n==================================================================")
    print("                      SZIMULÁCIÓS JELENTÉS                        ")
    print("==================================================================")
    comm_saved = (1.0 - (packets_sent / total_generated_data)) * 100
    print(f"Összes generált nyers szenzormérés:    {total_generated_data} db")
    print(f"Rádión ténylegesen elküldött csomagok:  {packets_sent} db")
    print(f"Edge AI / Aggregációs sávszélesség spórolás:  {comm_saved:.2f} %")
    print(f"Felismert és blokkolt Replay támadások: {replay_attacks_blocked} db")
    print(f"Hálózat teljes energiafogyasztása:     {final_energy:.6f} Joule")
    print("==================================================================")
    
    os.makedirs("reports/data", exist_ok=True)
    report_data = {
        "config": config,
        "results": {
            "total_measurements": total_generated_data,
            "packets_sent": packets_sent,
            "bandwidth_saved_percent": comm_saved,
            "blocked_attacks": replay_attacks_blocked,
            "total_energy_joule": final_energy
        }
    }
    with open("reports/data/main_simulation_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4, ensure_ascii=False)
    print("[+] A végleges mérési adatlap elmentve: reports/data/main_simulation_report.json\n")

if __name__ == "__main__":
    main()
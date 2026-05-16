import pytest
from sim.scheduler import Scheduler
from models.security import SecurityManager, SecurePacket
from models.energy import EnergyModel, RadioState

def test_replay_attack_prevention():
    """
    Abuse-case teszt: A visszajátszásos (Replay) támadás modellezése.
    """
    scheduler = Scheduler()
    sec_mgr = SecurityManager(scheduler)
    
    received_packets = []
    def app_layer_receive(packet):
        received_packets.append(packet)
        
    pkt1 = SecurePacket(src_id=1, dest_id=0, seq_num=100, payload="ALARM_FIRE")
    sec_mgr.process_received_packet(pkt1, app_layer_receive)
    scheduler.run(until=0.01)
    
    assert len(received_packets) == 1, "A legitim csomagot el kellett volna fogadni."
    
    pkt_replay = SecurePacket(src_id=1, dest_id=0, seq_num=100, payload="ALARM_FIRE")
    sec_mgr.process_received_packet(pkt_replay, app_layer_receive)
    scheduler.run(until=0.02)
    
    assert len(received_packets) == 1, "Hiba! A REPLAY TÁMADÁS SIKERES! A rendszer kétszer dolgozta fel a riasztást!"
    
    pkt2 = SecurePacket(src_id=1, dest_id=0, seq_num=101, payload="ALARM_CLEAR")
    sec_mgr.process_received_packet(pkt2, app_layer_receive)
    scheduler.run(until=0.03)
    
    assert len(received_packets) == 2, "Az új sorszámú legitim csomagot el kellett volna fogadni."

def test_security_cpu_overhead_delay():
    """
    Teszteli, hogy a biztonsági ellenőrzés (kriptográfia) valóban
    okoz-e feldolgozási késleltetést (CPU overhead).
    """
    scheduler = Scheduler()
    sec_mgr = SecurityManager(scheduler)
    
    process_times = []
    def app_layer_receive(packet):
        process_times.append(scheduler.current_time)
        
    pkt = SecurePacket(src_id=1, dest_id=0, seq_num=1, payload="DATA")
    start_time = scheduler.current_time
    
    sec_mgr.process_received_packet(pkt, app_layer_receive)
    
    assert len(process_times) == 0
    
    scheduler.run(until=0.1)
    expected_finish = start_time + sec_mgr.crypto_delay_s
    
    assert process_times[0] == pytest.approx(expected_finish), "A biztonsági CPU overhead nem érvényesült az időben!"

from models.energy import EnergyModel, RadioState

def test_negative_case_and_energy_overhead():
    """
    Két dolgot mér:
    1. Biztonsági overhead (normál forgalmon): A kripto CPU ideje miatti extra energia.
    2. Negatív teszt: Replay támadás esetén mekkora a kár védelem nélkül, és mennyi energiát ment a szűrő?
    """
    scheduler = Scheduler()
    energy_secure = EnergyModel()
    energy_insecure = EnergyModel()
    sec_mgr = SecurityManager(scheduler)

    def process_packet_secure(pkt):
        t = max(scheduler.current_time, energy_secure.last_update_time)
        energy_secure.update_state(RadioState.RX, t)
        energy_secure.update_state(RadioState.IDLE, t + 0.004)

        def on_success(p):
            t_tx = max(scheduler.current_time, energy_secure.last_update_time)
            energy_secure.update_state(RadioState.TX, t_tx)
            energy_secure.update_state(RadioState.IDLE, t_tx + 0.004)

        sec_mgr.process_received_packet(pkt, on_success)

    def process_packet_insecure(pkt):
        t = max(scheduler.current_time, energy_insecure.last_update_time)
        energy_insecure.update_state(RadioState.RX, t)
        energy_insecure.update_state(RadioState.IDLE, t + 0.004)
        
        energy_insecure.update_state(RadioState.TX, t + 0.004)
        energy_insecure.update_state(RadioState.IDLE, t + 0.008)

    pkt_legit = SecurePacket(src_id=1, dest_id=0, seq_num=1, payload="DATA")
    process_packet_secure(pkt_legit)
    process_packet_insecure(pkt_legit)
    scheduler.run(until=0.1)
    for _ in range(50):
        pkt_replay = SecurePacket(src_id=1, dest_id=0, seq_num=1, payload="DATA")
        process_packet_secure(pkt_replay)
        process_packet_insecure(pkt_replay)

    scheduler.run(until=1.0)
    t_end_secure = max(scheduler.current_time, energy_secure.last_update_time)
    consumed_secure = energy_secure.get_consumed_energy(t_end_secure)

    t_end_insecure = max(scheduler.current_time, energy_insecure.last_update_time)
    consumed_insecure = energy_insecure.get_consumed_energy(t_end_insecure)
    assert consumed_insecure > consumed_secure, "A védelemnek energiát kellett volna spórolnia a támadás alatt!"
    
    print(f"\n--- ENERGIA MÉRÉS (Replay támadás alatt) ---")
    print(f"Fogyasztás VÉDELEMMEL:      {consumed_secure:.6f} J")
    print(f"Fogyasztás VÉDELEM NÉLKÜL:  {consumed_insecure:.6f} J")
    print(f"Megspórolt energia:         {(consumed_insecure - consumed_secure):.6f} J")
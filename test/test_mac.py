import pytest
from sim.scheduler import Scheduler
from models.mac import AlohaMac, CsmaMac

PACKET_DURATION_S = 0.004

def test_aloha_collision_overlap():
    """ALOHA teszt: Az adások átfedik egymást az időben, tehát ütköznek."""
    scheduler = Scheduler()
    transmissions = []
    
    def physical_tx(packet):
        transmissions.append((scheduler.current_time, packet))
        
    mac_node_a = AlohaMac(scheduler, physical_tx)
    mac_node_b = AlohaMac(scheduler, physical_tx)
    
    mac_node_a.send("Packet_A", delay=1.000)
    mac_node_b.send("Packet_B", delay=1.002)
    
    scheduler.run(until=2.0)
    
    time_a = transmissions[0][0]
    time_b = transmissions[1][0] 
    
    time_difference = abs(time_a - time_b)
    assert time_difference < PACKET_DURATION_S

def test_csma_collision_avoidance():
    """
    CSMA teszt: A random backoff miatt a csomagok nem fedik át egymást.
    SEED HASZNÁLATA:
    A teszt reprodukálhatósága érdekében fix seed értékeket használunk.
    - Node A seed = 42
    - Node B seed = 99
    Ha nem adnánk meg seedet, vagy ugyanazt adnánk meg, a két node 
    ugyanazt a véletlen backoff slotot húzná, és a CSMA ellenére is 
    mindig ütköznének.
    """
    scheduler = Scheduler()
    transmissions = []
    
    def physical_tx(packet):
        transmissions.append((scheduler.current_time, packet))
        
    def is_channel_free():
        return True 

    mac_node_a = CsmaMac(scheduler, physical_tx, is_channel_free, seed=42)
    mac_node_b = CsmaMac(scheduler, physical_tx, is_channel_free, seed=99)
    
    mac_node_a.send("Packet_A", delay=1.0)
    mac_node_b.send("Packet_B", delay=1.0)
    
    scheduler.run(until=2.0)
    
    time_a = transmissions[0][0]
    time_b = transmissions[1][0]
    
    time_difference = abs(time_a - time_b)
    assert time_difference >= PACKET_DURATION_S
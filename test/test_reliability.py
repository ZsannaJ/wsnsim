import pytest
from sim.scheduler import Scheduler
from models.reliability import ArqReliability, AckPacket

class DummyPacket:
    """Egyszerűsített csomag a teszteléshez."""
    def __init__(self, seq_num):
        self.seq_num = seq_num

def test_arq_success_no_retry():
    """Teszt 1: Ha megjön az ACK a timeout előtt, nincs újraküldés."""
    scheduler = Scheduler()
    tx_events = []
    
    def mock_tx(packet):
        tx_events.append((scheduler.current_time, packet))
    
    arq = ArqReliability(scheduler, mock_tx, timeout_s=0.05)
    pkt = DummyPacket(seq_num=1)
    
    arq.send_with_retry(pkt, max_retries=3, delay=0.0)
    def mock_receive_ack(payload=None):
        arq.receive_ack(AckPacket(src_id=2, dest_id=1, ack_seq_num=1))
    scheduler.schedule(0.02, mock_receive_ack)
    
    scheduler.run(until=0.2)
    assert len(tx_events) == 1

def test_arq_max_retries():
    """Teszt 2: Ha sosem jön ACK, pontosan (1 normál + max_retries) adás történik."""
    scheduler = Scheduler()
    tx_events = []
    
    def mock_tx(packet):
        tx_events.append((scheduler.current_time, packet))
    
    arq = ArqReliability(scheduler, mock_tx, timeout_s=0.05)
    pkt = DummyPacket(seq_num=2)
    arq.send_with_retry(pkt, max_retries=2, delay=0.0)
    
    scheduler.run(until=0.5)
    assert len(tx_events) == 3
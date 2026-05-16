from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class AckPacket:
    """Egy nyugta (ACK) csomag reprezentációja."""
    src_id: int
    dest_id: int
    ack_seq_num: int

class ArqReliability:
    """
    Automatic Repeat reQuest (ARQ) mechanizmus implementációja.
    Kezeli a csomagok újraküldését, ha nem érkezik nyugta.
    """
    def __init__(self, scheduler, tx_callback: Callable, timeout_s: float = 0.05):
        self.scheduler = scheduler
        self.tx_callback = tx_callback
        self.timeout_s = timeout_s
        
        self.pending_transmissions = {}

    def send_with_retry(self, packet: Any, max_retries: int, delay: float = 0.0):
        """Elindít egy megbízható küldési folyamatot."""
        self.pending_transmissions[packet.seq_num] = {
            'packet': packet,
            'max_retries': max_retries,
            'attempts': 0
        }
        
        self.scheduler.schedule(delay=delay, callback=self._attempt_transmit, payload=packet.seq_num)

    def _attempt_transmit(self, seq_num: int):
        """Egy konkrét küldési (vagy újraküldési) kísérlet végrehajtása."""
        if seq_num not in self.pending_transmissions:
            return
        
        record = self.pending_transmissions[seq_num]
        
        if record['attempts'] <= record['max_retries']:
            record['attempts'] += 1
            self.tx_callback(record['packet'])
            
            self.scheduler.schedule(
                delay=self.timeout_s, 
                callback=self._check_timeout, 
                payload=seq_num
            )
        else:
            del self.pending_transmissions[seq_num]

    def _check_timeout(self, seq_num: int):
        """Ellenőrzi, hogy lejárt-e az idő az ACK megérkezése nélkül."""
        if seq_num in self.pending_transmissions:
            self._attempt_transmit(seq_num)

    def receive_ack(self, ack_packet: AckPacket):
        """A vevő oldali MAC/Fizikai réteg hívja meg, ha ACK érkezik."""
        seq_num = ack_packet.ack_seq_num
        if seq_num in self.pending_transmissions:
            del self.pending_transmissions[seq_num]
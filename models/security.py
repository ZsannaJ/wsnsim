from dataclasses import dataclass
from typing import Dict, Callable, Any

@dataclass
class SecurePacket:
    """A biztonságos hálózati csomag (Extra overhead-del)."""
    src_id: int
    dest_id: int
    seq_num: int
    payload: Any
    extra_bytes: int = 12 

class SecurityManager:
    """
    Kezeli a hálózat biztonsági funkcióit:
    1. Visszajátszás (Replay) elleni védelem.
    2. Kriptográfiai CPU overhead szimulálása.
    """
    def __init__(self, scheduler, energy_model=None):
        self.scheduler = scheduler
        self.energy_model = energy_model
        
        self.replay_cache: Dict[int, int] = {}
        
        self.crypto_delay_s = 0.005 

    def verify_packet(self, packet: SecurePacket) -> bool:
        """
        Ellenőrzi a csomag frissességét.
        Visszatérési érték: True (elfogadva), False (Replay támadás!).
        """
        last_seq = self.replay_cache.get(packet.src_id, -1)
        
        if packet.seq_num <= last_seq:
            return False
            
        self.replay_cache[packet.src_id] = packet.seq_num
        return True

    def process_received_packet(self, packet: SecurePacket, on_success: Callable):
        """
        Szimulálja a csomag fogadása utáni biztonsági feldolgozást.
        A CPU számol (időt és energiát fogyaszt), majd dönt az elfogadásról.
        """
        
        def _crypto_finished(payload=None):
            if self.verify_packet(packet):
                on_success(packet)
            else:
                pass
                
        self.scheduler.schedule(delay=self.crypto_delay_s, callback=_crypto_finished)
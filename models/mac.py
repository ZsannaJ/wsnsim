import numpy as np
from typing import Callable, Any

class AlohaMac:
    """ALOHA protokoll: Azonnali küldés, csatornafigyelés nélkül."""
    def __init__(self, scheduler, tx_callback: Callable):
        self.scheduler = scheduler
        self.tx_callback = tx_callback

    def send(self, packet: Any, delay: float = 0.0):
        """A csomag beütemezése azonnali (vagy adott késleltetésű) küldésre."""
        self.scheduler.schedule(delay=delay, callback=self.tx_callback, payload=packet)


class CsmaMac:
    """CSMA/CA protokoll: Carrier sense és véletlenszerű backoff."""
    def __init__(self, scheduler, tx_callback: Callable, is_channel_free_cb: Callable, 
                 seed: int = None, slot_time: float = 0.001, cwmin: int = 7, cwmax: int = 31):
        self.scheduler = scheduler
        self.tx_callback = tx_callback
        self.is_channel_free = is_channel_free_cb
        self.slot_time = slot_time
        self.cwmin = cwmin
        self.cwmax = cwmax
        self.rng = np.random.default_rng(seed)

    def send(self, packet: Any, delay: float = 0.0):
        """Kezdeti véletlenszerű backoff, majd csatornafigyelés."""
        slots = self.rng.integers(0, self.cwmin)
        backoff_delay = slots * self.slot_time
        
        self.scheduler.schedule(delay=delay + backoff_delay, callback=self._carrier_sense, payload=packet)

    def _carrier_sense(self, packet: Any):
        """Megvizsgálja a csatornát, és dönt a küldésről vagy az újabb várakozásról."""
        if self.is_channel_free():
            self.tx_callback(packet)
        else:
            slots = self.rng.integers(0, self.cwmax)
            retry_delay = slots * self.slot_time
            self.scheduler.schedule(delay=retry_delay, callback=self._carrier_sense, payload=packet)
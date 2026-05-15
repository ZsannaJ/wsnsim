import heapq
import logging
from dataclasses import dataclass, field
from typing import Callable, Any

# Logger inicializálása [cite: 138, 191]
logger = logging.getLogger("wsnsim")
logging.basicConfig(level=logging.INFO, format='%(message)s')

@dataclass(order=True)
class Event:
    time: float
    priority: int
    event_id: int
    callback: Callable = field(compare=False)
    payload: Any = field(compare=False, default=None)

class Scheduler:
    def __init__(self):
        self.current_time = 0.0
        self.event_queue = []
        self._event_counter = 0

    def schedule(self, delay: float, callback: Callable, priority: int = 10, payload: Any = None):
        """Beütemez egy eseményt a jövőbe a jelenlegi időhöz képest."""
        event_time = self.current_time + delay
        
        if event_time < self.current_time:
            raise ValueError("Nem lehet eseményt ütemezni a múltba!")

        self._event_counter += 1
        event = Event(event_time, priority, self._event_counter, callback, payload)
        heapq.heappush(self.event_queue, event)
        
        logger.debug(f"Esemény ütemezve: {event_time:.3f}s-re (ID: {self._event_counter})")

    def run(self, until: float):
        """Futtatja a szimulációt a megadott ideig."""
        logger.info(f"--- Szimuláció indítása (időtartam: {until}s) ---")
        
        while self.event_queue and self.event_queue[0].time <= until:
            event = heapq.heappop(self.event_queue)
            self.current_time = event.time
            
            logger.info(f"[{self.current_time:.3f}s] Esemény végrehajtása (ID: {event.event_id})")
    
            event.callback(event.payload)
        
        logger.info("--- Szimuláció vége ---")
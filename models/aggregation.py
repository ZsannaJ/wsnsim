from abc import ABC, abstractmethod
from typing import List, Optional, Any

class AggregationStrategy(ABC):
    """Absztrakt interfész az adataggregációs és tömörítési stratégiákhoz."""
    
    @abstractmethod
    def receive_data(self, data: float, source_id: int):
        """Fogadja és puffereli a (saját vagy gyermek) szenzoradatokat."""
        pass

    @abstractmethod
    def prepare_payload(self) -> Optional[Any]:
        """
        Elkészíti a továbbítandó adatot. 
        Ha a visszatérési érték None, a rádió nem küld csomagot (tömörítés/delta-kódolás).
        """
        pass


class RawDataForwarding(AggregationStrategy):
    """1. Stratégia: Minden nyers adatot listába gyűjt és továbbít (Nincs aggregáció)."""
    
    def __init__(self):
        self.buffer: List[float] = []

    def receive_data(self, data: float, source_id: int):
        self.buffer.append(data)

    def prepare_payload(self) -> Optional[List[float]]:
        if not self.buffer:
            return None
            
        payload = list(self.buffer)
        self.buffer.clear()
        return payload


class AverageDeltaAggregation(AggregationStrategy):
    """2. Stratégia: Fa menti Átlagolás + Threshold-alapú Delta-kódolás."""
    
    def __init__(self, delta_threshold: float = 0.5):
        self.delta_threshold = delta_threshold
        self.last_sent_value: Optional[float] = None
        
        self.sum_val = 0.0
        self.count = 0

    def receive_data(self, data: float, source_id: int):
        self.sum_val += data
        self.count += 1

    def prepare_payload(self) -> Optional[float]:
        if self.count == 0:
            return None
            
        current_avg = self.sum_val / self.count
        
        if self.last_sent_value is None or abs(current_avg - self.last_sent_value) >= self.delta_threshold:
            self.last_sent_value = current_avg
            self.sum_val = 0.0
            self.count = 0
            return current_avg
        else:
            self.sum_val = 0.0
            self.count = 0
            return None
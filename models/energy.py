from enum import Enum
from dataclasses import dataclass

class RadioState(Enum):
    """A rádiómodul lehetséges állapotai."""
    TX = "TX"
    RX = "RX"
    IDLE = "IDLE"
    SLEEP = "SLEEP"

@dataclass
class EnergyConfig:
    """
    Hardveres energiafogyasztási paraméterek (pl. CC2420 rádióhoz).
    Az értékek Amperben (A) és Voltban (V) értendők[cite: 17].
    """
    voltage: float = 3.0             
    current_tx: float = 0.0174       
    current_rx: float = 0.0188       
    current_idle: float = 0.000426   
    current_sleep: float = 0.0000002 
    
    wake_up_time_s: float = 0.002    # 
    wake_up_current: float = 0.005

class EnergyModel:
    def __init__(self, config: EnergyConfig = EnergyConfig()):
        self.config = config
        self.current_state = RadioState.SLEEP
        self.last_update_time = 0.0
        self.consumed_energy = 0.0
        self.wake_up_count = 0 
        
    def _get_power(self, state: RadioState) -> float:
        """Kiszámítja az adott állapothoz tartozó teljesítményt (Wattban)."""
        currents = {
            RadioState.TX: self.config.current_tx,
            RadioState.RX: self.config.current_rx,
            RadioState.IDLE: self.config.current_idle,
            RadioState.SLEEP: self.config.current_sleep
        }
        return self.config.voltage * currents[state]

    def update_state(self, new_state: RadioState, current_time: float):
        """Állapotváltás végrehajtása és fogyasztás integrálása."""
        dt = current_time - self.last_update_time
        
        if dt < 0:
            raise ValueError("Hiba: Az idő nem haladhat visszafelé!")
            
        power_w = self._get_power(self.current_state)
        self.consumed_energy += power_w * dt
        
        if self.current_state == RadioState.SLEEP and new_state != RadioState.SLEEP:
            wake_up_energy = self.config.voltage * self.config.wake_up_current * self.config.wake_up_time_s
            self.consumed_energy += wake_up_energy
            self.wake_up_count += 1
        
        self.current_state = new_state
        self.last_update_time = current_time

    def get_consumed_energy(self, current_time: float) -> float:
        """Visszaadja a pillanatnyi teljes energiafogyasztást Joule-ban."""
        dt = current_time - self.last_update_time
        if dt < 0:
            raise ValueError("Hiba: Az idő nem haladhat visszafelé!")
            
        power_w = self._get_power(self.current_state)
        return self.consumed_energy + (power_w * dt)
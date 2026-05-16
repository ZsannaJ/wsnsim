import math
import numpy as np
from scipy.optimize import least_squares
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Anchor:
    """Ismert pozíciójú horgonypont a lokalizációhoz."""
    x: float
    y: float

class ClockModel:
    """
    Óra-drift modell: szimulálja egy csomópont hardveres órájának pontatlanságát.
    """
    def __init__(self, ppm: float, initial_offset_s: float = 0.0):
        self.ppm = ppm 
        self.offset = initial_offset_s
        
    def get_local_time(self, true_time: float) -> float:
        """Kiszámolja a node által érzékelt helyi időt a valós idő alapján."""
        drift_factor = self.ppm * 1e-6
        return true_time * (1.0 + drift_factor) + self.offset
        
    def sync_clock(self, true_time: float, reference_local_time: float):
        """Időszinkronizáció szimulálása (pl. TPSN protokoll esetén)."""
        current_drift = true_time * (self.ppm * 1e-6)
        self.offset = reference_local_time - (true_time + current_drift)

class LocalizationModel:
    """RSSI alapú trilateráció modellt biztosít a node-ok helyzetének meghatározására."""
    
    @staticmethod
    def rssi_to_distance(rssi_dbm: float, tx_power_dbm: float = 0.0, path_loss_exp: float = 2.0, d0: float = 1.0) -> float:
        """
        Kiszámítja a becsült távolságot az RSSI alapján az inverz log-distance modellel.
        A zaj (shadowing) eleve benne van az rssi_dbm paraméterben!
        """
        exponent = (tx_power_dbm - rssi_dbm) / (10.0 * path_loss_exp)
        return d0 * (10 ** exponent)

    @staticmethod
    def trilaterate(anchors: List[Anchor], estimated_distances: List[float], initial_guess: Tuple[float, float] = (50.0, 50.0)) -> Tuple[float, float]:
        """
        Legkisebb Négyzetek (Least Squares) alapú trilateráció.
        Numerikusan stabil, rossz geometria vagy zajos metszéspontok esetén is talál egy "legjobb" közelítést.
        """
        if len(anchors) < 3:
            raise ValueError("Legalább 3 horgonypont (anchor) szükséges a 2D trilaterációhoz!")
            
        def error_function(guess_coords):
            x, y = guess_coords
            errors = []
            for anchor, est_d in zip(anchors, estimated_distances):
                calc_d = math.sqrt((x - anchor.x)**2 + (y - anchor.y)**2)
                errors.append(calc_d - est_d)
            return errors
            
        result = least_squares(error_function, initial_guess)
        return result.x[0], result.x[1]
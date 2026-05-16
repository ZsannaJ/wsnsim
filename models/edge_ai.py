import numpy as np
from dataclasses import dataclass
from typing import Tuple

@dataclass
class DetectionMetrics:
    """A detektor teljesítményét leíró metrikák."""
    true_positives: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    true_negatives: int = 0
    total_packets_sent: int = 0
    communication_saved_percent: float = 0.0

class SensorSignalGenerator:
    """Szimulált szenzorjel generátor anomáliákkal (Ground Truth biztosításával)."""
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def generate_signal(self, length: int = 1000, anomaly_prob: float = 0.05) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generál egy zajos szinuszjelet, véletlenszerű tüskékkel (anomáliákkal).
        Visszatérési értékek: (mért_jel_tömb, ground_truth_boolean_tömb)
        """
        time = np.arange(length)
        base_signal = 20.0 + 5.0 * np.sin(time / 10.0) + self.rng.normal(0, 0.5, length)
        
        ground_truth = self.rng.random(length) < anomaly_prob
        
        signal = np.copy(base_signal)
        anomaly_indices = np.where(ground_truth)[0]
        signal[anomaly_indices] += self.rng.choice([15.0, -15.0], size=len(anomaly_indices))
        
        return signal, ground_truth

class ZScoreDetector:
    """
    Baseline Edge AI detektor: Z-score (Standard Score) alapján működik.
    A rádió csak akkor kapcsol be (küld csomagot), ha anomáliát detektál.
    """
    def __init__(self, threshold: float = 3.0, window_size: int = 20):
        self.threshold = threshold
        self.window_size = window_size
        self.window = []

    def process(self, value: float) -> bool:
        """
        Feldolgoz egyetlen adatpontot. 
        Visszatérési érték: True (Anomália detektálva -> küldés), False (Normál -> csend).
        """
        if len(self.window) < self.window_size:
            self.window.append(value)
            return False
        
        mean = np.mean(self.window)
        std = np.std(self.window)
        
        if std == 0:
            std = 0.0001
            
        z_score = abs(value - mean) / std
        is_anomaly = z_score > self.threshold
        
        self.window.pop(0)
        self.window.append(value)
        
        return is_anomaly
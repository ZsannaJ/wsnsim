import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class FLCostModel:
    """Kommunikációs költségmodell a Federated Learninghez."""
    model_size_params: int
    bytes_per_param: int = 4
    tx_energy_per_byte: float = 0.0001

    @property
    def model_size_bytes(self) -> int:
        return self.model_size_params * self.bytes_per_param

    def get_transmission_energy(self) -> float:
        """Kiszámolja egy modell elküldésének energiaigényét."""
        return self.model_size_bytes * self.tx_energy_per_byte

class FederatedNode:
    """Egy WSN csomópont, ami lokális tanítást végez."""
    def __init__(self, node_id: int, ideal_weights: np.ndarray, noise_std: float = 1.0, learning_rate: float = 0.1):
        self.node_id = node_id
        self.learning_rate = learning_rate
        self.local_target = ideal_weights + np.random.normal(0, noise_std, size=ideal_weights.shape)
        
        self.local_weights = None

    def receive_global_model(self, global_weights: np.ndarray):
        """A szervertől kapott globális modellt beállítja sajátjaként."""
        self.local_weights = np.copy(global_weights)

    def local_update(self, steps: int = 1) -> np.ndarray:
        """
        Szimulálja a lokális tanítást (Stochastic Gradient Descent proxy).
        A súlyokat a saját, zajos 'célja' felé mozdítja el.
        """
        for _ in range(steps):
            gradient = self.local_weights - self.local_target
            self.local_weights -= self.learning_rate * gradient
            
        return self.local_weights

class FedAvgServer:
    """A központi Sink, ami a Federated Averaging algoritmust futtatja."""
    def __init__(self, model_size_params: int):
        self.global_weights = np.zeros(model_size_params)

    def aggregate(self, local_weights_list: List[np.ndarray]) -> np.ndarray:
        """
        FedAvg magja: A beküldött lokális modellek (súlyok) átlagolása.
        """
        if not local_weights_list:
            return self.global_weights

        self.global_weights = np.mean(local_weights_list, axis=0)
        return self.global_weights

    def evaluate_convergence(self, ideal_weights: np.ndarray) -> float:
        """Proxy konvergencia metrika: MSE a globális és az ideális (valódi) modell között."""
        mse = np.mean((self.global_weights - ideal_weights) ** 2)
        return mse
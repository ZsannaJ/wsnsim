import numpy as np

class ChannelModel:
    def __init__(self, d0: float = 1.0, pl_d0: float = 50.0, n: float = 2.5, sigma: float = 4.0, seed: int = None):
        """
        Rádiós csatornamodell inicializálása.
        
        :param d0: Referenciatávolság (méter)
        :param pl_d0: Útvonalveszteség a d0 távolságon (dB)
        :param n: Path loss exponent (csillapítási kitevő)
        :param sigma: Shadowing szórása (dB)
        :param seed: Determinisztikus véletlenszám-generátor magja
        """
        self.d0 = d0
        self.pl_d0 = pl_d0
        self.n = n
        self.sigma = sigma
        self.rng = np.random.default_rng(seed)

    def pl(self, d: float) -> float:
        """
        Kiszámítja az ideális (determinisztikus) log-distance path loss-t.
        Matematikai képlet: PL(d) = PL(d0) + 10 * n * log10(d / d0)
        """
        if d <= self.d0:
            return self.pl_d0
        
        return self.pl_d0 + 10 * self.n * np.log10(d / self.d0)
   

    def rssi(self, d: float, tx_power: float = 0.0) -> float:
        """
        Kiszámítja a vevőoldali jelerősséget (RSSI) a shadowing figyelembevételével.

        Matematikai képlet: RSSI = TX_power - (PL(d) + X_sigma)
        
        :param d: Távolság az adó és vevő között (méter)
        :param tx_power: Adóteljesítmény (dBm)
        :return: Vett jelerősség (dBm)
        """
        deterministic_loss = self.pl(d)
        
        shadowing_component = self.rng.normal(loc=0.0, scale=self.sigma)
        
        total_path_loss = deterministic_loss + shadowing_component
        
        return tx_power - total_path_loss
    

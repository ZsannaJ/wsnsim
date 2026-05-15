import pytest
from models.channel import ChannelModel

def test_boundary_distance():
    """Határérték teszt: ha a távolság <= d0, a veszteség pontosan pl_d0."""

    channel = ChannelModel(d0=1.0, pl_d0=50.0)
    
    assert channel.pl(0.5) == 50.0
    assert channel.pl(1.0) == 50.0

def test_monotonicity():
    """Monotonicitás teszt: nagyobb távolság szigorúan nagyobb veszteséget jelent."""
    channel = ChannelModel(n=2.5)
    
    # (d = 10.0 méter):
    # PL(d) = pl_d0 + 10 * n * log10(d / d0) 
    # PL(10.0) = 50.0 + 10 * 2.5 * log10(10.0 / 1.0) = 50.0 + 25 * 1.0
    # PL(10.0) = 75.0
    loss_10m = channel.pl(10.0)

    # (d = 20.0 méter):
    # PL(d) = pl_d0 + 10 * n * log10(d / d0) 
    # PL(20.0) = 50.0 + 10 * 2.5 * log10(20.0 / 1.0) = 50.0 + 25 * 1.30103
    # PL(20.0) = 82.5257
    loss_20m = channel.pl(20.0)
    
    assert loss_20m > loss_10m

def test_reproducibility():
    """Reprodukálhatóság teszt: azonos seed azonos RSSI értékeket eredményez."""

    channel1 = ChannelModel(seed=42, sigma=4.0)
    channel2 = ChannelModel(seed=42, sigma=4.0)

    # PL(d) = pl_d0 + 10 * n * log10(d / d0)
    # PL(15.0) = 50.0 + 10 * 2.5 * log10(15.0 / 1.0) = 50.0 + 25 * 1.17609
    # PL(15.0) = 79.402

    # RSSI(d) = tx_power - (PL(d) + X_sigma_seed)
    # RSSI(15.0) = 0.0 - (79.402 + X_sigma_42)
    # RSSI(15.0) = -79.402 - X_sigma_42
    
    rssi1 = channel1.rssi(d=15.0, tx_power=0.0)
    rssi2 = channel2.rssi(d=15.0, tx_power=0.0)

    assert rssi1 == rssi2

def test_randomness():
    """Véletlenszerűség teszt: a shadowing miatt ugyanaz a távolság eltérő RSSI-t ad."""

    channel = ChannelModel(seed=123, sigma=4.0)

    # RSSI_i = tx_power - (PL(d) + X_sigma_i)
    # RSSI_i = 0.0 - (79.402 + X_sigma_i)
    # RSSI_i = -79.402 - X_sigma_i
    results = [channel.rssi(d=15.0, tx_power=0.0) for _ in range(5)]
    
    assert len(set(results)) > 1
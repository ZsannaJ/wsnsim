import pytest
from models.energy import EnergyModel, RadioState, EnergyConfig

def test_no_negative_energy():
    """Sanity check: Az energia sosem lehet negatív, és az idő nem mehet visszafelé."""
    model = EnergyModel()
    
    assert model.get_consumed_energy(0.0) == 0.0
    
    model.update_state(RadioState.SLEEP, 1.0)
    assert model.get_consumed_energy(1.0) >= 0.0
    
    with pytest.raises(ValueError):
        model.update_state(RadioState.TX, 0.5)

def test_duty_cycle_trend():
    """Kiszámolt trendek ellenőrzése, beleértve az ébredési energiát (wake-up overhead)."""
    config = EnergyConfig()
    
    model_sleep = EnergyModel(config)
    model_sleep.update_state(RadioState.SLEEP, 0.0)
    energy_100_sleep = model_sleep.get_consumed_energy(10.0)
    
    model_rx = EnergyModel(config)
    model_rx.update_state(RadioState.RX, 0.0)
    energy_100_rx = model_rx.get_consumed_energy(10.0)
    
    model_dc = EnergyModel(config)
    model_dc.update_state(RadioState.RX, 0.0)
    model_dc.update_state(RadioState.SLEEP, 1.0)
    energy_10_percent_dc = model_dc.get_consumed_energy(10.0)
    
    assert energy_100_rx > energy_100_sleep * 1000 
    assert energy_100_sleep < energy_10_percent_dc < energy_100_rx
    
    wake_up_cost = config.voltage * config.wake_up_current * config.wake_up_time_s
    expected_energy = (config.voltage * config.current_rx * 1.0) + \
                      (config.voltage * config.current_sleep * 9.0) + \
                      wake_up_cost
                      
    import pytest
    assert energy_10_percent_dc == pytest.approx(expected_energy)
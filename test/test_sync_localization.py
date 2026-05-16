import pytest
import math
from models.sync_localization import ClockModel, LocalizationModel, Anchor

def test_clock_drift_scaling():
    """Teszteli, hogy a PPM skálázás pontosan 1e-6 értékkel történik-e."""
    clock = ClockModel(ppm=20.0)
    
    true_time = 1.0 
    local_time = clock.get_local_time(true_time)
    
    # 1.0 + (1.0 * 20 * 1e-6) = 1.000020
    import pytest
    assert local_time == pytest.approx(1.000020)
    
    event_a_true = 10.0
    event_b_true = 15.0
    
    local_a = clock.get_local_time(event_a_true)
    local_b = clock.get_local_time(event_b_true)
    
    assert (local_b - local_a) == pytest.approx(5.0001)

def test_exact_trilateration_no_noise():
    """Sanity check: Tökéletes, zajmentes mérések esetén a lokalizáció hajszálpontos-e?"""

    anchors = [
        Anchor(0.0, 0.0),
        Anchor(100.0, 0.0),
        Anchor(50.0, 100.0)
    ]
    
    d1 = math.sqrt((50-0)**2 + (50-0)**2)      # 70.7106
    d2 = math.sqrt((50-100)**2 + (50-0)**2)    # 70.7106
    d3 = math.sqrt((50-50)**2 + (50-100)**2)   # 50.0
    
    estimated_distances = [d1, d2, d3]
    
    est_x, est_y = LocalizationModel.trilaterate(anchors, estimated_distances)
    
    assert est_x == pytest.approx(50.0, abs=0.01)
    assert est_y == pytest.approx(50.0, abs=0.01)
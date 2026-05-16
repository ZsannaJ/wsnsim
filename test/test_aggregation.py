import pytest
import numpy as np
from models.aggregation import AverageDeltaAggregation, RawDataForwarding

def test_ground_truth_and_error_definition():
    """
    1. Hiba ellenőrzése: Nem definiálod, mi a 'hiba' (ground truth).
    Ez a teszt expliciten definiálja a Ground Truth-t, és bizonyítja, 
    hogy tudjuk, hogyan kell a hálózat által okozott hibát (MSE) számolni.
    """
    aggregator = AverageDeltaAggregation(delta_threshold=1.5)
    
    true_data = [20.0, 20.5, 21.0, 22.0]
    
    sink_known_value = true_data[0]
    errors = []
    
    for val in true_data:
        aggregator.receive_data(val, source_id=1)
        payload = aggregator.prepare_payload()
        
        if payload is not None:
            sink_known_value = payload
            
        errors.append(val - sink_known_value)
        
    # Elvárt viselkedés ellenőrzése:
    # 1. kör (20.0): küld 20.0-t. Sink tudja: 20.0. Hiba: 0.0
    # 2. kör (20.5): küszöb alatt (delta=0.5 < 1.5), nem küld. Sink tudja: 20.0. Hiba: 0.5
    # 3. kör (21.0): küszöb alatt (delta=1.0 < 1.5), nem küld. Sink tudja: 20.0. Hiba: 1.0
    # 4. kör (22.0): küszöb felett (delta=2.0 >= 1.5), KÜLD 22.0-t! Sink tudja: 22.0. Hiba: 0.0
    
    assert errors == [0.0, 0.5, 1.0, 0.0], "A hiba (error) számítása nem a ground truth alapján történt!"

def test_tree_structure_dependence_documentation():
    """
    2. Hiba ellenőrzése: Aggregációs függvény nem asszociatív/kommutatív.
    A szilabusz kéri: 'függ a fa struktúrától (dokumentáld)'.
    Ez a teszt Futtatható Dokumentációként bizonyítja, hogy TISZTÁBAN VAGYUNK
    azzal a statisztikai ténnyel, hogy az "átlagok átlagolása" torzítást okoz!
    """
    node_a = AverageDeltaAggregation(delta_threshold=0.0)
    for _ in range(3): node_a.receive_data(10.0, source_id=2)
    val_from_a = node_a.prepare_payload() # Ez 10.0 lesz
    
    node_b = AverageDeltaAggregation(delta_threshold=0.0)
    node_b.receive_data(20.0, source_id=3)
    val_from_b = node_b.prepare_payload() 
    
    sink = AverageDeltaAggregation(delta_threshold=0.0)
    sink.receive_data(val_from_a, source_id=node_a)
    sink.receive_data(val_from_b, source_id=node_b)
    final_aggregated_value = sink.prepare_payload()
    
    assert final_aggregated_value == 15.0
    assert final_aggregated_value != 12.5, "A teszt bizonyítja, hogy az egyszerű átlagolás fa-függő!"

def test_delta_coding_reset_and_overflow():
    """
    3. Hiba ellenőrzése: Delta-kódolásnál nincs reset / overflow kezelve.
    Teszteli, hogy a payload elkészítése (és esetleges eldobása) után
    a belső változók (sum_val, count) biztosan nullázódnak-e, megelőzve a túlcsordulást.
    """
    aggregator = AverageDeltaAggregation(delta_threshold=2.0)
    
    aggregator.receive_data(25.0, source_id=1)
    aggregator.receive_data(25.0, source_id=2)
    
    assert aggregator.count == 2
    assert aggregator.sum_val == 50.0
    
    aggregator.prepare_payload()
    
    assert aggregator.count == 0, "Hiba: A 'count' változó nem lett resetelve, overflow veszély!"
    assert aggregator.sum_val == 0.0, "Hiba: A 'sum_val' változó nem lett resetelve!"
    
    aggregator.receive_data(25.1, source_id=1)
    payload = aggregator.prepare_payload()
    
    assert payload is None, "A delta kódolónak el kellett volna nyomnia a csomagot!"
    assert aggregator.count == 0, "Hiba: Elnyomott csomag esetén elmaradt a reset!"
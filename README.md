# wsnsim
Wireless Sensor Network Simulator

A `wsnsim` egy Python-alapú diszkrét eseményű szimulátor (Discrete Event Simulator - DES) vezeték nélküli szenzorhálózatokhoz (WSN). A projekt jelenleg az **M1 (Szimulátor alap) mérföldkőnél** tart.

## Gyors indítás

A szimulátor futtatásához és a függőségek telepítéséhez (Windows/PowerShell környezetben) futtasd az alábbi parancsokat:

```bash
# Virtuális környezet létrehozása és aktiválása
python -m venv .venv
.venv\Scripts\activate

# Függőségek telepítése (pl. pytest, numpy, matplotlib)
pip install -r requirements.txt

# Összes Unit teszt futtatása
python -m pytest -v

# 1. Kísérlet futtatása: PRR vs Távolság
python experiments/run_prr.py

# 2. Kísérlet futtatása: Üzemidő vs Duty Cycle
python experiments/run_energy.py

## Tesztelés és Validálás

A szimulátor megbízhatóságát automatikus unit tesztek garantálják[cite: 46, 715]. A tesztek futtatásához használható parancsok (aktív virtuális környezet mellett a projekt gyökeréből futtatva):


# Az ÖSSZES létező unit teszt futtatása részletes (verbose) módban
python -m pytest -v

# Csak az eseményütemező (Scheduler) motor tesztelése
python -m pytest test/test_scheduler.py -v

# Az eseményütemező tesztelése úgy, hogy az időbélyeges LOG-ok is látszódjanak
python -m pytest test/test_scheduler.py -v --log-cli-level=INFO

# Csak a rádiós csatorna modell (monotonicitás, határértékek) tesztelése
python -m pytest test/test_channel.py -v

# Csak az energiafogyasztási modell és a guard védelmek tesztelése
python -m pytest test/test_energy.py -v

# Csak a MAC protokollok és az időbeli csomag-átfedési ütközések tesztelése
python -m pytest test/test_mac.py -v
```

## Mit szimulálunk?

[cite_start]A jelenlegi verzió a WSN hálózatok fizikai és adatkapcsolati rétegének alapjait modellezi az alábbiak szerint[cite: 713, 714, 719]:
- [cite_start]**Rádiós csatorna:** Log-distance path loss és log-normális árnyékolás (shadowing) hatása a vevőoldali jelerősségre (RSSI)[cite: 211, 216].
- [cite_start]**Energiafogyasztás:** A csomópontok hardveres állapotai (TX, RX, IDLE, SLEEP) és az állapotváltások (SLEEP modból való ébredési) költségei alapján, integrált módon számolja az elhasznált energiát[cite: 252, 257].
- [cite_start]**Közeg-hozzáférés (MAC):** ALOHA és CSMA/CA protokollok, különös tekintettel a véletlenszerű backoff mechanizmusra és az időben átfedő adásokból fakadó ütközések (kollíziók) elkerülésére[cite: 298, 302].

[cite_start]**Mért hálózati metrikák[cite: 144, 748]:**
- [cite_start]**PRR (Packet Reception Ratio):** A sikeresen megérkezett csomagok aránya a távolság és a környezeti zaj függvényében[cite: 144, 213].
- [cite_start]**Becsült élettartam (Lifetime):** A csomópont várható működési ideje napokban kifejezve, a rádió Duty Cycle (ébrenléti) arányának függvényében[cite: 144, 253].

## Modulok

[cite_start]A szimulátor kódja szigorúan követi az alábbi modularitási elveket a felelősségek szétválasztása érdekében[cite: 30, 81, 140]:
- [cite_start]`sim/scheduler.py`: A diszkrét eseményű (DES) motor[cite: 87]. [cite_start]Prioritásos eseménylistát (heap queue) kezel, determinisztikus tie-breaker-rel ellátva az azonos időpontú események sorrendezéséhez[cite: 133, 712].
- [cite_start]`models/channel.py`: Útvonalveszteség és RSSI jelerősség számítás, Monte Carlo alapú PRR generálással[cite: 88, 216].
- [cite_start]`models/energy.py`: Állapotgépes fogyasztáskövetés és az elhasznált Joule-ok idő alapú integrálása[cite: 88, 257].
- [cite_start]`models/mac.py`: Adatkapcsolati közeg-hozzáférési logikák (`AlohaMac`, `CsmaMac`)[cite: 88, 302].
- [cite_start]`test/`: Automatizált egységtesztek a determinizmus, a fizikai határértékek és a MAC ütközések ellenőrzésére[cite: 46, 93].
- [cite_start]`experiments/`: Futtatható kísérleti szkriptek és mérések (paraméter-söprések)[cite: 47, 96].

## Reprodukálhatóság

**Seed kezelése:** Minden sztochasztikus folyamat (a csatorna shadowing komponense és a CSMA random backoff slotjai) a numpy.random.default_rng(seed) megoldásra épül. A tesztekben és kísérletekben a seed értékek fixen rögzítettek (pl. 42, 99, 123).  
**Output fájlok helye:** A kísérleti futások által generált diagramok és vizualizációk automatikusan a reports/figures/ könyvtárba mentődnek el PNG formátumban.  
**Promptlog:** A fejlesztés és a tervezés során hozott mérnöki MI-döntések a transzparencia érdekében a prompt.md fájlban vannak vezetve.  

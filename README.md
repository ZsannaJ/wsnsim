# Első mérföldkő

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



# Második mérföldkő


# wsnsim
Wireless Sensor Network Simulator

A `wsnsim` egy Python-alapú diszkrét eseményű szimulátor (Discrete Event Simulator - DES) vezeték nélküli szenzorhálózatokhoz (WSN). A projekt jelenleg az **M2 (Protokollok) mérföldkőnél** tart.

## Gyors indítás

A szimulátor futtatásához és a függőségek telepítéséhez (Windows/PowerShell környezetben) futtasd az alábbi parancsokat:

```bash
# Virtuális környezet létrehozása és aktiválása
python -m venv .venv
.venv\Scripts\activate

# Függőségek telepítése (pl. pytest, numpy, matplotlib, networkx)
pip install -r requirements.txt

# Összes Unit teszt futtatása
python -m pytest -v

# 1. Kísérlet: PRR vs Távolság (Csatornamodell)
python experiments/run_prr.py

# 2. Kísérlet: Üzemidő vs Duty Cycle (Energiamodell)
python experiments/run_energy.py

# 3. Kísérlet: Topológia generálás és vizualizáció (M2)
python experiments/run_topology.py

# 4. Kísérlet: Flooding vs. Sink-fa routing összehasonlítása (M2)
python experiments/run_routing_compare.py

# 5. Kísérlet: Megbízhatóság (PDR) vs. Energiafogyasztás trade-off (M2)
python experiments/run_reliability.py

Tesztelés és Validálás

A szimulátor megbízhatóságát automatikus unit tesztek garantálják. A specifikus modulok teszteléséhez használd az alábbiakat:
```

# Alapmodulok (M1)
python -m pytest test/test_scheduler.py -v
python -m pytest test/test_channel.py -v
python -m pytest test/test_energy.py -v
python -m pytest test/test_mac.py -v

# Protokollok és Hálózat (M2)
python -m pytest test/test_topology.py -v     # Összefüggőség és Sink elérés tesztelése
python -m pytest test/test_routing.py -v      # Flooding végtelen ciklus elleni védelem tesztelése
python -m pytest test/test_reliability.py -v  # ARQ (ACK + Retry) és timeout mechanizmus tesztelése

**Mit szimulálunk?**

A jelenlegi verzió (M2) a fizikai rétegtől egészen az adatkapcsolati és hálózati (routing) rétegig modellezi a WSN hálózatokat:

    Rádiós csatorna: Log-distance path loss és log-normális árnyékolás (shadowing) hatása a vevőoldali jelerősségre (RSSI).

    Energiafogyasztás: A csomópontok hardveres állapotai (TX, RX, IDLE, SLEEP) és az állapotváltások (ébredési) költségei alapján integrálja a fogyasztást.

    Közeg-hozzáférés (MAC): ALOHA és CSMA/CA protokollok, véletlenszerű backoffal és csatornafigyeléssel az ütközések elkerülésére.

    Topológia: Különböző elrendezési stratégiák (Random, Grid, Cluster) és a rádiós hatótávon alapuló szomszédsági gráfok (NetworkX) vizsgálata.

    Routing (Útválasztás): Többugrásos (multi-hop) adatgyűjtés a központi Sink felé. Vizsgált stratégiák: egyszerű elárasztás (Flooding) TTL védelemmel, BFS-alapú feszítőfa (Sink-Tree), és ETX-alapú intelligens szülőválasztás.

    Megbízhatóság (Reliability / ARQ): Nyugtázás (ACK), időtúllépés (Timeout) és újraküldés (Retry). Segítségével modellezhető a PDR (Siker arány) és az extra energiafogyasztás közti kompromisszum (trade-off).

**Mért hálózati metrikák:**

    PRR / PDR: A sikeresen megérkezett csomagok aránya a csatorna vagy a routing réteg szempontjából.

    Hálózati terhelés: A rádiós adások (TX) teljes száma (kifejezetten fontos a flooding vs. fa routing összehasonlításánál).

    Becsült élettartam: A csomópontok energia-büdzséjének kimerülési ideje.

**Modulok**

A szimulátor kódja szigorúan követi a modularitás elvét:

    sim/scheduler.py: A diszkrét eseményű (DES) motor prioritásos eseménylistával.

    models/channel.py: Útvonalveszteség, RSSI és PRR számítás.

    models/energy.py: Állapotgépes fogyasztáskövetés (Joule).

    models/mac.py: Adatkapcsolati közeg-hozzáférési logikák.

    models/topology.py: Csomópontok elhelyezése és szomszédsági gráfok építése.

    models/routing.py: Hálózati réteg és útválasztási protokollok (FloodingRouting, TreeRouting).

    models/reliability.py: ARQ protokoll (ACK + Retry) a csomagvesztések kompenzálására.

    test/: Automatizált egységtesztek a TDD szemlélet fenntartásáért.

    experiments/: Futtatható kísérleti szkriptek és vizualizációk.

**Reprodukálhatóság**

Seed kezelése: Minden sztochasztikus folyamat a numpy.random.default_rng(seed) megoldásra épül. A tesztekben és kísérletekben a seed értékek fixen rögzítettek, garantálva a determinisztikus működést a fair protokoll-összehasonlításokhoz.

Output fájlok helye: A kísérleti futások által generált vizualizációk (PNG diagramok) a reports/figures/ könyvtárba mentődnek.

Promptlog: A fejlesztés során hozott mérnöki MI-döntések a prompt.md fájlban vannak vezetve.
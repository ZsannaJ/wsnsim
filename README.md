# Vezeték Nélküli Szenzorhálózat Szimulátor

## Vezetői Összefoglaló (Executive Summary)

A `wsnsim` egy Python-alapú, moduláris diszkrét eseményű szimulátor (DES), amely a vezeték nélküli szenzorhálózatok (WSN) teljes protokollvermét modellezi a fizikai rétegtől az alkalmazási rétegig. A féléves projekt célja a tipikus tervezési kompromisszumok – mint az energiafogyasztás minimalizálása és a hálózati megbízhatóság (PDR) maximalizálása – adatalapú vizsgálata és optimalizálása. A szimulátor magában foglalja a valósághű rádiós csatornamodellezést (log-normal shadowing), az állapotgép-alapú energiamodellt, a MAC (ALOHA, CSMA/CA) és hálózati (Flooding, Sink-fa) protokollokat, valamint az ARQ megbízhatósági mechanizmusokat.

Az alapvető hálózati funkciókon túl a rendszer intelligens in-network feldolgozást is végez: a Z-Score alapú Edge AI anomáliadetektor és a delta-kódolásos aggregáció együttesen több mint 95%-os sávszélesség- és energiamegtakarítást eredményez. Ezt egészíti ki a biztonsági modul, amely sikerrel blokkolja a Replay (visszajátszásos) támadásokat, megvédve a csomópontokat a lemerüléstől. A projektet az M4 mérföldkő keretében egy automatizált Design Space Exploration (DSE) framework zárja, amely paraméter-söpréssel és matematikai Pareto-szűréssel azonosítja az optimális kompromisszumokat. A mérnöki eredmények hitelességét a szigorú determinizmus (seed-kezelés), a teljes reprodukálhatóság és az automatizált unit tesztek (TDD) garantálják.

A projekt legfőbb eredményei:
1. **Intelligens Adattömörítés:** A Z-Score alapú Edge AI anomáliadetektor és a delta-kódolásos aggregáció együttesen **>95%-os sávszélesség-megtakarítást** eredményezett.
2. **Kiberbiztonság:** A Szekvenciaszám-alapú védelmi modul sikerrel blokkolta a Replay (visszajátszásos) támadásokat, megakadályozva a védelem nélküli node-ok lemerítését.
3. **Pareto-Optimalizálás:** Egy automatikus Design Space Exploration (DSE) framework segítségével térképeztük fel a MAC/Routing paramétereket, megtalálva az optimális Pareto-frontot az energia és a PDR között.

A projekt teljes működését demonstráló integrált szimuláció (Edge AI + Aggregáció + ARQ + Security) egyetlen paranccsal futtatható. A telepítés és futtatás menete:

```bash
# 1. Virtuális környezet létrehozása és aktiválása
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

# 2. Függőségek telepítése
pip install -r requirements.txt

# 3. AZ INTEGRÁLT M4 SZIMULÁCIÓ FUTTATÁSA
python experiments/run_main.py
```

Az eredmények és a konfiguráció automatikusan mentésre kerül a reports/data/main_simulation_report.json fájlba.


## Tesztelés és Validálás

A szimulátor megbízhatóságát automatikus unit tesztek garantálják. A tesztek futtatásához használható parancsok (aktív virtuális környezet mellett a projekt gyökeréből futtatva)
```bash
# Az ÖSSZES létező unit teszt futtatása részletes (verbose) módban
python -m pytest -v

# Csak az eseményütemező (Scheduler) motor tesztelése
python -m pytest test/test_scheduler.py -v

# Az eseményütemező tesztelése úgy, hogy az időbélyeges LOG-ok is látszódjanak
python -m pytest test/test_scheduler.py -v --log-cli-level=INFO

# Csak a rádiós csatorna modell (monotonicitás, határértékek) tesztelése
python -m pytest test/test_channel.py -v

# Csak az energiafogyasztási modell és a guard védelmek (időutazás blokkolása) tesztelése
python -m pytest test/test_energy.py -v

# Csak a MAC protokollok és az időbeli csomag-átfedési ütközések tesztelése
python -m pytest test/test_mac.py -v

# Hálózati topológia, gráf összefüggőség (connectivity) és grid generátor tesztelése
python -m pytest test/test_topology.py -v

# Útvonalválasztás (Flooding és Sink-fa), hurok-elkerülés és TTL (Time-To-Live) tesztelése
python -m pytest test/test_routing.py -v

# Megbízhatósági protokollok (ARQ, ACK timeout, újraküldési limitek) tesztelése
python -m pytest test/test_reliability.py -v

# Óra-drift modellezés és RSSI-alapú trilateráció matematikai pontosságának tesztelése
python -m pytest test/test_sync_localization.py -v

# Adataggregációs torzítások (fa-struktúra függőség) és delta-kódolás buffer-reset tesztelése
python -m pytest test/test_aggregation.py -v

# Kiberbiztonsági Abuse-case tesztek (Replay támadás védelme és az ebből adódó energia-spórolás)
python -m pytest test/test_security.py -v

# Design Space Exploration (DSE), kombinatorikus generátor és Pareto-dominancia algoritmus tesztelése
python -m pytest test/test_optimization.py -v
```

## Mit szimulálunk? (Esettanulmány és Szcenárió)

A projekt fő kísérlete egy **100 csomópontból álló, random eloszlású** vezeték nélküli szenzorhálózatot szimulál, amelynek közepén egyetlen központi adatgyűjtő (Sink) található. 
* **Forgalom (Traffic):** A csomópontok Edge AI (Z-Score) modellt futtatnak. Csak akkor kapcsolják be a rádiót, ha a nyers szenzorjelekben anomáliát detektálnak. A forgalom tehát ritka, de rendkívül kritikus.
* **Mért metrikák:** Csomagcélbaérési arány (PDR), Hálózati energiafogyasztás (Joule), Fals pozitív riasztások száma, és Kommunikációs sávszélesség megtakarítás (%).

## Tervezési kompromisszumok és Pareto-elemzés
A féléves projekt legfontosabb döntéseit egy Design Space Exploration (DSE) paraméter-söprés segítségével hoztuk meg. Három tipikus design alternatívát vizsgáltunk:
1. **"Brute Force" alternatíva (Magas TX power, ALOHA, sok újraküldés):** Garantálja a közel 100%-os PDR-t, de az energiafogyasztás az állandó ütközések miatt az egekbe szökik.
2. **"Túl optimista" alternatíva (Alacsony TX power, újraküldés nélkül):** Kiváló energiahatékonyság, azonban a PDR elfogadhatatlanul alacsonyra (40-50%) esik a csatornazaj és a rejtett állomás probléma miatt.
3. **A Pareto-optimális választás (Közepes TX power, CSMA/CA, limitált ARQ):** A matematikai dominancia-vizsgálat megmutatta az "arany középutat". A CSMA/CA backoff mechanizmusának és 3-as limitű ARQ beállításának köszönhetően >90% PDR-t értünk el, az energiafogyasztás minimalizálása mellett.

## A Szimulátor Architektúrája (Modulok)

A félév során a szimulátor az alábbi, szigorúan szétválasztott modulokból épült fel:

* `sim/`: Determinisztikus diszkrét eseményű (DES) motor (időzítő, eseménysor).
* `models/channel.py`: Log-distance útvonalveszteség és shadowing PRR modell.
* `models/energy.py`: Állapotgép (TX/RX/IDLE/SLEEP) bázisú energia-integrátor.
* `models/mac.py`: Adatkapcsolati logikák (ALOHA, CSMA/CA).
* `models/topology.py`: Random/Grid hálózat generálás és gráf összefüggőség.
* `models/routing.py`: Hálózati réteg (Flooding és Sink-fa routing).
* `models/reliability.py`: Megbízhatósági réteg (ARQ, ACK timeout, Retry).
* `models/sync_localization.py`: Óra-drift szimuláció és RSSI-alapú trilateráció.
* `models/aggregation.py`: In-network processing, delta-kódolás.
* `models/security.py`: Threat modell, CPU overhead szimuláció és Replay-támadás védelem.
* `models/edge_ai.py` & `federated.py`: Node-oldali anomália detektor és FedAvg baseline.
* `models/optimization.py`: Paraméter-grid generátor és Pareto-front szűrés.

## WSN Threat Model (Biztonsági Fókusz)

A projekt külön figyelmet fordít a kiberbiztonságra. A `security` modul a következőket fedi le:
- **Támadási felület:** A rádiócsatorna nyílt, így az adatok lehallgathatók és visszajátszhatók (Replay Attack).
- **Védekezés:** A csomagok szekvenciaszámozást (Sequence Numbers) kapnak. A Sink eldobja a duplikált/régi sorszámú csomagokat, megakadályozva, hogy a támadó hamis riasztásokkal lemerítse a hálózatot.


## WSN Threat Checklist (Fenyegetési Modell) a wsnsim-hez

A WSN hálózatok biztonsági modellje a fizikai hozzáférés hiánya és a nyílt rádiócsatorna miatt egészen speciális. Íme a projektünkre szabott checklist:

**Védendő Értékek (Assets):**

- Szenzoradatok (Integritás és Hitelesség): A Sink-nek biztosnak kell lennie abban, hogy a kapott riasztás/adat valós, és egy legitim node-tól származik.

- Hálózati rendelkezésre állás (Availability): A hálózatnak képesnek kell lennie adatot továbbítani a Sink felé.

- A node-ok energiája (Battery life): A szenzorok legértékesebb erőforrása. Ha lemerítik őket, a hálózat (vagy egy része) meghal.

**A Támadó (Attacker Model):**

- Kívülálló (Outsider): Nincsenek meg a hálózati titkosító kulcsai. Csak lehallgatni (sniffing), zavarni (jamming) vagy rögzített üzeneteket visszajátszani (replay) tud.

- Belső támadó (Insider): Fizikailag elfogott és kompromittált node. Ismeri a kulcsokat, képes hamis adatokat generálni vagy a routingot manipulálni (pl. Sinkhole attack).

- Erőforrások: Mote-class (egy másik szenzor a támadó) vs. Laptop-class (végtelen energiájú, erős antennával rendelkező támadó).

**Támadási Felület (Attack Surface):**

- Fizikai/MAC réteg: Folyamatos zavarás (Jamming) vagy szándékos ütközések generálása (Collision induction), ami újraküldésekre kényszeríti a node-okat, lemerítve az akkumulátorokat.

- Routing réteg: Hamis útvonalak hirdetése. Például a támadó azt hazudja, hogy ő a Sink (Sinkhole attack), így minden forgalmat magához vonz és eldob (Blackhole attack).  

- Adatkapcsolat: Visszajátszásos támadás (Replay Attack). A támadó lehallgat egy tegnapi "Tűzriadó!" csomagot, és ma újra besugározza a hálózatba.

**Védekezések (Mitigations):**

- Integritás védelem: Message Authentication Code (MAC/MIC) hozzáadása a csomaghoz.

- Replay védelem: Szekvenciaszámok (Sequence Numbers) vagy Nonce-ok (egyszer használatos véletlen számok) beágyazása a csomagokba.  

- Titkosítás: A payload titkosítása (bár ez önmagában nem véd a replay vagy jamming ellen).

## Reprodukálhatóság és Transzparencia

A tudományos és mérnöki reprodukálhatóság garantálása a projekt alapköve:

- **Determinizmus:** Minden sztochasztikus folyamat egy központi `seed` alapján fut (alapértelmezetten `seed=42`).
- **Config Dump:** A kísérletek paraméterei automatikusan mentődnek a `reports/data/` könyvtárba JSON formátumban.
- **Kimenetek:** A nyers CSV eredmények és a kigenerált diagramok a `reports/` mappában érhetők el.
- **Egygombos futtatás:** A fő pipeline és a kísérletek egyetlen CLI paranccsal reprodukálhatók.
- **MI Transzparencia:** Az LLM eszközök használatát, a generált javaslatokat és a meghozott mérnöki döntéseket a projekt gyökerében található `PROMPTLOG.md` fájl dokumentálja.

## Reproducibility Checklist

A kísérletek és a Pareto-optimalizálás reprodukálhatóságának biztosítása érdekében az alábbiakat ellenőriztem:

### 1. Kód és Környezet
- [ ] **Függőségek rögzítve:** A projekt gyökerében található egy naprakész `requirements.txt` fájl (pl. `pip freeze > requirements.txt`), ami tartalmazza az összes szükséges csomagot (numpy, matplotlib, scipy, stb.).
- [ ] **Egygombos indítás:** A fő kísérlet (pl. a 13. heti sweep) egyetlen, a README-ben világosan leírt paranccsal indítható (pl. `python experiments/run_sweep.py`).
- [ ] **Nincsenek hardkódolt, gép-specifikus útvonalak:** A kód relatív elérési utakat használ (pl. `reports/figures/...`), így bármelyik mappába klónozva lefut hiba nélkül.

### 2. Determinizmus és Seed
- [ ] **Központi Seed rögzítése:** Minden sztochasztikus folyamat (csatorna zaj, backoff, anomália generálás) egy fix, előre megadott seed-del inicializálódik (pl. `np.random.default_rng(42)`).
- [ ] **Determinisztikus eseményütemező:** A `Scheduler` `heapq` implementációja tartalmaz tie-breakert (pl. beillesztési sorszámot), így az azonos időbélyegű események mindig ugyanabban a sorrendben hajtódnak végre.

### 3. Konfiguráció Menedzsment
- [ ] **Config Dump (Paraméterek mentése):** A kísérlet futtatása során a szkript automatikusan kimenti a használt paramétereket és sweep tartományokat egy `config_dump.json` (vagy YAML) fájlba.
- [ ] **Verziókövetés:** A futtatott kód egy adott, címkézett Git commit-hoz (pl. `tag: m4-final`) tartozik.

### 4. Adatok és Kimenetek
- [ ] **Nyers eredmények mentése:** A paraméter-söprés összes futásának eredménye kimentésre kerül egy `reports/data/sweep_results.csv` fájlba, a Pareto-szűrés előtt.
- [ ] **Automata ábragenerálás:** Az ábrák automatikusan elmentődnek a `reports/figures/` mappába.
- [ ] **Ábrák minősége:** Minden ábrán szerepel értelmezhető tengelyfelirat (mértékegységgel), cím, és egyértelmű jelmagyarázat (Legend). A felhasznált seed és a fő paraméterek fel vannak tüntetve a diagramon vagy annak feliratában.

### 5. Transzparencia
- [ ] **PROMPTLOG.md frissítve:** A fájl tartalmazza az utolsó hetek MI-használatának lényegét (milyen kódot generáltam, milyen döntéseket hoztam a javaslatok alapján).
- [ ] **Esettanulmány / Mini Riport:** A README elején vagy egy külön fájlban található egy rövid vezetői összefoglaló a Pareto-front eredményeiről és a választott "ideális" mérnöki kompromisszum indoklásáról.
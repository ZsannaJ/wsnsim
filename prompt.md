### 1. Prompt - Első hét

**Prompt (röviden):**

Tervezd meg a wsnsim minimális architektúráját modulokra bontva (sim, models, scenarios, metrics).
Adj 5-10 függvény-szignatúrát.
Írj egy minimal event scheduler-t heapq-val: schedule(time, callback), run(until). Adj hozzá unit
teszteket determinisztikus sorrendre. 

**Kontextus:**

Egy lokális fájlba összeolóztam a feladat leírását hogy tudja mik a célok és a használandó eszközök

**MI válasz lényege:**

Javasolt függvény-szignatúrák ajánlása. Minimal Event Scheduler kód generálása. Unit tesztek generálása a determinisztikus sorrendre.

**Döntésem / módosításaim:**

Kódokat átolcvastam kicsit javítottam majd 2 körben kijavítottam a futás során felmerülő hibákat amik felléptek.

### 2. Prompt - Első hét

**Prompt (röviden):**

Át tudod nézni az eddigi kódokat, hogy hol lehet nondeterminism, hol kell seed? 

**MI válasz lényege:**

Code Review: Determinizmus és Seed hosszan kifejtve ajánlásokat adott hogy melyik részein a kódoknak ajánlott a nondeterminism és a seed.

### 3. Prompt - Első hét

**Prompt (röviden):**

Adj logolást a tesztekhez hogy lehessen követni a lefutásukat.
(python -m pytest test/test_scheduler.py --log-cli-level=INFO)

### 4. Prompt - Első hét

**Prompt (röviden):**

Csinálj nekem egy helo simulation példát mert jelenleg ez nincs megvalósulva a kódomban. Ezen kívül a logger modul pontosan működik, ezt hozzáadod ha még nincs? 

**Kontextus:**

scheduler.py fájl kódja

**MI válasz lényege:**

A sim/scheduler.py kód kiegészítése logolással a logging könyvtárat használva.
Alap hello_sim.py kód legenerálása

**Döntésem / módosításaim:**

Az új kódok átnézése és 2 körben való javítása amíg a felmerülő hibák meg nem szűntek.

### 5. Prompt - Második hét

**Prompt (röviden):**

Implementáld a log-distance + log-normal shadowing modellt Pythonban: pl(d), rssi(d). Javasolj paramétereket (n, sigma). Majd adj unit teszt ötleteket a csatorna modellre: monotonicitás, határértékek (d→d0), seed hatás. 

**MI válasz lényege:**

channel.py  alapjainak generálása valamint több unit teszt ötlet felvázolása

**Döntésem / módosításaim:**

Kódok átnézése és alapszintű átírása ott ahol hibásnak találtam

### 6. Prompt - Második hét

**Prompt (röviden):**

Meg tudod csinálni a határérték, monotonicitás teszteket valamint a reprodukálhatóságra illetve véletlenszerűségre vonatkozó teszteket. Meg tudod adni a futtatási kódot. 

**MI válasz lényege:**

test_channel.py alapjainak legenerálása

**Döntésem / módosításaim:**

Szükséges köyvtárak telepítése és requirements frissítése valamint 2 körben a futás során fellépő hibák javítása pár alap kód javítással hibák

### 7. Prompt - Második hét

**Prompt (röviden):**

Készíts egy kísérletet: PRR(d) görbe több sigma értékre; hogyan ábrázoljam?

**MI válasz lényege:**

run_prr.py alapjának legenerálása és álltalános ajánlás az ábrázolás módjáról

**Döntésem / módosításaim:**

Kód átnézése kissebb javítáésok a megfelelő működés érdekében


### 8. Prompt - Második hét

**Prompt (röviden):**

Ezekből mindegyik teljesül, át tudod nézni te is gyorsan a kódot?
• channel modul: PRR(distance) + shadowing opció. ✅
• Egy ábra: PRR vs távolság (legalább 2 paraméter beállítással). ✅
• Validálás: kézi számítás 2 ponton dokumentálva ❌

### 9. Prompt - Második hét

**Prompt (röviden):**

Be tudsz tenni a chaneles függvényhívásokhoz egy alap kikommentelt számítás részt ahova a kézzel számolt eredményeket is majd be tudom helyettesíteni? Olyat hogy matematikai művelet = matematikai művelet behelyettesített számokkal eredmény. Ki tudod te is számolni hogy ellenőrizzem az én eredményemet a tiéddel?

**Kontextus:**

test_channel.ps kódok

**MI válasz lényege:**

"Természetesen! Ez egy nagyon jó gyakorlat, hiszen a szimulátorokban (és a tesztekben) a "black box" (fekete doboz) szerű működés helyett mindig látnunk kell a pontos matematikát.
Az alábbiakban frissítettem a test_channel.py fájlodat..."

**Döntésem / módosításaim:**

Mivel különböző számolásoknál különböző módon történt a megjelenítés egyet kiválasztottam ét átalakítottam kicsit hogy olvashítóbb legyen majd ezt a formátumot átmásoltam a többi számolás helyrére behelyettesítve ez adott számolás adatait.

### 10. Prompt - Harmadik hét

**Prompt (röviden):**

 Tervezd meg az energy state machine-t (enum) és az energia integrálását események alapján. Adj API-t és dataclass struktúrát. Írj teszteket: negatív energia ne legyen; duty-cycle mellett az átlagos fogyasztás kövesse az elvárt
trendet. 

**MI válasz lényege:**

Elméleti alapok összegzése, energy.py és test_energy.py alapkódjának legenerálása.

**Döntésem / módosításaim:**

Kód átnézése kissebb javítáésok a megfelelő működés érdekében


### 11. Prompt - Harmadik hét

**Prompt (röviden):**

Tudsz adni egy a korábbihoz hasonló experiment filet ami Egy mini-kísérlet: duty cycle vs becsült üzemidő (grafikon) hoz létre? 

**MI válasz lényege:**

run_energy.py alapkódjának legenerálása.

**Döntésem / módosításaim:**

Kód átnézése kissebb javítáésok a megfelelő működés érdekében

### 12. Prompt - Harmadik hét

**Prompt (röviden):**

 Adj egy 'sanity check' checklistet az energia modellhez. Sanity check: 'negatív energia' guard + teszt. 

 **MI válasz lényege:**

 ✅ WSN Energia Modell - Sanity Check Checklist

 **Döntésem / módosításaim:**

 Átalakítottam a test_no_negative_energy() függvényt az ajánlott módon

### 13. Prompt - Harmadik hét

**Prompt (röviden):**

  Át tudod te is nézni a kódot hogy biztosan minden benne legyen a következők közül?

Tipikus hibák és gyors ellenőrzések

• A teljesítmény (W) és energia (J) keverése.

• Nem veszed figyelembe az állapotváltások (switching) költségét (ha modellezed, dokumentáld).

• A rádió RX/TX időtartam nincs konzisztensen számolva (packet duration).

Kritériumok

• energy modul: állapotgép + fogyasztás integrálása idő szerint.

• Egy mini-kísérlet: duty cycle vs becsült üzemidő (grafikon).

• Sanity check: 'negatív energia' guard + teszt. 

 **MI válasz lényege:**

 Checklist a megadott pontok ellenörzéséről és hogy mennyire teljeasítik a feltételt

### 14. Prompt - Harmadik hét

**Prompt (röviden):**

Modellezd le az állapotváltozások energiaigényét. Valamint nem lehetne a run_energybe most megcsinálni a konzisztens számolást, le tudod generálni?

 **MI válasz lényege:**

 models/energy.py, experiments/run_energy.py, test/test_energy.py kódjavítási javaslatok

  **Döntésem / módosításaim:**

  átnéztem a javítási javaslatokat és szelektálva átalakítottam a kódokat pár helyen

### 15. Prompt - Harmadik hét

**Prompt (röviden):**

Nézd át ezeket a kódokat hogy most megfelelnek e a kitételeknek.

  Át tudod te is nézni a kódot hogy biztosan minden benne legyen a következők közül?


Tipikus hibák és gyors ellenőrzések

• A teljesítmény (W) és energia (J) keverése.

• Nem veszed figyelembe az állapotváltások (switching) költségét (ha modellezed, dokumentáld).

• A rádió RX/TX időtartam nincs konzisztensen számolva (packet duration).


Kritériumok

• energy modul: állapotgép + fogyasztás integrálása idő szerint.

• Egy mini-kísérlet: duty cycle vs becsült üzemidő (grafikon).

• Sanity check: 'negatív energia' guard + teszt. 

**Kontextus:**

models/energy.py, experiments/run_energy.py, test/test_energy.py

 **MI válasz lényege:**

 Checklist a megadott pontok ellenörzéséről és hogy mennyire teljeasítik a feltételt

 ### 16. Prompt - Negyedik hét

**Prompt (röviden):**

 Írj ALOHA MAC modult (send at will) és CSMA backoff-ot (carrier sense + random backoff). Adj

paramétereket (slot, cwmin, cwmax). Készíts determinisztikus teszt-szcenáriót két node-al: egyszerre küldés → ütközés. Mi az elvárt viselkedés ALOHA vs CSMA esetén?

 **MI válasz lényege:**

models/mac.py, test/test_mac.py alapkódjainak legenerálása. "Mi az elvárt viselkedés ALOHA vs CSMA esetén?" kérdés kifejtése.

 ### 17. Prompt - Negyedik hét

**Prompt (röviden):**

 Generálj összehasonlító táblázatot: ALOHA/CSMA/TDMA pro-kontra WSN szemszögből

  ### Edit

**Prompt (röviden):**

  Generálj összehasonlító táblázatot: ALOHA/CSMA/TDMA pro-kontra WSN szemszögből, olyan legyen amit md fileba tzudok tenni és aztán megjelenik normálisan 

   **MI válasz lényege:**

  ### ALOHA, CSMA/CA és TDMA protokollok összehasonlítása WSN szemszögből

| Protokoll | Alapelv | Előnyök (Pro) | Hátrányok (Contra) | Energiahatékonyság | Skálázhatóság és Komplexitás |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ALOHA** | [cite_start]**"Send at will"**<br>Ha van adat, azonnal küldi csatornafigyelés nélkül[cite: 302, 311]. | • Rendkívül egyszerű implementáció.<br>• Nulla vezérlési overhead.<br>• Alacsony terhelésnél minimális késleltetés. | [cite_start]• Magas forgalomnál rengeteg az ütközés[cite: 312, 316].<br>• Súlyos csomagvesztés.<br>• Alacsony maximális csatornakihasználtság (~18.4%). | **Rossz:** Az ütközések miatti folyamatos újraküldések és a tétlen hallgatózás gyorsan lemerítik a node-okat. | **Kiváló skálázhatóság, minimális komplexitás:** Nem igényel hálózati koordinációt vagy központi egységet. |
| **CSMA/CA** | [cite_start]**"Listen before talk"**<br>Adás előtt hallgatózik (Carrier Sense), foglalt csatornánál véletlenszerűt vár (Backoff)[cite: 290, 311]. | [cite_start]• Elkerüli a "vak" ütközéseket[cite: 308].<br>• Közepes terhelésig kiváló áteresztőképesség.<br>• Elosztott működés, nincs szükség központi órára. | [cite_start]• Kialakulhat a **rejtett állomás probléma**[cite: 299].<br>• A random backoff miatt változó és kiszámíthatatlan késleltetés (jitter). | [cite_start]**Közepes:** Jobb, mint az ALOHA, de a folyamatos csatornafigyelés (idle listening) és az ütközések még mindig sok energiát emésztenek fel[cite: 284]. | **Jó skálázhatóság, közepes komplexitás:** Új csomópontok dinamikusan, konfiguráció nélkül csatlakozhatnak a hálózathoz. |
| **TDMA** | [cite_start]**"Time Division"**<br>Az idő fix ablakokra (slot) van osztva, minden node-nak saját dedikált időszelete van[cite: 291]. | [cite_start]• **Teljesen ütközésmentes** működés[cite: 284].<br>• Nincs szükség csatornafigyelésre.<br>• Garantált sávszélesség és determinisztikus késleltetés. | [cite_start]• Szigorú, folyamatos **időszinkronizációt igényel**[cite: 438, 449].<br>• Pazarolja a slotot, ha a node-nak épp nincs adata.<br>• Nehézkes dinamikus topológiáknál. | **Kiváló:** Mivel a slotok fixek, a node pontosan tudja, mikor kell ébren lennie. [cite_start]A ciklus többi részében mély SLEEP módban maradhat (nincs idle listening)[cite: 241, 294]. | **Gyenge skálázhatóság, magas komplexitás:** Új node felvételekor a teljes menetrendet újra kell osztani. [cite_start]A szinkronizációs overhead jelentős[cite: 438]. |

 ### 18. Prompt - Negyedik hét

**Prompt (röviden):**

 Át tudod te is nbézni a kódot hogy megfelel e ezeknek a kritériumoknak?

Tipikus hibák és gyors ellenőrzések
• Carrier sense fogalma elnagyolva: definiáld, mit jelent a szimulátorban (csatorna foglalt? küszöb?).
• Backoff random nélkül vagy seed nélkül.
• Ütközés definíciója pontatlan (időben átfedő adások).

Heti leadandó / DoD
• mac modul v1: ALOHA + CSMA backoff implementáció.
• Ütközés teszt + seed dokumentálás.

 **MI válasz lényege:**

 Checklist a megadott pontok ellenörzéséről és hogy mennyire teljeasítik a feltételt, test_mac.py javítási javaslatok

 ### 19. Prompt - Ötödik hét

**Prompt (röviden):**

 Implementálj topológia generátort: random uniform, grid, és egy egyszerű cluster modell. Adj seedet és paramétereket.
 Adj ötleteket connectivity tesztekre: van-e út a sinkhez? hány komponens? átlagos degree?
 A generálás során vedd figyelembe a következő szempontokat és lehetséges hibákat is.
 Tipikus hibák és gyors ellenőrzések
• A random deployment seed nélküli.
• Hatótáv alapú link: egységek és távolságszámítás hibás.
• A vizualizáció nem tartalmaz tengelyt/scale-t/legend-et.
Szempontok amik elvártak
• topology modul: legalább 2 deployment stratégia + neighbor graph.
• Összefüggőség teszt + 1 ábra seed paraméterekkel.

 **MI válasz lényege:**

 A generátor osztályunk rögtön a numpy.random.default_rng(seed) inicializálásával fog kezdeni
 Szigorúan az Euklideszi távolságképletet ($d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$) fogjuk használni, ügyelve arra, hogy minden méterben (m) legyen megadva.
 models/topology.py alapkódja, és ajánlások tesztelésre

   **Döntésem / módosításaim:**
  
  Kódok átolvasása és tisztogatása pár helyen. Tesztötletek átnézése a kód alapján.

 ### 20. Prompt - Ötödik hét

**Prompt (röviden):**

El tudod készíteni a test/test_topology.py fájlt az autómatikus tesztelés megoldásához amivel teszteljük az olyanokat mint hogy van e útvonal a sinkhez. És meg tudod csinálni a NetworkX vizualizációt amit ábrába lehet exportálni?

 **MI válasz lényege:**

 test/test_topology.py a networkx beépített gráf-algoritmusait használja fel, hogy ellenőrizze az összefüggőséget és a Sink elérhetőségét.
 experiments/run_topology.py alapkódjának legenerálása 
 
   **Döntésem / módosításaim:**

  Kódok átnézése és felmerülő hibák kijavítása

   ### 21. Prompt - Ötödik hét

**Prompt (röviden):**

 Át tudod nézni a következő kódokat, hogy megfelelnek e a meghatározott szempontoknak?

 Tipikus hibák és gyors ellenőrzések
• A random deployment seed nélküli.
• Hatótáv alapú link: egységek és távolságszámítás hibás.
• A vizualizáció nem tartalmaz tengelyt/scale-t/legend-et.

Szempontok amik elvártak
• topology modul: legalább 2 deployment stratégia + neighbor graph.
• Összefüggőség teszt + 1 ábra seed paraméterekkel.

**Kontextus:**
experiments/run_topology.py, test/test_topology.py, models/topology.py módosított fájlai

 **MI válasz lényege:**

 Checklist a szempontokról és rövid összefoglaló hogy a kódok amiket küldtem valóban megvalósítjájk e azokat.




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

"Természetesen! Ez egy nagyon jó gyakorlaSt, hiszen a szimulátorokban (és a tesztekben) a "black box" (fekete doboz) szerű működés helyett mindig látnunk kell a pontos matematikát.
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

### 22. Prompt - Hatodik hét

**Prompt (röviden):**

Implementálj flooding routingot (TTL-lel) és egy sink-fát BFS alapján. Milyen adatstruktúrákat
használjak?

 **MI válasz lényege:**

Flooding vs. Sink-fa összefoglalása, adatstroktúrá közötti különbségek összefoglalása.
models/routing.py alapkódjának legenerálása.

**Döntésem / módosításaim:**

A generált kódok alapvető átnézése, tisztítása.

### 23. Prompt - Hatodik hét

**Prompt (röviden):**

Milyen módszert ajánlasz a kötés kialakításához ami a szimulátor motorját köti össze az összehasonlító kísérlethez?

 **MI válasz lényege:**

A legjobb és legszabványosabb módszer a kötések kialakítására az Ágens-alapú (Node-centric) csomagolás...
run_routing_compare.py létrehoására adott példakódok.

**Döntésem / módosításaim:**

run_routing_compare.py összerakása a példakódok alapján.

### 24. Prompt - Hatodik hét


**Prompt (röviden):**
Írj egy ETX-szerű metrikát PRR alapján, és hogyan válasszak szülőt? 

 **MI válasz lényege:**

A probléma a BFS-sel, és az ETX megoldás összefoglalása képletekkel. 
Hogyan válasszunk szülőt? Nem a legkevesebb ugrást keressük, hanem azt az utat a Sink-ig, ahol az ETX értékek összege a legkisebb. Az ETX inkább választ két rövid, tökéletes ugrást (költség = 1 + 1 = 2), mint egyetlen hosszú, bizonytalan ugrást (költség = 4). Ezt a klasszikus Dijkstra algoritmussal fogjuk megoldani a networkx segítségével!

EtxTreeRouting példakódok.

**Döntésem / módosításaim:**

A példakódok alapján összeállítottam a EtxTreeRouting osztályt a routing.py fájlba.

### 25. Prompt - Hatodik hét

**Prompt (röviden):**
 Megnéztem a kiemelt hibákat amiket ehhez a heti leckéhez ad esetleg ezekből lehetne csinálni egy teszt fájt ami ellenőrzi hogy ő ne legyen a kódban hasonló előfordulása.
Hibák
• Flooding végtelen ciklus (nincs TTL/seen cache).
....

**Cél:**

A szilabuszban jelzett típus-hibák elkerülésére TDD megközelítést alkalmaztam. Írtam egy test_routing.py-t, ami automatizáltan ellenőrzi a flooding végtelen ciklusának elkerülését, bizonyítja a fa-routing statikus mivoltát , és validálja a fair összehasonlításhoz szükséges topológiai determinizmust."

 **MI válasz lényege:**

Három ajánlott lehetséges khiba kiemelése lés azoknak a célzott tesztelésére példakódok.

**Döntésem / módosításaim:**

test/test_routing.py összeállítása a pélákból

### 26. Prompt - Hetedik hét

**Prompt (röviden):**

Eddig a csomagjainkat csak "vakul" kiküldtük a rádióba. Ha a csatorna zajos volt, vagy a távolság miatt alacsony volt a PRR, a csomag egyszerűen elveszett a levegőben. Ennek a problémának a megoldására tudsz kgenerálni egy megbízhatóságért felelős réteget ARQ mechanizmussal.

 **MI válasz lényege:**

models/reliability.py alakódja

**Döntésem / módosításaim:**

Kód átnézése és tisztítása

### 27. Prompt - Hetedik hét

**Prompt (röviden):**

Milyen eseményeket ütemezzek (timeout)? Tervezd meg a paraméter sweep-et retry_limit és backoff tartományokra. Milyen grafikonokat rajzoljak? Generálj teszteket amik a megbízhatóságot ellenőrzik: Ha megjön az ACK a timeout elött ne legyen vújraküldés, és hogy mi van ha sosem jön meg az ACK

 **MI válasz lényege:**

Milyen eseményeket ütemezzek (timeout)? összefoglalása, test/test_reliability.py, experiments/run_reliability.py alapkódok generálása, a grafikonon várt eredmények leírása.

**Döntésem / módosításaim:**

Tesztek és experiment kódok átnézése és letisztítása, futtatása, a futás során fellépő hibák kijavítása.


### 27. Prompt - Hetedik hét

**Prompt (röviden):**

Át tudod nézni a következő kódokat hogy megfelelnek e a megadott szempontoknak és nem jelenik meg bennük a sűrűn előforduló hibák egyike sem?
ipikus hibák és gyors ellenőrzések
• Timeout túl kicsi/nagy: irreális viselkedés.
• ACK-ot ugyanúgy kezeled, mint data packet-et (méret, energia) - legyen dokumentálva.
• A PDR javul, de nem méred az energia többletet.
Heti leadandó / DoD
• reliability: ACK + retry/backoff implementálva.
• Egy kísérlet: PDR vs energia görbe különböző retry limitekkel.

**Kontextus:**

models/reliability.py, test/test_reliability.py, experiments/run_reliability.py

 **MI válasz lényege:**

Checklist a megadott szempontokról és hogy megfelelnek e az megadott fájlok.

**Döntésem / módosításaim:**

Egyszerűsítettem: Az ACK csomagok visszaküldésének extra energia- és időköltségét (mivel azok mérete elhanyagolhatóan kicsi az adatcsomagokhoz képest) a jelenlegi ARQ szimulációban nem integráltam a fogyasztási modellbe.

### 28. Prompt - Nyolcadik hét

**Prompt (röviden):**

Tudsz implementálni egy egyszerű drift modellt ahol mindegyik node órája ppm eléréssel fut? hogyan számoljam a driftet események között? Figyelj a következő szempontokra és hibákra hogy a kódban ne legyen benne a hiba és megfeleljen a szempontoknak?

Tipikus hibák és gyors ellenőrzések
• Drift képlet rossz skálázással (ppm → 1e-6).
• Trilateráció numerikailag instabil, rossz anchor geometria esetén.
• RSSI→distance inverz túl naiv, nincs noise model.

Heti leadandó / DoD
• sync_localization modul: drift modell + trilateráció.
• Unit teszt: ismert pozíciók esetén kis hiba.

 **MI válasz lényege:**

Óra-drift és Lokalizáció összefoglalása, models/sync_localization.py, test_sync_localization.py generálása

**Döntésem / módosításaim:**

A szilabusz által opcionálisan kért ábra arról szól, hogy ha az RSSI értékeket $N(0, \sigma^2)$ árnyékolási zajjal (shadowing) terheljük, az exponenciális távolság-inverz miatt a távolságbecslés hibája aszimmetrikusan elszáll. Ha az RSSI jel 3 dB-t esik a zaj miatt, az algoritmus azt hiszi, a szenzor sokkal távolabb van, mint a valóságban, és a Least Squares metszéspont elcsúszik az eredeti helyéről.

### 29. Prompt - Nyolcadik hét

**Prompt (röviden):**

Adj alternatív lokalizációs megközelítéseket és mikor nem működik az RSSI?

 **MI válasz lényege:**

Az RSSI (Received Signal Strength Indicator) a legolcsóbb módszer, mert minden rádió chip alapból méri, de a legpontatlanabb is. A következő esetekben drasztikusan elcsúszik a távolságbecslés:

    Többutas terjedés (Multipath Fading):...

Ha az RSSI nem elég jó (pl. centiméteres pontosság kell), az alábbiakat használják a WSN és IoT világában:

    TOA (Time of Arrival):...

### 30. Prompt - Nyolcadik hét

**Prompt (röviden):**

tudsz generálni egy kísérlet fájt a mély a kritériumokban szereplő ábrát legenerálja ami hol a lokalizáció hiba a zaj függvényében van?

 **MI válasz lényege:**

run_localization.py alapkódjának legenerálása

**Döntésem / módosításaim:**

A run_localization.py kód átnézése letisztítása és tesztelése

### 31. Prompt - Nyolcadik hét

**Prompt (röviden):**

át tudod nézni a következő fájlokat hogy biztosan megfelelnek-e a nyolcadik fejezetben említett kritériumoknak illetve hogy a hibák nem fordulnak elő bennük?

Tipikus hibák és gyors ellenőrzések

• Drift képlet rossz skálázással (ppm → 1e-6).
• Trilateráció numerikailag instabil, rossz anchor geometria esetén.
• RSSI→distance inverz túl naiv, nincs noise model.

Heti leadandó / DoD

• sync_localization modul: drift modell + trilateráció.
• Unit teszt: ismert pozíciók esetén kis hiba.
• Rövid jegyzet/ábra: lokalizáció hiba a zaj függvényében (opcionális).

**Kontextus**

models/sync_localization.py, test_sync_localization.py, experiments/run_localization.py

 **MI válasz lényege:**

 Checklist a megadott szempontokból és hogy megfelel e a kód az adott pontnak.

### 32. Prompt - Kilencedik hét

**Prompt (röviden):**

Készíts két aggregációs stratégiát: (1) nyers adat továbbítás, (2) fa menti átlag + delta kódolás. Milyen interfészt használjak?

 **MI válasz lényege:**

models/aggregation.py generálása

**Döntésem / módosításaim:**

A kódodt átnéztem és letisztítottam

### 33. Prompt - Kilencedik hét

**Prompt (röviden):**

Tervezd meg a kísérletet: hogyan mérjem a kommunikáció csökkenést és az aggregáció okozta hibát (pl. MSE)? Javasolj riport struktúrát 1 oldalas kísérleti összefoglalóhoz.

 **MI válasz lényege:**

A Kísérlet Megtervezése: Kommunikáció vs. Hiba (MSE)

Hogyan mérjük?

    A 'Ground Truth' (Valós adat) generálása: Szimulálunk egy lassan változó fizikai jelenséget, például a hőmérsékletet. Erre a legjobb egy szinuszgörbe, amire egy kis véletlen zajt teszünk (így realisztikus). Ezt hívjuk valós adatnak.

    Kommunikációs költség (TX Count):...

experiments/run_aggregation.py alapkódjának a legenerálása

week09_aggregation.md riporthoz tartalmi pontok ajánlása, alap szerkezet legenerálása

**Döntésem / módosításaim:**

experiments/run_aggregation.py átnézése, futtatása, week09_aggregation.md összeállítása az ajánlott pontok alapján

### 34. Prompt - Kilencedik hét

**Prompt (röviden):**

Tudsz generálni egy tesztfilet ami a következő gyakran előfotrduló hibákra ellenőrzi a korábban létrehozott kódot?

Tipikus hibák és gyors ellenőrzések
• Nem definiálod, mi a 'hiba' (ground truth).
• Aggregációs függvény nem asszociatív/kommutatív → függ a fa struktúrától (dokumentáld).
• Delta-kódolásnál nincs reset / overflow kezelve (ha modellezed).

 **MI válasz lényege:**

test/test_aggregation.py alapkódjának létrehozása

**Döntésem / módosításaim:**

test/test_aggregation.py kóddjának átnézése, tisztítása, hibák javítása

### 35. Prompt - Tizedik hét

**Prompt (röviden):**

Generálj egy threat checklistet a wsnsim projektre: asset, attacker, attack surface, mitigations. Adj ötletet: hogyan modellezzem 'security overhead'-ként az extra byte-okat és extra CPU időt az energia modulban?

 **MI válasz lényege:**

WSN Threat Checklist (Fenyegetési Modell) a wsnsim-hez (asset, attacker, attack surface, mitigations)
A szilabusz egy nagyon fontos mérnöki kérdést tesz fel: hogyan jelenítsük meg ezt a szimulátorban? Két fő költsége van a biztonságnak: Extra Byte-ok (Hálózati / MAC terhelés), Extra CPU idő (Feldolgozási késleltetés és fogyasztás)

### 36. Prompt - Tizedik hét

**Prompt (röviden):**

Implementálj egy Replay védelmet, írj abuse-case tesztet replay attack szimulálására és védelemre (nonce/seq).
Készíts el egy models/security.py modult a szekvenciaszámos szűrővel és a CPU overhead szimulátorával, valamint hozzá a tesztfájlt 

**MI válasz lényege:**

models/security.py, test/test_security.py alapkódjának a legenerálása

**Döntésem / módosításaim:**

A generált kódok átnézése, tisztítása futtatása és a felmerülő hibák javítása.

### 37. Prompt - Tizedik hét

**Prompt (röviden):**

Tudsz generálni egy tesztet a test/test_security.py-hoz ami behúzza az EnergyModel-t is, és számszerűen bebizonyítja, hogy a támadás alatt a védelem nélküli node pillanatok alatt lemerül, míg a védett node megmenekül.

**MI válasz lényege:**

test_negative_case_and_energy_overhead() függvény kódja

**Döntésem / módosításaim:**

A test_negative_case_and_energy_overhead() tuttatása során fellépő hibák javítása, biztosítása annak hogy az idő nem folyhat visszafelé

### 38. Prompt - Tizenegyedik hét

**Prompt (röviden):**

Adj ötleteket idősor feature-ökre anomália detektáláshoz (statisztikai + egyszerű ML). Implementálj egy baseline detektort (pl. z-score, EWMA) és definiálj metrikákat (FP/FN, commsaved).

**MI válasz lényege:**

Ötletek idősoros (Time-Series) Feature-ökre Edge eszközökön, Baseline Detektor Implementációja models/edge_ai.py kóddal

**Döntésem / módosításaim:**

Rektam a hibák ellen védelmet mint a Ground truth a generátorban, és a paraméterek a konstruktorban

### 39. Prompt - Tizenegyedik hét

**Prompt (röviden):**

Hogyan logoljam a hiperparamétereket és seed-et a detektor kísérleteknél? Meg tudod írni ezt a kísérletet ami megméri és ábrázolja, hogy a threshold paraméter változtatásával hogyan mozog a Communication Saved (Spórolás) vs. a False Positive (Fals Riasztás) aránya. 

**MI válasz lényege:**

A legprofibb mérnöki megoldás (amit a szilabusz is javasol ), ha minden kísérlet futtatásakor automatikusan kigenerálsz egy config_dump.json fájlt az eredmények és az ábrák mellé...
experiments/run_edge_ai.py alaprogramjának a legenerálása

**Döntésem / módosításaim:**

Kód átnézése és letisztítása, kód futatása és eredmények ellenőrzése.

### 40. Prompt - Tizenegyedik hét

**Prompt (röviden):**

Át tudod nmézni a következő fájlokat hogy a tartalmuk eleget tesz e a megemlyített szempontoknak?
Tipikus hibák és gyors ellenőrzések
• Nincs ground truth → nem tudod FP/FN-t mérni.
• A kommunikáció spórolás definíciója nincs rögzítve (byte? packet? radio on-time?).
• A detektor paraméterei nincsenek a configban → irreprodukálható.
Heti leadandó / DoD
• edge_ai modul: jel generátor + detektor + mérés.
• Egy grafikon: communication saved vs false positive (vagy ROC-szerű).

**Kontextus:**

experiments/run_edge_ai.py, models/edge_ai.py

**MI válasz lényege:**

Checklist a felsorolt szempontokról és hogy megtalálta e őket a fájlokban

### 41. Prompt - Tizenkettedik hét

**Prompt (röviden):**

Implementálj FedAvg szimulációt: K node lokális update, server aggregál. Milyen adatstruktúrák
legyenek a modellekhez?

**Cél:**

A cél a kommunikációs trade-off vizsgálata a diszkrét eseményű szimulátorban, nem pedig a mesterséges intelligencia pontosságának maximalizálása

**MI válasz lényege:**

Milyen adatstruktúrák legyenek a modellekhez?
Mivel a kommunikációs költséget (hány bájtot küldünk a rádión) akarjuk mérni, a modellünket úgy kell reprezentálnunk, hogy egyértelmű legyen a mérete...

models/federated.py alapkódjának a legenerálása

**Döntésem / módosításaim:**

models/federated.py kódjának átnézése, letisztítása

### 42. Prompt - Tizenkettedik hét

**Prompt (röviden):**

Írj egy run_federated.py kísérletet ami teszteli, hogy mi történik he ritkábban, mondjuk csak minden 5. lépésben kommunikálnak a node-ok a szerverrel majd kirajzolja az eredményeket egy ábrával.

**MI válasz lényege:**

experiments/run_federated.py generálása

**Döntésem / módosításaim:**

experiments/run_federated.py átolvasása, kódok letisztítása

### 43. Prompt - Tizenkettedik hét

**Prompt (röviden):**

Adj kommunikációs költség modellt: bytes per round, rounds; hasonlítsd össze centralizált tanítással.

**MI válasz lényege:**

Federated Learning (FL) Kommunikációs Költségmodell és Összehasonlítás a Centralizált Tanítással

### 44. Prompt - Tizenkettedik hét

**Prompt (röviden):**

Nézd át a kódokat hogy a következő szempontoknak megfelelnek e.

Tipikus hibák és gyors ellenőrzések
• Túl bonyolult ML modellt választasz - a cél a kommunikációs trade-off, nem a SOTA pontosság.
• Nem rögzíted a modell méretet (paraméterek száma) → nem mérhető a költség.
• A 'konvergencia' metrika nincs definiálva (loss? accuracy? proxy?).
Heti leadandó / DoD
• federated modul: FedAvg baseline + cost model.
• Egy ábra: update periódus vs kommunikációs költség (és opcionálisan proxy accuracy)

**Kontextus:**

experiments/run_federated.py, models/federated.py

**MI válasz lényege:**

Checklist a szempontokról és hogy mindegyik megtalálható a model szerint az elkészült fájlokban

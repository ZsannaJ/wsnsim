**1. Prompt - Első hét**

Tervezd meg a wsnsim minimális architektúráját modulokra bontva (sim, models, scenarios, metrics).
Adj 5-10 függvény-szignatúrát.
Írj egy minimal event scheduler-t heapq-val: schedule(time, callback), run(until). Adj hozzá unit
teszteket determinisztikus sorrendre. 

**2. Prompt - Első hét**

 (.venv) PS C:\Users\mester\Desktop\wsnsim> & c:\Users\mester\Desktop\wsnsim\.venv\Scripts\python.exe c:/Users/mester/Desktop/wsnsim/test/test_scheduler.py
Traceback (most recent call last):
  File "c:\Users\mester\Desktop\wsnsim\test\test_scheduler.py", line 3, in <module>
    from sim.scheduler import Scheduler
ModuleNotFoundError: No module named 'sim'
(.venv) PS C:\Users\mester\Desktop\wsnsim>  

A hibán kívül át tudod nézni, hogy hol lehet nondeterminism, hol kell seed? 

**3. Prompt - Első hét**

Adj logolást a tesztekhez hogy lehessen követni a lefutásukat.
(python -m pytest test/test_scheduler.py --log-cli-level=INFO)

**4. Prompt - Első hét**

Csinálj nekem egy helo simulation példát mert jelenleg ez nincs megvalósulva a kódomban. Ezen kívül a logger modul pontosan működik, ezt hozzáadod ha még nincs? 

**5. Prompt - Második hét**  

Implementáld a log-distance + log-normal shadowing modellt Pythonban: pl(d), rssi(d). Javasolj paramétereket (n, sigma). Majd adj unit teszt ötleteket a csatorna modellre: monotonicitás, határértékek (d→d0), seed hatás. 

**6. Prompt - Második hét**  

Meg tudod csinálni a határérték, monotonicitás teszteket valamint a reprodukálhatóságra illetve véletlenszerűségre vonatkozó teszteket. Meg tudod adni a futtatási kódot. 

**7. Prompt - Második hét**  

Készíts egy kísérletet: PRR(d) görbe több sigma értékre; hogyan ábrázoljam?


Ezekből mindegyik teljesül, át tudod nézni te is gyorsan a kódot?

**8. Prompt - Második hét**

• channel modul: PRR(distance) + shadowing opció. ✅
• Egy ábra: PRR vs távolság (legalább 2 paraméter beállítással). ✅
• Validálás: kézi számítás 2 ponton dokumentálva ❌

**9. Prompt - Második hét**

Be tudsz tenni a chaneles függvényhívásokhoz egy alap kikommentelt számítás részt ahova a kézzel számolt eredményeket is majd be tudom helyettesíteni? Olyat hogy matematikai művelet = matematikai művelet behelyettesített számokkal eredmény. Ki tudod te is számolni hogy ellenőrizzem az én eredményemet a tiéddel?

**10. Prompt - Harmadik hét**

 Tervezd meg az energy state machine-t (enum) és az energia integrálását események alapján. Adj API-t és dataclass struktúrát. Írj teszteket: negatív energia ne legyen; duty-cycle mellett az átlagos fogyasztás kövesse az elvárt
trendet. 

**11. Prompt - Harmadik hét**

Tudsz adni egy a korábbihoz hasonló experiment filet ami Egy mini-kísérlet: duty cycle vs becsült üzemidő (grafikon) hoz létre? 

**12. Prompt - Harmadik hét**

 Adj egy 'sanity check' checklistet az energia modellhez. Sanity check: 'negatív energia' guard + teszt. 

 **13. Prompt - Harmadik hét**

  Át tudod te is nézni a kódot hogy biztosan minden benne legyen a következők közül?

Tipikus hibák és gyors ellenőrzések

• A teljesítmény (W) és energia (J) keverése.

• Nem veszed figyelembe az állapotváltások (switching) költségét (ha modellezed, dokumentáld).

• A rádió RX/TX időtartam nincs konzisztensen számolva (packet duration).

Kritériumok

• energy modul: állapotgép + fogyasztás integrálása idő szerint.

• Egy mini-kísérlet: duty cycle vs becsült üzemidő (grafikon).

• Sanity check: 'negatív energia' guard + teszt. 

 **14. Prompt - Harmadik hét**

Modellezd le az állapotváltozások energiaigényét. Valamint nem lehetne a run_energybe most megcsinálni a konzisztens számolást, le tudod generálni?

 **15. Prompt - Harmadik hét**

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
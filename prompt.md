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


Výsledky voleb 2017 – okresy a obce

Tento projekt slouží k stahování výsledků voleb do Poslanecké sněmovny 2017 pro zvolený okres a jeho obce přímo z webu volby.cz.
Výstupem je CSV soubor, který lze otevřít v Excelu nebo jiném tabulkovém editoru.

---

Funkce:

* Extrahuje všechny obce v zadaném okrese.
* Stahuje tyto údaje pro každou obec:

  * kód obce
  * název obce
  * voliči v seznamu
  * vydané obálky
  * platné hlasy
  * počet hlasů pro jednotlivé kandidující strany
* CSV je ve formátu kompatibilním s Microsoft Excel (středník ; jako oddělovač, UTF-8 s BOM).
* Přehled prvních 10 obcí se vypíše do konzole v tabulce pro rychlou kontrolu.
---
Doporučuji spustit v CMD, nikde jinde mi to nefungovalo.
---
Stáhni všechny 3 soubory main.py, requirements.txt a readme.txt do složky odkud chceš spouštět virtuální prostředí a kam chceš vytvořit csv.
---
Víš kam jsi si uložil soubory? ----> ano tak pak v cmd otevři toto ----> příklad cesty k uloženým souborům 

cd C:\Users\vojta\Desktop\Python
----
Nevíš kam jsi uložil soubory? ----> zkus to znovu a lépe!
---

Instalace:

Aktivace virtuálního prostředí na windows

1. zadej tento příkaz: venv\Scripts\activate.bat  

2. Instalace potřebných knihoven:
   pip install -r requirements.txt

---
Spusť tento příkaz:

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107" vysledky_mb.csv

* Po spuštění se do konzole vypíše ukázka prvních 10 obcí s hlavními údaji.
* CSV obsahuje kód obce, název obce, voliči, obálky, platné hlasy a hlasy pro strany.
---
Pro ukončení virtuálního prostředí napiš

deactivate
---
Autor:
Vojtěch Pažout
vojtapazout@gmail.com
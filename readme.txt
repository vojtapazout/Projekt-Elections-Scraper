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
Pokud chceš zvolit jiný okres postupuj podle tohoto aby jsi měl jednoduchý příkaz pro spuštění:

Použití: python main.py <URL_okresu> <nazev_vystupniho_csv>

<URL_okresu> – odkaz na web volby.cz pro konkrétní okres

<nazev_vystupniho_csv> – jméno souboru pro výsledky

Spusť příkaz, který bude vypadat takto:

1. verze pro Mladou Boleslav:

python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2107" vysledky_mb.csv

2. verze pro Benešov
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv

* Po spuštění se do konzole vypíše ukázka prvních 10 obcí s hlavními údaji.
* CSV obsahuje kód obce, název obce, voliči, obálky, platné hlasy a hlasy pro strany.

příklad:
535427;Bakov nad Jizerou;3922;2551;2539;864;285;295;252;204;179;153;113;42;36;27;32;18;4;4;8;3;6;1;2;2;1;3;1;2;2
535443;Bělá pod Bezdězem;3805;2219;2204;802;215;253;218;214;107;153;61;38;33;28;33;9;8;1;3;2;7;4;4;4;1;0;3;3;0
535451;Benátky nad Jizerou;5596;3269;3254;1041;533;306;323;225;176;198;151;77;58;58;24;26;10;9;6;12;6;3;4;1;3;2;1;0;1

---
Pro ukončení virtuálního prostředí napiš:

deactivate
---
Autor:
Vojtěch Pažout
vojtapazout@gmail.com
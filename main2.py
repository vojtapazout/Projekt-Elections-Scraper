import sys
import csv
from collections import defaultdict
from typing import List, Tuple, Dict, Optional

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def nacti_html(url: str) -> str:
    """Načte HTML obsah stránky a vrátí jej jako text."""
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text

def ziskej_obce(soup: BeautifulSoup) -> List[Tuple[str, str, str]]:
    """Vrátí seznam obcí jako (kód, název, href)."""
    obce = []
    for link in soup.select("td.cislo a"):
        kod = link.text.strip()
        href = BASE_URL + link["href"]
        obec_td = link.find_parent("td").find_next_sibling("td")
        obec = obec_td.text.strip()
        obce.append((kod, obec, href))
    return obce

def zpracuj_obec(url_obce: str) -> Optional[Tuple[str, str, str, List[str], List[int]]]:
    """Načte data o obci: voliči, obálky, platné hlasy a hlasy stran."""
    html = nacti_html(url_obce)
    soup = BeautifulSoup(html, "html.parser")

    info_table = soup.find("table", {"class": "table"})
    if not info_table:
        return None

    td_values = [td.get_text(strip=True).replace("\xa0", "") for td in info_table.find_all("td")]
    volici = td_values[3] if len(td_values) > 3 else ""
    obalky = td_values[4] if len(td_values) > 4 else ""
    platne = td_values[7] if len(td_values) > 7 else ""

    tables = soup.find_all("table", {"class": "table"})
    strany, hlasy = [], []
    for tab in tables[1:]:
        for r in tab.find_all("tr")[2:]:
            tds = r.find_all("td")
            if len(tds) >= 3:
                jmeno = tds[1].get_text(strip=True)
                hlasu = tds[2].get_text(strip=True).replace("\xa0", "")
                if jmeno:
                    strany.append(jmeno)
                    hlasy.append(int(hlasu) if hlasu.isdigit() else 0)
    return volici, obalky, platne, strany, hlasy

def zpracuj_okres(url: str) -> Tuple[List[Dict], Dict[str, int]]:
    """Načte všechny obce v okrese a sečte hlasy stran."""
    html = nacti_html(url)
    soup = BeautifulSoup(html, "html.parser")
    obce = ziskej_obce(soup)

    vsechny_obce = []
    soucet_hlasu = defaultdict(int)

    for kod, obec, href in obce:
        print(f" Zpracovávám: {obec}")
        vysledky = zpracuj_obec(href)
        if not vysledky:
            continue
        volici, obalky, platne, strany, hlasy = vysledky
        zaznam = {
            "kód obce": kod,
            "název obce": obec,
            "voliči v seznamu": volici,
            "vydané obálky": obalky,
            "platné hlasy": platne
        }
        for s, h in zip(strany, hlasy):
            zaznam[s] = h
            soucet_hlasu[s] += h
        vsechny_obce.append(zaznam)
    return vsechny_obce, soucet_hlasu

def uloz_csv(vsechny_obce: List[Dict], soucet_hlasu: Dict[str, int], vystup: str):
    """Uloží výsledky do CSV souboru a vypíše ukázku."""
    serazene_strany = sorted(soucet_hlasu, key=lambda k: soucet_hlasu[k], reverse=True)
    sloupce = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + serazene_strany

    with open(vystup, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=sloupce, delimiter=';')
        writer.writeheader()
        for o in vsechny_obce:
            writer.writerow(o)

    tabulka = [[o["kód obce"], o["název obce"], o["voliči v seznamu"], o["vydané obálky"], o["platné hlasy"]]
               for o in vsechny_obce[:10]]
    print("\n Ukázka výsledků (prvních 10 obcí):")
    print(tabulate(tabulka, headers=["Kód", "Obec", "Voliči", "Obálky", "Platné hlasy"], tablefmt="grid"))

def main():
    if len(sys.argv) != 3:
        print("Použití: python main.py <url_okresu> <vystup.csv>")
        sys.exit(1)

    url = sys.argv[1]
    vystup = sys.argv[2]

    vsechny_obce, soucet_hlasu = zpracuj_okres(url)
    if not vsechny_obce:
        print(" Nebyla nalezena žádná data.")
        return
    uloz_csv(vsechny_obce, soucet_hlasu, vystup)
    print(f"\n Hotovo! Uloženo do CSV: {vystup}")

if __name__ == "__main__":
    main()

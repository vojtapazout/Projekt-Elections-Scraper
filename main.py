import sys
import csv
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from collections import defaultdict

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def nacti_html(url):
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text

def zpracuj_obec(url_obce):
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
    strany = []
    hlasy = []
    for tab in tables[1:]:
        rows = tab.find_all("tr")[2:]
        for r in rows:
            tds = r.find_all("td")
            if len(tds) >= 3:
                jmeno = tds[1].get_text(strip=True)
                hlasu = tds[2].get_text(strip=True).replace("\xa0", "")
                if jmeno:
                    strany.append(jmeno)
                    hlasy.append(int(hlasu) if hlasu.isdigit() else 0)

    return volici, obalky, platne, strany, hlasy

def main():
    if len(sys.argv) != 3:
        print("Použití: python main.py <url_okresu> <vystup.csv>")
        sys.exit(1)

    url = sys.argv[1]
    vystup = sys.argv[2]

    html = nacti_html(url)
    soup = BeautifulSoup(html, "html.parser")

    vsechny_obce = []
    soucet_hlasu = defaultdict(int)

    for link in soup.select("td.cislo a"):
        kod = link.text.strip()
        href = BASE_URL + link["href"]
        obec_td = link.find_parent("td").find_next_sibling("td")
        obec = obec_td.text.strip()

        print(f" Zpracovávám: {obec}")
        try:
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
        except Exception as e:
            print(f" Chyba u {obec}: {e}")

    if not vsechny_obce:
        print(" Nebyla nalezena žádná data.")
        return

    # Seřazení stran podle celkového počtu hlasů sestupně
    serazene_strany = sorted(soucet_hlasu, key=lambda k: soucet_hlasu[k], reverse=True)

    # pevný pořádek sloupců
    sloupce = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"] + serazene_strany

    # zápis do CSV s oddělovačem středník
    with open(vystup, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=sloupce, delimiter=';')
        writer.writeheader()
        for o in vsechny_obce:
            writer.writerow(o)

    # Přehled prvních 10 obcí
    tabulka = [
        [o["kód obce"], o["název obce"], o["voliči v seznamu"], o["vydané obálky"], o["platné hlasy"]]
        for o in vsechny_obce[:10]
    ]
    print("\n Ukázka výsledků (prvních 10 obcí):")
    print(tabulate(tabulka, headers=["Kód", "Obec", "Voliči", "Obálky", "Platné hlasy"], tablefmt="grid"))

    print(f"\n Hotovo! Uloženo do CSV: {vystup}")

if __name__ == "__main__":
    main()

import os
import csv
from .models import Kategoria, Pytanie, Odpowiedz
from .db import db

def pobierz_dane(plikcsv):
    """Funkcja zwraca tuplę zawierającą tuple z danymi z pliku csv."""
    dane = []
    if os.path.isfile(plikcsv):
        with open(plikcsv, newline='') as plikcsv:
            tresc = csv.reader(plikcsv, delimiter=';')
            for rekord in tresc:
                dane.append(tuple(rekord))
    else:
        print("Plik z danymi", plikcsv, "nie istnieje!")
    return tuple(dane)

def dodaj_pytania(dane):
    """Funkcja dodaje pytania i odpowiedzi przekazane w tupli do bazy."""
    print(dane)
    for pytanie, odpowiedzi, odpok, kategoria in dane:
        k = Kategoria(kategoria=kategoria)
        p = Pytanie(pytanie=pytanie, odpok=odpok, kategoria=k)
        for o in odpowiedzi.split(","):
            odp = Odpowiedz(odpowiedz=o.strip())
            p.odpowiedzi.append(odp)
        db.session.add(p)
        db.session.commit()
    print("Dodano przykładowe pytania")

import os
import csv
from peewee import SqliteDatabase, Model, BooleanField
from peewee import CharField, ForeignKeyField
from config import Config

# tworzymy instancję klasy Database do obsługi bazy
baza = SqliteDatabase(Config.DATABASE, pragmas={'foreign_keys': 1})


# klasa bazowa dla modeli
class Base(Model):
    class Meta:
        database = baza

class Kategoria(Base):
    nazwa = CharField()

    def __str__(self):
        return self.nazwa


class Pytanie(Base):
    tresc = CharField(unique=True)
    kategoria = ForeignKeyField(Kategoria, backref='pytania')

    def __str__(self):
        return self.tresc


class Odpowiedz(Base):
    tresc = CharField(unique=True)
    poprawna = BooleanField(default=False)
    pytanie = ForeignKeyField(
        Pytanie, backref='odpowiedzi', on_delete='CASCADE')

    def __str__(self):
        return self.tresc


# def init_app(plik_bazy):
#    baza.init(Config.DATABASE)

def init_db():
    baza.create_tables([Kategoria, Pytanie, Odpowiedz])  # tworzymy tabele

def pobierz_dane(plikcsv, delimiter):
    """Funkcja zwraca listę słowników z danymi z pliku csv."""
    dane= []
    if os.path.isfile(plikcsv):
        with open(plikcsv, newline='') as plikcsv:
            dane = list(csv.DictReader(plikcsv, delimiter=delimiter))
    else:
        print(f'Plik z danymi {plikcsv} nie istnieje!')
    return dane

def dodaj_dane():
    dane = pobierz_dane('kategorie.csv', ';')
    for kategoria in dane:
        k = Kategoria(**kategoria)
        print(k)
        k.save(force_insert=True)
    dane = pobierz_dane('pytania.csv', ';')
    for pytanie in dane:
        print(pytanie['tresc'])
        p = Pytanie(tresc=pytanie['tresc'])
        k = Kategoria.select().where(Kategoria.id==pytanie['kategoria']).get()
        p.kategoria = k
        p.save(force_insert=True)
    dane = pobierz_dane('odpowiedzi.csv', ';')
    for odpowiedz in dane:
        o = Odpowiedz(**odpowiedz)
        print(o)
        o.save(force_insert=True)

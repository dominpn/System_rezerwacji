from pymongo import MongoClient
import random
import string

client = MongoClient()
db = client.uzytkownicy
kolekcja = db.loginy

def dodaj_klienta_mongo(ID, imie, nazwisko):
    if len(imie)>2 and len(nazwisko)>2:
        haslo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        uzytkownik = {"id": ID, "login": imie.lower() + "_" + nazwisko.lower(),
                  "haslo": haslo, "typ_uzytkownika": "klient"}
        kolekcja.insert(uzytkownik)
def usun_klienta_mongo(ID):
    try:
        kolekcja.delete_one({"id":ID})
    except:
        raise NameError("Nie ma takiego rekordu w bazie")

def zwroc_uzytkownika(login):
    try:
        uzytkownik = kolekcja.find_one({"login": login})
        return uzytkownik
    except:
        raise NameError("Nie ma takiego uzytkownika")
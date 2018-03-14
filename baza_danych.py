import pyodbc
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, func

Base = declarative_base()
engine = create_engine("mssql+pyodbc://dominik:dominik@DOMINIK-LAPTOP\SQLEXPRESS/System_rezerwacji?driver=SQL+Server+Native+Client+11.0")
metadata = MetaData(bind=engine)


class Klienci(Base):
    __table__ = Table('Klienci', metadata, autoload=True)

    @staticmethod
    def click(imie, nazwisko, email, karnet_data_rozpoczecia, karnet_data_zakonczenia):
        try:
            nowyKlient = Klienci(Imie = imie, Nazwisko = nazwisko,
                                 Adres_email = email, Karnet_data_rozpoczecia=karnet_data_rozpoczecia,
                                 Karnet_data_zakonczenia=karnet_data_zakonczenia)

            session = create_session(bind=engine)
            session.add(nowyKlient)
            session.commit()
            session.close()


        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise NameError(sqlstate)

    @staticmethod
    def click_procedure(imie, nazwisko, email, karnet_data_rozpoczecia, karnet_data_zakonczenia):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("dodaj_klienta ?, ?, ?, ?, ?", [imie, nazwisko, email,
                                                           karnet_data_rozpoczecia, karnet_data_zakonczenia])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000': #łapanie wyjątków z procedury oraz trigerów
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                raise NameError(mes[0])
            elif sqlstate == '23000': #łapanie błędów z warunków spójności
                raise NameError("Naruszono warunki spojnosci. \nAdres email musi byc w formie aaa@aaa.aaa, "
                                                "data w formacie YYYY.MM.DD, data zakonczenia pozniejsza od daty rozpoczecia")
    @staticmethod
    def readfromdatabase():
        session = create_session(bind=engine)
        testlist = session.query(Klienci).all();
        session.close()
        return testlist

    @staticmethod
    def zwroc_poID(ID_Klienta):
        session = create_session(bind=engine)
        q = session.query(Klienci).filter(Klienci.ID_Klienta == ID_Klienta)
        rekord = q.one()
        return rekord
    @staticmethod
    def usun(ID_Klienta):
        session = create_session(bind=engine)
        session.query(Klienci).filter(Klienci.ID_Klienta==ID_Klienta).delete()
        session.close()

    @staticmethod
    def usun_procedura(ID_Klienta):
        cursor = engine.raw_connection().cursor()
        cursor.execute("usun_klienta ?", [ID_Klienta])
        cursor.commit()
    @staticmethod
    def modyfikuj(ID_Klienta, Imie, Nazwisko, Email, Data_rozpoczecia, Data_zakonczenia):
        try:
            session = create_session(bind=engine)
            q = session.query(Klienci)
            q = q.filter(Klienci.ID_Klienta == ID_Klienta)
            record = q.one()
            if len(Imie)>0:
                record.Imie = Imie
            if len(Nazwisko)>0:
                record.Nazwisko = Nazwisko
            if len(Email)>0:
                record.Adres_email = Email
            if len(Data_rozpoczecia)>0:
                record.Karnet_data_rozpoczecia = Data_rozpoczecia
            if len(Data_zakonczenia)>0:
                record.Karnet_data_zakonczenia = Data_zakonczenia
            session.flush()
            session.close()

        except:
            raise NameError("Naruszono warunki spojnosci lub nie ma takiego klienta. \n"
                                                "Adres email musi byc w formie aaa@aaa.aaa, data w formacie YYYY.MM.DD, data zakonczenia pozniejsza "
                                    "od daty rozpoczecia")

    @staticmethod
    def modyfikuj_procedura(ID_Klienta, Imie, Nazwisko, Email, Data_rozpoczecia, Data_zakonczenia):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("modyfikuj_klienta ?, ?, ?, ?, ?, ?",
                        [ID_Klienta ,Imie, Nazwisko, Email,
                         Data_rozpoczecia, Data_zakonczenia])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                raise NameError(mes[0])
            elif sqlstate == '23000':
                raise NameError("Naruszono warunki spojnosci. \nAdres email musi byc w formie aaa@aaa.aaa, "
                                                "data w formacie YYYY.MM.DD, data zakonczenia pozniejsza od daty rozpoczecia")

    @staticmethod
    def zwroc_ID(Imie, Naziwsko, Email, Data_rozpoczecia, Data_zakonczenia):
        session = create_session(bind=engine)
        q = session.query(Klienci).filter(Klienci.Imie == Imie, Klienci.Nazwisko == Naziwsko, Klienci.Adres_email == Email, Klienci.Karnet_data_rozpoczecia==Data_rozpoczecia, Klienci.Karnet_data_zakonczenia==Data_zakonczenia)
        rekord = q.one()
        return rekord.ID_Klienta



class Trenerzy(Base):
    __table__ = Table('Trenerzy', metadata, autoload=True)

    @staticmethod
    def dodaj(imie, nazwisko, specjalnosc):
        try:
            nowyTrener = Trenerzy(Imie=imie, Nazwisko=nazwisko,
                                 Specjalnosc=specjalnosc)

            session = create_session(bind=engine)
            session.add(nowyTrener)
            session.flush()
            session.close()


        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise NameError(sqlstate)

    @staticmethod
    def dodaj_procedura(imie, nazwisko, specjalnosc):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("dodaj_trenera ?, ?, ?", [imie, nazwisko, specjalnosc])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':  # łapanie wyjątków z procedury oraz trigerów
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                return
                raise NameError(mes[0])
            elif sqlstate == '23000':  # łapanie błędów z warunków spójności
                raise NameError("Naruszono warunki spojnosci.")

    @staticmethod
    def odczyt():
        session = create_session(bind=engine)
        lista = session.query(Trenerzy).all();
        session.close()
        return lista

    @staticmethod
    def zwroc_poID(ID_Trenera):
        session = create_session(bind=engine)
        q = session.query(Trenerzy).filter(Trenerzy.ID_Trenera == ID_Trenera)
        rekord = q.one()
        return rekord

    @staticmethod
    def usun(ID_Trenera):
        session = create_session(bind=engine)
        session.query(Trenerzy).filter(Trenerzy.ID_Trenera == ID_Trenera).delete()
        session.close()

    def usun_procedura(ID_Trenera):
        cursor = engine.raw_connection().cursor()
        cursor.execute("usun_trenera ?", [ID_Trenera])
        cursor.commit()

    @staticmethod
    def modyfikuj(ID_Trenera, Imie, Nazwisko, Specjalnosc):
        try:
            session = create_session(bind=engine)
            q = session.query(Trenerzy)
            q = q.filter(Trenerzy.ID_Trenera == ID_Trenera)
            record = q.one()
            if len(Imie) > 0:
                record.Imie = Imie
            if len(Nazwisko) > 0:
                record.Nazwisko = Nazwisko
            if len(Specjalnosc) > 0:
                record.Specjalnosc = Specjalnosc
            session.flush()
            session.close()

        except:
            raise NameError("Naruszono warunki spojnosci lub nie ma takiego trenera.")

    @staticmethod
    def modyfikuj_procedura(ID_Trenera, Imie, Nazwisko, Specjalnosc):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("modyfikuj_trenera, ?, ?, ?, ?",
                           [ID_Trenera, Imie, Nazwisko, Specjalnosc])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                raise NameError(mes[0])
            elif sqlstate == '23000':
                raise NameError("Naruszono warunki spojnosci.")

class Sala(Base):
    __table__ = Table('Sala', metadata, autoload=True)

    @staticmethod
    def dodaj(pojemnosc, pietro):
        try:
            nowaSala = Sala(Pojemnosc=pojemnosc, Pietro=pietro)

            session = create_session(bind=engine)
            session.add(nowaSala)
            session.flush()
            session.close()


        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise NameError(sqlstate)

    @staticmethod
    def dodaj_procedura(pojemnosc, pietro):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("dodaj_sale ?, ?", [pojemnosc, pietro])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':  # łapanie wyjątków z procedury oraz trigerów
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                return
                raise NameError(mes[0])
            elif sqlstate == '23000':  # łapanie błędów z warunków spójności
                raise NameError("Naruszono warunki spojnosci.")

    @staticmethod
    def odczyt():
        session = create_session(bind=engine)
        lista = session.query(Sala).all();
        session.close()
        return lista

    @staticmethod
    def zwroc_poID(ID_Sali):
        session = create_session(bind=engine)
        q = session.query(Sala).filter(Sala.ID_Sali == ID_Sali)
        rekord = q.one()
        return rekord

    @staticmethod
    def usun(ID_Sali):
        session = create_session(bind=engine)
        session.query(Sala).filter(Sala.ID_Sali == ID_Sali).delete()
        session.close()

    def usun_procedura(ID_Sali):
        cursor = engine.raw_connection().cursor()
        cursor.execute("usun_sale ?", [ID_Sali])
        cursor.commit()

    @staticmethod
    def modyfikuj(ID_Sali, Pojemnosc, Pietro):
        try:
            session = create_session(bind=engine)
            q = session.query(Sala)
            q = q.filter(Sala.ID_Sali == ID_Sali)
            record = q.one()
            if len(Pojemnosc) > 0:
                record.Pojemnosc = Pojemnosc
            if len(Pietro) > 0:
                record.Pietro = Pietro
            session.flush()
            session.close()

        except:
            raise NameError("Naruszono warunki spojnosci lub nie ma takiego trenera.")

    @staticmethod
    def modyfikuj_procedura(ID_Sali, Pojemnosc, Pietro):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("modyfikuj_sale, ?, ?, ?",
                           [ID_Sali, Pojemnosc, Pietro])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                raise NameError(mes[0])
            elif sqlstate == '23000':
                raise NameError("Naruszono warunki spojnosci.")

class Zajecia(Base):
    __table__ = Table('Zajecia', metadata, autoload=True)

    @staticmethod
    def dodaj(Nazwa, Ilosc_miejsc, ID_Trenera, Godzina_rozpoczecia, Godzina_zakonczenia, ID_Sali):
        try:
            noweZajecie = Zajecia(Nazwa=Nazwa, Ilosc_miejsc=Ilosc_miejsc, ID_Trenera=ID_Trenera, Godzina_rozpoczecia=Godzina_rozpoczecia,
                                  Godzina_zakonczenia=Godzina_zakonczenia, ID_Sali=ID_Sali)
            session = create_session(bind=engine)
            session.add(noweZajecie)
            session.flush()
            session.close()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise NameError(sqlstate)

    @staticmethod
    def dodaj_procedura(Nazwa, Ilosc_miejsc, ID_Trenera, Godzina_rozpoczecia, Godzina_zakonczenia, ID_Sali):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("dodaj_zajecie ?, ?, ?, ?, ?, ?", [Nazwa, Ilosc_miejsc, ID_Trenera, Godzina_rozpoczecia, Godzina_zakonczenia, ID_Sali])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':  # łapanie wyjątków z procedury oraz trigerów
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                return
                raise NameError(mes[0])
            elif sqlstate == '23000':  # łapanie błędów z warunków spójności
                raise NameError("Naruszono warunki spojnosci.")

    @staticmethod
    def odczyt():
        session = create_session(bind=engine)
        lista = session.query(Zajecia).all();
        session.close()
        return lista

    @staticmethod
    def zwroc_poID(ID_Zajecia):
        session = create_session(bind=engine)
        q = session.query(Zajecia).filter(Zajecia.ID_Zajecia == ID_Zajecia)
        rekord = q.one()
        return rekord

    @staticmethod
    def usun(ID_Zajecia):
        session = create_session(bind=engine)
        session.query(Zajecia).filter(Zajecia.ID_Zajecia == ID_Zajecia).delete()
        session.close()

    def usun_procedura(ID_Zajecia):
        cursor = engine.raw_connection().cursor()
        cursor.execute("usun_zajecie ?", [ID_Zajecia])
        cursor.commit()

    @staticmethod
    def modyfikuj(ID_Zajecia, Nazwa, Ilosc_miejsc, ID_Trenera, Godzina_rozpoczecia, Godzina_zakonczenia, ID_Sali):
        try:
            session = create_session(bind=engine)
            q = session.query(Zajecia)
            q = q.filter(Zajecia.ID_Zajecia == ID_Zajecia)
            record = q.one()
            if len(Nazwa) > 0:
                record.Nazwa = Nazwa
            if len(Ilosc_miejsc) > 0:
                record.Ilosc_miejsc = Ilosc_miejsc
            if len(ID_Trenera) > 0:
                record.ID_Trenera = ID_Trenera
            if len(Godzina_rozpoczecia) > 0:
                record.Godzina_rozpoczecia = Godzina_rozpoczecia
            if len(Godzina_zakonczenia) > 0:
                record.Godzina_zakonczenia = Godzina_zakonczenia
            if len(ID_Sali) > 0:
                record.ID_Sali = ID_Sali
            session.flush()
            session.close()

        except:
            raise NameError("Naruszono warunki spojnosci lub nie ma takiego trenera.")

    @staticmethod
    def modyfikuj_procedura(ID_Zajecia, Nazwa, Ilosc_miejsc, ID_Trenera, Godzina_rozpoczecia, Godzina_zakonczenia, ID_Sali):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("modyfikuj_zajecie, ?, ?, ?, ?, ?, ?, ?",
                           [ID_Zajecia, Nazwa, Ilosc_miejsc, ID_Trenera, Godzina_rozpoczecia, Godzina_zakonczenia, ID_Sali])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                raise NameError(mes[0])
            elif sqlstate == '23000':
                raise NameError("Naruszono warunki spojnosci.")

class Sprzet(Base):
    __table__ = Table('Sprzet', metadata, autoload=True)

    @staticmethod
    def dodaj(Nazwa, Ilosc, ID_Sali):
        try:
            nowySprzet = Sprzet(Nazwa=Nazwa, Ilosc=Ilosc, ID_Sali=ID_Sali)
            session = create_session(bind=engine)
            session.add(nowySprzet)
            session.flush()
            session.close()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            raise NameError(sqlstate)

    @staticmethod
    def dodaj_procedura(Nazwa, Ilosc, ID_Sali):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("dodaj_sprzet ?, ?, ?",
                           [Nazwa, Ilosc, ID_Sali])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':  # łapanie wyjątków z procedury oraz trigerów
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                return
                raise NameError(mes[0])
            elif sqlstate == '23000':  # łapanie błędów z warunków spójności
                raise NameError("Naruszono warunki spojnosci.")

    @staticmethod
    def odczyt():
        session = create_session(bind=engine)
        lista = session.query(Sprzet).all();
        session.close()
        return lista

    @staticmethod
    def zwroc_poID(ID_Sprzetu):
        session = create_session(bind=engine)
        q = session.query(Sprzet).filter(Sprzet.ID_Sprzetu == ID_Sprzetu)
        rekord = q.one()
        return rekord

    @staticmethod
    def usun(ID_Sprzetu):
        session = create_session(bind=engine)
        session.query(Sprzet).filter(Sprzet.ID_Sprzetu == ID_Sprzetu).delete()
        session.close()

    def usun_procedura(ID_Sprzetu):
        cursor = engine.raw_connection().cursor()
        cursor.execute("usun_sprzet ?", [ID_Sprzetu])
        cursor.commit()

    @staticmethod
    def modyfikuj(ID_Sprzetu, Nazwa, Ilosc, ID_Sali):
        try:
            session = create_session(bind=engine)
            q = session.query(Sprzet).with_for_update().filter(Sprzet.ID_Sprzetu == ID_Sprzetu)
            record = q.one()
            record.Nazwa = Nazwa
            record.Ilosc_miejsc = Ilosc
            record.ID_Sali = ID_Sali
            session.flush()
            session.close()

        except:

            session.rollback()

    @staticmethod
    def modyfikuj_procedura(ID_Sprzetu, Nazwa, Ilosc, ID_Sali):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("modyfikuj_sprzet, ?, ?, ?, ?",
                           [ID_Sprzetu, Nazwa, Ilosc, ID_Sali])
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                raise NameError(mes[0])
            elif sqlstate == '23000':
                raise NameError("Naruszono warunki spojnosci.")

def generuj_raport(ID_Trenera):
    session = create_session(bind=engine)
    return session.execute('exec raport :val', {'val': ID_Trenera}).fetchall()

def klient_zajecia(ID_Klienta):
    try:
        session = create_session(bind=engine)
        return session.execute('exec klient_lista_zajec :val', {'val': ID_Klienta}).fetchall()
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '42000':
            mes = ex.args[1].split(']')
            mes = mes[4].split('(')
            raise NameError(mes[0])

def klient_lista_oczekujaca(ID_Klienta):
    try:
        session = create_session(bind=engine)
        return session.execute('exec klient_lista_oczekujacych :val', {'val': ID_Klienta}).fetchall()
    except pyodbc.Error as ex:

        sqlstate = ex.args[0]
        if sqlstate == '42000':
            mes = ex.args[1].split(']')
            mes = mes[4].split('(')
            raise NameError(mes[0])



def dodaj_klienta_do_zajec(ID_Klienta, ID_Zajecia):
    try:
        cursor = engine.raw_connection().cursor()
        cursor.execute('dodaj_klienta_do_zajec ?, ?', [ID_Klienta, ID_Zajecia])
        cursor.commit()
    except pyodbc.Error as ex:
        mes = ex.args[1].split(']')
        mes = mes[4].split('(')
        return
        raise NameError(mes[0])

def usun_lista(ID_Klienta, ID_Zajecia):
    try:
        cursor = engine.raw_connection().cursor()
        cursor.execute('usun_lista ?, ?', [ID_Klienta, ID_Zajecia])
        cursor.commit()
    except pyodbc.Error as ex:
        mes = ex.args[1].split(']')
        mes = mes[4].split('(')
        return
        raise NameError(mes[0])

def usun_uczestnicza(ID_Klienta, ID_Zajecia):
    try:
        cursor = engine.raw_connection().cursor()
        cursor.execute('usun_uczestnicza ?, ?', [100, ID_Zajecia])
        cursor.commit()
    except pyodbc.Error as ex:
        mes = ex.args[1].split(']')
        mes = mes[4].split('(')
        return
        raise NameError(mes[0])
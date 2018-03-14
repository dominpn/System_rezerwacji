import pyodbc
from tkinter import *
import tkinter.messagebox
from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import text
from sqlalchemy_views import CreateView, DropView


Base = declarative_base()
root=Tk()
try:
    engine = create_engine("mssql+pyodbc://dominik:dominik@DOMINIK-LAPTOP\SQLEXPRESS/System_rezerwacji?driver=SQL+Server+Native+Client+11.0")
    metadata = MetaData(bind=engine)
except:
    tkinter.messagebox.showinfo("Blad", "Nie udalo sie polaczyc")

class Klienci(Base):
    try:
        __table__ = Table('Klienci', metadata, autoload=True)
    except:
        tkinter.messagebox.showinfo("Blad", "Nie udalo sie pobrac tabeli")
class Dodaj():
    def __init__(self):
        self.root = Tk()
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.root.title("Dodaj")
        self.fnameLabel = Label(self.root, text="Imie:", width=20)
        self.fnameLabel.grid(row=0, column=0)
        self.fnameEntry = Entry(self.root, width=20, bg="white")
        self.fnameEntry.grid(row=1, column=0)
        self.lnameLabel = Label(self.root, text="Nazwisko:", width=20)
        self.lnameLabel.grid(row=2, column=0)
        self.lnameEntry = Entry(self.root, width=20, bg="white")
        self.lnameEntry.grid(row=3, column=0)
        self.emailLabel = Label(self.root, text="Email:", width=20)
        self.emailLabel.grid(row=4, column=0)
        self.emailEntry = Entry(self.root, width=20, bg="white")
        self.emailEntry.grid(row=5, column=0)
        self.datestartLabel = Label(self.root, text="Data rozpoczecia karnetu:", width=20)
        self.datestartLabel.grid(row=6, column=0)
        self.datestartEntry = Entry(self.root, width=20, bg="white")
        self.datestartEntry.grid(row=7, column=0)
        self.dateendLabel = Label(self.root, text="Data zakonczenia karnetu:", width=20)
        self.dateendLabel.grid(row=8, column=0)
        self.dateendEntry = Entry(self.root, width=20, bg="white")
        self.dateendEntry.grid(row=9, column=0)
        self.Label = Label(self.root, text=":", width=20)
        self.Label.grid(row=10, column=0)
        self.button = Button(self.root, text="Wprowadz", width=20, command=self.click)
        self.button.grid(row=11, column=0)
        self.button_procedure = Button(self.root, text="Wprowadz procedura", width=20, command=self.click_procedure)
        self.button_procedure.grid(row=12, column=0)
    def click(self):
        try:
            nowyKlient = Klienci(Imie = self.fnameEntry.get(), Nazwisko = self.lnameEntry.get(),
                                 Adres_email = self.emailEntry.get(), Karnet_data_rozpoczecia=self.datestartEntry.get(),
                                 Karnet_data_zakonczenia=self.dateendEntry.get())

            session = create_session(bind=engine)
            session.add(nowyKlient)
            session.flush()
            session.close()
            self.root.destroy()
            Odswiez()
        except:
            tkinter.messagebox.showinfo("Blad", "Naruszono warunki spojnosci. \nAdres email musi byc w formie aaa@aaa.aaa, "
                                                "data w formacie YYYY.MM.DD, data zakonczenia pozniejsza od daty rozpoczecia")
    def click_procedure(self):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("dodaj_klienta ?, ?, ?, ?, ?", [self.fnameEntry.get(), self.lnameEntry.get(), self.emailEntry.get(),
                                                        self.datestartEntry.get(), self.dateendEntry.get()])
            cursor.commit()
            self.root.destroy()
            Odswiez()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000': #łapanie wyjątków z procedury oraz trigerów
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                tkinter.messagebox.showinfo("Blad", mes[0])
            elif sqlstate == '23000': #łapanie błędów z warunków spójności
                tkinter.messagebox.showinfo("Blad", "Naruszono warunki spojnosci. \nAdres email musi byc w formie aaa@aaa.aaa, "
                                                "data w formacie YYYY.MM.DD, data zakonczenia pozniejsza od daty rozpoczecia")

class Usun():
    def __init__(self):
        self.root = Tk()
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.root.title("Usun")
        self.indexLabel = Label(self.root, text="Podaj ID do usuniecia:", width=20)
        self.indexLabel.grid(row=0, column=0)
        self.index_Entry = Entry(self.root, width=20, bg="white")
        self.index_Entry.grid(row=1, column=0)
        self.button = Button(self.root, text="Akceptuj", width=20, command=self.click)
        self.button.grid(row=2, column=0)
        self.button_procedure = Button(self.root, text="Usun procedura", width=20, command=self.click_procedure)
        self.button_procedure.grid(row=3, column=0)
    def click(self):
        self.id = self.index_Entry.get()
        session = create_session(bind=engine)
        session.query(Klienci).filter(Klienci.ID_Klienta==self.id).delete()
        session.close()
        self.root.destroy()
        Odswiez()
    def click_procedure(self):
        cursor = engine.raw_connection().cursor()
        cursor.execute("usun_klienta ?", [self.index_Entry.get()])
        cursor.commit()
        self.root.destroy()
        Odswiez()
class Modyfikuj():
    def __init__(self):
        self.root = Tk()
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.root.title("Modyfikuj")
        tkinter.messagebox.showinfo("Informacja","Podaj ID klienta, ktorego dane chcesz zmodyfikowac. Pola ktore nie chcesz modyfikowac pozostaw puste")
        self.indexLabel = Label(self.root, text="Podaj ID klienta:", width=20)
        self.indexLabel.grid(row=0, column=0)
        self.index_Entry = Entry(self.root, width=20, bg="white")
        self.index_Entry.grid(row=1, column=0)
        self.fnameLabel = Label(self.root, text="Imie:", width=20)
        self.fnameLabel.grid(row=2, column=0)
        self.fnameEntry = Entry(self.root, width=20, bg="white")
        self.fnameEntry.grid(row=3, column=0)
        self.lnameLabel = Label(self.root, text="Nazwisko:", width=20)
        self.lnameLabel.grid(row=4, column=0)
        self.lnameEntry = Entry(self.root, width=20, bg="white")
        self.lnameEntry.grid(row=5, column=0)
        self.emailLabel = Label(self.root, text="Email:", width=20)
        self.emailLabel.grid(row=6, column=0)
        self.emailEntry = Entry(self.root, width=20, bg="white")
        self.emailEntry.grid(row=7, column=0)
        self.datestartLabel = Label(self.root, text="Data rozpoczecia karnetu:", width=20)
        self.datestartLabel.grid(row=8, column=0)
        self.datestartEntry = Entry(self.root, width=20, bg="white")
        self.datestartEntry.grid(row=9, column=0)
        self.dateendLabel = Label(self.root, text="Data zakonczenia karnetu:", width=20)
        self.dateendLabel.grid(row=10, column=0)
        self.dateendEntry = Entry(self.root, width=20, bg="white")
        self.dateendEntry.grid(row=11, column=0)
        self.Label = Label(self.root, text=":", width=20)
        self.Label.grid(row=12, column=0)
        self.button = Button(self.root, text="Wprowadz", width=20, command=self.click)
        self.button.grid(row=13, column=0)
        self.button_procedure = Button(self.root, text="Wprowadz procedura", width=20, command=self.click_procedure)
        self.button_procedure.grid(row=14, column=0)
    def click(self):
        try:
            session = create_session(bind=engine)
            q = session.query(Klienci)
            q = q.filter(Klienci.ID_Klienta == self.index_Entry.get())
            record = q.one()
            if len(self.fnameEntry.get())>0:
                record.Imie = self.fnameEntry.get()
            if len(self.lnameEntry.get())>0:
                record.Nazwisko = self.lnameEntry.get()
            if len(self.emailEntry.get())>0:
                record.r = self.emailEntry.get()
            if len(self.datestartEntry.get())>0:
                record.Karnet_data_rozpoczecia = self.datestartEntry.get()
            if len(self.dateendEntry.get())>0:
                record.Karnet_data_zakonczenia = self.dateendEntry.get()
            session.flush()
            session.close()
            self.root.destroy()
            Odswiez()
        except:
            tkinter.messagebox.showinfo("Blad", "Naruszono warunki spojnosci lub nie ma takiego klienta. \n"
                                                "Adres email musi byc w formie aaa@aaa.aaa, data w formacie YYYY.MM.DD, data zakonczenia pozniejsza "
                                                "od daty rozpoczecia")
    def click_procedure(self):
        try:
            cursor = engine.raw_connection().cursor()
            cursor.execute("modyfikuj_klienta ?, ?, ?, ?, ?, ?",
                        [self.index_Entry.get() ,self.fnameEntry.get(), self.lnameEntry.get(), self.emailEntry.get(),
                            self.datestartEntry.get(), self.dateendEntry.get()])
            cursor.commit()
            self.root.destroy()
            Odswiez()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':
                mes = ex.args[1].split(']')
                mes = mes[4].split('(')
                tkinter.messagebox.showinfo("Blad", mes[0])
            elif sqlstate == '23000':
                tkinter.messagebox.showinfo("Blad", "Naruszono warunki spojnosci. \nAdres email musi byc w formie aaa@aaa.aaa, "
                                                "data w formacie YYYY.MM.DD, data zakonczenia pozniejsza od daty rozpoczecia")
class Klienci_widok():
    def __init__(self,master):
        self.master=master
        self.master.title("Klienci")

        self.showallrecords()



    def showallrecords(self):
        data = self.readfromdatabase()
        Label(self.master, text="ID Klienta", width=10).grid(row=0, column=0)
        Label(self.master, text="Imie", width=10).grid(row=0, column=1)
        Label(self.master, text="Nazwisko", width=10).grid(row=0, column=2)
        Label(self.master, text="Email", width=10).grid(row=0, column=3)
        Label(self.master, text="Data rozpoczecia karnetu", width=20).grid(row=0, column=4)
        Label(self.master, text="Data zakonczenia karnetu", width=20).grid(row=0, column=5)
        for index, dat in enumerate(data):
            Label(self.master, text=dat.ID_Klienta).grid(row=index + 1, column=0)
            Label(self.master, text=dat.Imie).grid(row=index + 1, column=1)
            Label(self.master, text=dat.Nazwisko).grid(row=index + 1, column=2)
            Label(self.master, text=dat.Adres_email).grid(row=index + 1, column=3)
            Label(self.master, text=dat.Karnet_data_rozpoczecia).grid(row=index + 1, column=4)
            Label(self.master, text=dat.Karnet_data_zakonczenia).grid(row=index + 1, column=5)

    def readfromdatabase(self):
        session = create_session(bind=engine)
        testlist = session.query(Klienci).all();
        session.close()
        return testlist

def main():
    Klienci_widok(root)
    menu = Menu(root)
    root.config(menu=menu)
    subMenu = Menu(menu)
    menu.add_cascade(label="Narzedzia", menu=subMenu)
    subMenu.add_command(label="Dodaj", command=Dodaj)
    subMenu.add_command(label="Usun", command=Usun)
    subMenu.add_command(label="Zmodyfikuj", command=Modyfikuj)
    root.mainloop()
def Odswiez():
    list = root.grid_slaves()
    for l in list:
        l.destroy()
    Klienci_widok(root)

if __name__ == '__main__':
    main()
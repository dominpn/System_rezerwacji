create database System_rezerwacji
use System_rezerwacji
create table Trenerzy
(ID_Trenera int PRIMARY KEY NOT NULL Identity(1,1),  
    Imie varchar(25) NOT NULL,  
	Nazwisko varchar(25) NOT NULL,
	Specjalnosc varchar(25) NOT NULL)
create table Sala
(ID_Sali int PRIMARY KEY NOT NULL Identity(1,1),  
    Pojemnosc int NOT NULL,  
	Pietro int NOT NULL)
create table Zajecia
(ID_Zajecia int PRIMARY KEY NOT NULL Identity(1,1),  
    Nazwa varchar(25) NOT NULL,  
	Ilosc_miejsc int NOT NULL,
	ID_Trenera int foreign key references Trenerzy(ID_Trenera),
	Godzina_rozpoczecia DECIMAL(2,2) not null,
	Godzina_zakonczenia DECIMAL(2,2) not null,
	ID_Sali int foreign key references Sala(ID_Sali)
	)
create table Klienci
(ID_Klienta int PRIMARY KEY NOT NULL Identity(1,1),  
    Imie varchar(25) NOT NULL,  
	Nazwisko varchar(25) NOT NULL,
	Adres_email varchar(255),
	Karnet_data_rozpoczecia date NOT NULL,
	Karnet_data_zakonczenia date not null)



create table Sprzet
(ID_Sprzetu int PRIMARY KEY NOT NULL Identity(1,1),  
    Nazwa varchar(100) NOT NULL,  
	Ilosc int NOT NULL,
	ID_Sali int foreign key references Sala(ID_Sali))

create table Uczestnicza
(	ID_Klienta int foreign key references Klienci(ID_Klienta),
	ID_Zajecia int foreign key references Zajecia(ID_Zajecia))

	create table Lista_oczekujacych
(	ID_Klienta int foreign key references Klienci(ID_Klienta),
	ID_Zajecia int foreign key references Zajecia(ID_Zajecia))


alter table Klienci
add constraint Email_check check (Adres_email like '[a-z,0-9,_,-]%@[a-z,0-9,_,-]%.[a-z][a-z]%')

alter table Klienci
add constraint Date_check check (Karnet_data_rozpoczecia < Karnet_data_zakonczenia)


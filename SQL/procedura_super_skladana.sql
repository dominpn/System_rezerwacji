alter procedure dodaj_klienta_do_zajec
@ID_Klienta int,
@ID_Zajecia int
as begin
declare @Pojemnosc int set @Pojemnosc = (select Ilosc_miejsc from Zajecia where ID_Zajecia=@ID_Zajecia)
declare @Ilosc_klientow_na_zajeciach int 
set @Ilosc_klientow_na_zajeciach = (select count(*) from Uczestnicza where ID_Zajecia=@ID_Zajecia)
declare @Klient_jest_juz_na_liscie int 
set @Klient_jest_juz_na_liscie = (select count(*) from Uczestnicza where ID_Klienta=@ID_Klienta and ID_Zajecia=@ID_Zajecia)
declare @Klient_na_liscie_oczekujacych int 
set @Klient_na_liscie_oczekujacych = (select count(*) from Lista_oczekujacych where ID_Klienta=@ID_Klienta and ID_Zajecia=@ID_Zajecia)
if @Klient_jest_juz_na_liscie = 1
begin
raiserror ('Uczestniczysz w tych zajeciach. Wybierz inne',16,1)
end
else
if @Pojemnosc>@Ilosc_klientow_na_zajeciach
begin
insert into Uczestnicza(ID_Klienta,ID_Zajecia)
values (@ID_Klienta,@ID_Zajecia)
end
else
if @Klient_na_liscie_oczekujacych=1
begin
raiserror ('Jestes juz na liscie oczekujacych', 16,1)
end
else
begin
insert into Lista_oczekujacych(ID_Klienta,ID_Zajecia)
values (@ID_Klienta,@ID_Zajecia)
raiserror ('Niestety brak miejsc. Zostales dodany do listy oczekujacych',16,1)
end
end

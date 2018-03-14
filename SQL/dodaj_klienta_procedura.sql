IF OBJECT_ID('dodaj_klienta', 'P') IS NOT NULL
DROP PROCEDURE dodaj_klienta
GO

CREATE PROCEDURE dodaj_klienta
@Imie varchar(25),
@Nazwisko varchar(25),
@Adres_email varchar(255),
@Karnet_data_rozpoczecia date,
@Karnet_data_zakonczenia date
AS
BEGIN
if LEN(@Imie) < 2
BEGIN
raiserror('Imie musi mieæ co najmniej 2 znaki', 16, 1)
END
if LEN(@Nazwisko) < 2
BEGIN
raiserror('Nazwisko musi mieæ co najmniej 2 znaki', 16, 1)
END
if SUBSTRING(@Imie,1,1) != UPPER(SUBSTRING(@Imie,1,1))
BEGIN
raiserror('Imie musi zaczynac sie z wielkiej litery', 16,1)
END
if SUBSTRING(@Nazwisko,1,1) != UPPER(SUBSTRING(@Nazwisko,1,1))
BEGIN
raiserror('Nazwisko musi zaczynac sie z wielkiej litery', 16,1)
END
INSERT INTO Klienci Values (@Imie, @Nazwisko, @Adres_email, @Karnet_data_rozpoczecia,
@Karnet_data_zakonczenia)
return 0
END
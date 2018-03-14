IF OBJECT_ID('modyfikuj_klienta', 'P') IS NOT NULL
DROP PROCEDURE modyfikuj_klienta
GO

CREATE PROCEDURE modyfikuj_klienta
@ID_Klienta int,
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
UPDATE Klienci SET Imie=@Imie, Nazwisko=@Nazwisko, Adres_email=@Adres_email,
					Karnet_data_rozpoczecia=@Karnet_data_rozpoczecia,
					Karnet_data_zakonczenia=@Karnet_data_zakonczenia
					WHERE ID_Klienta=@ID_Klienta
IF @@ROWCOUNT=0
BEGIN
raiserror('Aktualizacja danych nieudana',16,1)
END
return 0
END
IF OBJECT_ID('usun_klienta', 'P') IS NOT NULL
DROP PROCEDURE usun_klienta
GO

CREATE PROCEDURE usun_klienta
@ID_Klienta int
AS
BEGIN
DELETE FROM Klienci WHERE ID_Klienta=@ID_Klienta
IF @@ROWCOUNT=0
BEGIN
raiserror('Usuniecie danych nie powiodlo sie',16,1)
END
return 0
END
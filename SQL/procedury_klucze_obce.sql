create PROCEDURE usun_lista
@ID_Klienta int,
@ID_Zajecia int
AS
BEGIN
DELETE FROM Lista_oczekujacych WHERE ID_Klienta=@ID_Klienta and ID_Zajecia=@ID_Zajecia
IF @@ROWCOUNT=0
BEGIN
raiserror('Usuniecie danych nie powiodlo sie',16,1)
END
return 0
END

alter PROCEDURE usun_uczestnicza
@ID_Klienta int,
@ID_Zajecia int
AS
BEGIN
SET NOCOUNT ON
    SET XACT_ABORT ON

    BEGIN TRY
        BEGIN TRANSACTION
DELETE FROM Uczestnicza WHERE ID_Klienta=@ID_Klienta and ID_Zajecia=@ID_Zajecia
COMMIT
    END TRY
    BEGIN CATCH

        SELECT ERROR_MESSAGE()
		raiserror('Usuniecie danych nie powiodlo sie',16,1)
        IF @@TRANCOUNT>0
            ROLLBACK

    END CATCH

END

select * from Uczestnicza

exec usun_uczestnicza 67,10
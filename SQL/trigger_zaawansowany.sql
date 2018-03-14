use System_rezerwacji
go
alter trigger Oczekujacy_jako_Uczestnik
ON Uczestnicza
AFTER DELETE
as 
declare @id_zajecia int
set @id_zajecia = (select ID_Zajecia from deleted)
begin transaction
if exists (select * from Lista_oczekujacych where ID_Zajecia=@id_zajecia)
begin
declare @id_klienta int
set @id_klienta = (select top 1 ID_Klienta from Lista_oczekujacych where ID_Zajecia=@id_zajecia)
BEGIN TRANSACTION 
insert into Uczestnicza values (@id_klienta, @id_zajecia)
IF @@ERROR <> 0 
            BEGIN 
                        RAISERROR ('B³¹d, operacja nie udana!', 16, 1) 
                        ROLLBACK TRANSACTION 
            END 
delete from Lista_oczekujacych where ID_Klienta=@id_klienta and ID_Zajecia=@id_zajecia
IF @@ERROR <> 0 
            BEGIN 
                        RAISERROR ('B³¹d, operacja nie udana!', 16, 1) 
                        ROLLBACK TRANSACTION 
            END 
COMMIT TRANSACTION
end



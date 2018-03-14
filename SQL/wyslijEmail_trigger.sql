CREATE TRIGGER wyslijEmail
ON Klienci
AFTER INSERT
AS
declare @klient varchar(50)
set @klient=(select Imie+', '+Nazwisko from inserted)
declare @tresc varchar(200)
set @tresc='Mamy nowego klienta ' + @klient;
EXEC msdb.dbo.sp_send_dbmail
@profile_name = 'Profil',
@recipients = 'dominik.krystkowiak@student.put.poznan.pl',
@body = @tresc,
@subject = @klient;
GO
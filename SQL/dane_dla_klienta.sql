alter procedure klient_lista_zajec
@id_klienta int
as
begin
select u.ID_Zajecia, z.Nazwa from Zajecia z inner join Uczestnicza u on z.ID_Zajecia=u.ID_Zajecia 
where u.ID_Klienta=@id_klienta
end

alter procedure klient_lista_oczekujacych
@id_klienta int
as
begin
select  lo.ID_Zajecia, z.Nazwa from Zajecia z inner join Lista_oczekujacych lo on z.ID_Zajecia=lo.ID_Zajecia 
where lo.ID_Klienta=@id_klienta
end
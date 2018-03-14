create procedure raport
@id_trenera int
as
begin
select k.Imie, k.Nazwisko, z.Nazwa from Zajecia z inner join Uczestnicza u on z.ID_Zajecia=u.ID_Zajecia 
inner join Klienci k on k.ID_Klienta=u.ID_Klienta inner join Trenerzy t on z.ID_Trenera=t.ID_Trenera 
where t.ID_Trenera=@id_trenera order by z.Nazwa
end
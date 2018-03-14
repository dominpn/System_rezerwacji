from baza_danych import *
from mongodb import *
from flask import render_template, request, Flask, url_for, redirect, flash, session, g
from decimal import *




app = Flask(__name__)
app.secret_key='123'



@app.route('/klienci')
def wszyscy_klienci():
    if g.admin:
        try:
            Lista_Klientow= Klienci.readfromdatabase()
            return render_template('klienci/klienci.html',klienci=Lista_Klientow)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))

@app.route('/klienci/<int:ID>/usun')
def usun_klienta(ID):
    if g.admin:
        try:
            Klienci.usun_procedura(ID)
            usun_klienta_mongo(ID)
        except NameError as error:
            flash(str(error))
        return redirect(url_for('wszyscy_klienci'))
    return redirect(url_for('homepage'))


@app.route('/klienci/<int:ID_Klienta>')
def klient_poID(ID_Klienta):
    if g.admin:
        try:
            Klient = Klienci.zwroc_poID(ID_Klienta)
            return render_template('klienci/modyfikuj.html', klient=Klient)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))

@app.route('/klienci/<int:ID_Klienta>', methods=['POST'])
def klient_modyfikuj(ID_Klienta):
    if g.admin:
        if request.method == 'POST':
            try:
                Klienci.modyfikuj_procedura(ID_Klienta, request.form['Imie'], request.form['Nazwisko'], request.form['Email'],
                                request.form['Karnet_rozpoczecie'], request.form['Karnet_zakonczenie'])
                return redirect(url_for('wszyscy_klienci'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('klient_poID', ID_Klienta=ID_Klienta))
    return redirect(url_for('homepage'))

@app.route('/klienci/dodaj')
def dodaj():
    if g.admin:
        return render_template('klienci/dodaj_klienta.html')
    return redirect(url_for('homepage'))

@app.route('/klienci/dodaj', methods=['POST'])
def dodaj_klienta():
    if g.admin:
        if request.method == 'POST':
            try:
                Klienci.click_procedure(request.form['Imie'], request.form['Nazwisko'], request.form['Email'],
                                        request.form['Karnet_rozpoczecie'], request.form['Karnet_zakonczenie'])
                ID = Klienci.zwroc_ID(request.form['Imie'], request.form['Nazwisko'], request.form['Email'],
                                      request.form['Karnet_rozpoczecie'], request.form['Karnet_zakonczenie'])
                dodaj_klienta_mongo(ID, request.form['Imie'], request.form['Nazwisko'])
                return redirect(url_for('wszyscy_klienci'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('dodaj'))
    return redirect(url_for('homepage'))


@app.route('/trenerzy')
def wszyscy_trenerzy():
    if g.admin:
        try:
            Lista_Trenerow= Trenerzy.odczyt()
            return render_template('trenerzy/trenerzy.html',trenerzy=Lista_Trenerow)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))

@app.route('/trenerzy/<int:ID>/usun')
def usun_trenera(ID):
    if g.admin:
        try:
            Trenerzy.usun(ID)
        except NameError as error:
            flash(str(error))
        return redirect(url_for('wszyscy_trenerzy'))
    return redirect(url_for('homepage'))

@app.route('/trenerzy/<int:ID_Trenera>')
def trener_poID(ID_Trenera):
    if g.admin:
        try:
            Trener = Trenerzy.zwroc_poID(ID_Trenera)
            return render_template('trenerzy/modyfikuj_trenera.html', trener=Trener)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))

@app.route('/trenerzy/<int:ID_Trenera>', methods=['POST'])
def trener_modyfikuj(ID_Trenera):
    if g.admin:
        if request.method == 'POST':
            try:
                Trenerzy.modyfikuj(ID_Trenera, request.form['Imie'], request.form['Nazwisko'], request.form['Specjalnosc'])
                return redirect(url_for('wszyscy_trenerzy'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('trener_poID', ID_Trenera=ID_Trenera))
    return redirect(url_for('homepage'))

@app.route('/trenerzy/dodaj_trenera')
def dodaj_trenera_strona():
    if g.admin:
        return render_template('trenerzy/dodaj_trenera.html')
    return redirect(url_for('homepage'))

@app.route('/trenerzy/dodaj_trenera', methods=['POST'])
def dodaj_trenera():
    if g.admin:
        if request.method == 'POST':
            try:
                Trenerzy.dodaj(request.form['Imie'], request.form['Nazwisko'], request.form['Specjalnosc'])
                return redirect(url_for('wszyscy_trenerzy'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('dodaj_trenera_strona'))
    return redirect(url_for('homepage'))


@app.route('/trenerzy/<int:ID_Trenera>/raport')
def trener_raport(ID_Trenera):
    if g.admin:
        Uczestnicy = generuj_raport(ID_Trenera)
        Trener = Trenerzy.zwroc_poID(ID_Trenera)
        Lista_Zajec = Zajecia.odczyt()
        return render_template('raport.html', trener=Trener, uczestnicy=Uczestnicy, lista=Lista_Zajec)
    return redirect(url_for('homepage'))


@app.route('/sale')
def wszyskie_sale():
    if g.admin:
        try:
            Lista_Sal= Sala.odczyt()
            return render_template('sale/sale.html',sale=Lista_Sal)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))

@app.route('/sale/<int:ID>/usun')
def usun_sale(ID):
    if g.admin:
        try:
            Sala.usun(ID)
        except NameError as error:
            flash(str(error))
        return redirect(url_for('wszyskie_sale'))
    return redirect(url_for('homepage'))


@app.route('/sale/<int:ID_Sali>')
def sala_poID(ID_Sali):
    if g.admin:
        try:
            sala = Sala.zwroc_poID(ID_Sali)
            return render_template('sale/modyfikuj_sale.html', sala=sala)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))


@app.route('/sale/<int:ID_Sali>', methods=['POST'])
def sala_modyfikuj(ID_Sali):
    if g.admin:
        if request.method == 'POST':
            try:
                Sala.modyfikuj(ID_Sali, request.form['Pojemnosc'], request.form['Pietro'])
                return redirect(url_for('wszyskie_sale'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('sala_poID', ID_Sali=ID_Sali))
    return redirect(url_for('homepage'))


@app.route('/sale/dodaj_sale')
def dodaj_sale_strona():
    if g.admin:
        return render_template('sale/dodaj_sale.html')
    return redirect(url_for('homepage'))


@app.route('/sale/dodaj_sale', methods=['POST'])
def dodaj_sale():
    if g.admin:
        if request.method == 'POST':
            try:
                Sala.dodaj(request.form['Pojemnosc'], request.form['Pietro'])
                return redirect(url_for('wszyskie_sale'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('dodaj_sale_strona'))
    return redirect(url_for('homepage'))


@app.route('/zajecia')
def wszyskie_zajecia():
    if g.admin:
        try:
            Lista_Zajec= Zajecia.odczyt()
            Lista_Trenerow = Trenerzy.odczyt()
            return render_template('zajecia/zajecia.html',zajecia=Lista_Zajec, trenerzy=Lista_Trenerow)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))

@app.route('/zajecia/<int:ID>/usun')
def usun_zajecie(ID):
    if g.admin:
        try:
            Zajecia.usun(ID)
        except NameError as error:
            flash(str(error))
        return redirect(url_for('wszyskie_zajecia'))
    return redirect(url_for('homepage'))

@app.route('/zajecia/<int:ID_Zajecia>')
def zajecie_poID(ID_Zajecia):
    if g.admin:
        try:
            zajecie = Zajecia.zwroc_poID(ID_Zajecia)
            sale = Sala.odczyt()
            trenerzy = Trenerzy.odczyt()
            return render_template('zajecia/modyfikuj_zajecie.html', zajecie=zajecie, sale=sale, trenerzy=trenerzy)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))

@app.route('/zajecia/<int:ID_Zajecia>', methods=['POST'])
def zajecia_modyfikuj(ID_Zajecia):
    if g.admin:
        if request.method == 'POST':
            try:
                Zajecia.modyfikuj(ID_Zajecia, request.form['Nazwa'], request.form['Ilosc_miejsc'],
                               request.form['ID_Trenera'], request.form('Godzina_rozpoczecia'),
                               request.form('Godzina_zakonczenia'), request.form('ID_Sali'))
                return redirect(url_for('wszyskie_zajecia'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('zajecie_poID', ID_Zajecia=ID_Zajecia))
    return redirect(url_for('homepage'))


@app.route('/zajecia/dodaj_zajecie')
def dodaj_zajecie_strona():
    if g.admin:
        try:
            sale= Sala.odczyt()
            trenerzy = Trenerzy.odczyt()
            return render_template('zajecia/dodaj_zajecie.html',sale=sale, trenerzy=trenerzy)
        except NameError as error:
            flash(str(error))
            redirect(url_for('wszyskie_sale'))
    return redirect(url_for('homepage'))

@app.route('/zajecia/dodaj_zajecie', methods=['POST'])
def dodaj_zajecie():
    if g.admin:
        if request.method == 'POST':
            try:
                trener = request.form['Trener'].split(' ')
                session = create_session(bind=engine)
                q = session.query(Trenerzy).filter(Trenerzy.Imie == trener[0], Trenerzy.Nazwisko==trener[1])
                rekord = q.one()
                print(request.form['Sala'])
                getcontext().prec = 2
                Zajecia.dodaj(request.form['Nazwa'], request.form['Ilosc_miejsc'],
                               rekord.ID_Trenera, request.form['Godzina_rozpoczecia'],
                              request.form['Godzina_zakonczenia'], request.form['Sala'])
                return redirect(url_for('wszyskie_zajecia'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('dodaj_zajecie_strona'))
    return redirect(url_for('homepage'))

@app.route('/sprzet')
def caly_sprzet():
    if g.admin:
        try:
            Lista_Sprzetow= Sprzet.odczyt()
            return render_template('sprzet/sprzet.html',sprzet=Lista_Sprzetow)
        except NameError as error:
            flash(str(error))
            return render_template('main.html')
    return redirect(url_for('homepage'))


@app.route('/sprzet/<int:ID>/usun')
def usun_sprzet(ID):
    if g.admin:
        try:
            Sprzet.usun(ID)
        except NameError as error:
            flash(str(error))
        return redirect(url_for('caly_sprzet'))
    return redirect(url_for('homepage'))


@app.route('/sprzet/<int:ID_Sprzetu>')
def sprzet_poID(ID_Sprzetu):
    if g.admin:
        try:
            sprzet = Sprzet.zwroc_poID(ID_Sprzetu)
            sale = Sala.odczyt()
            return render_template('sprzet/modyfikuj_sprzet.html', sprzet=sprzet, sale=sale)
        except NameError as error:
            flash(str(error))
            return redirect(url_for('caly_sprzet'))
    return redirect(url_for('homepage'))


@app.route('/sprzet/<int:ID_Sprzetu>', methods=['POST'])
def sprzet_modyfikuj(ID_Sprzetu):
    if g.admin:
        if request.method == 'POST':
            try:
                Sprzet.modyfikuj(ID_Sprzetu, request.form['Nazwa'], request.form['Ilosc'],
                request.form['Sala'])
                return redirect(url_for('caly_sprzet'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('sprzet_poID', ID_Sprzetu=ID_Sprzetu))
    return redirect(url_for('homepage'))

@app.route('/sprzet/dodaj_sprzet')
def dodaj_sprzet_strona():
    if g.admin:
        try:
            sale= Sala.odczyt()
            return render_template('sprzet/dodaj_sprzet.html',sale=sale)
        except NameError as error:
            flash(str(error))
            redirect(url_for('caly_sprzet'))
    return redirect(url_for('homepage'))

@app.route('/sprzet/dodaj_sprzet', methods=['POST'])
def dodaj_sprzet():
    if g.admin:
        if request.method == 'POST':
            try:
                Sprzet.dodaj(request.form['Nazwa'], request.form['Ilosc'],
                             request.form['Sala'])
                return redirect(url_for('caly_sprzet'))
            except NameError as error:
                flash(str(error))
                return redirect(url_for('dodaj_sprzet_strona'))
    return redirect(url_for('homepage'))

@app.route('/', methods=['GET','POST'])
def homepage():
    if request.method == 'POST':
        try:
            session.pop('admin', None)
            session.pop('user', None)
            uzytkownik = zwroc_uzytkownika(request.form['login'])
            if request.form['haslo'] == uzytkownik["haslo"] and "admin"==uzytkownik["typ_uzytkownika"]:
                session['admin'] = uzytkownik["id"]
                return redirect(url_for('wszyscy_klienci'))
            elif request.form['haslo'] == uzytkownik['haslo'] and "klient" == uzytkownik["typ_uzytkownika"]:
                session['user'] = uzytkownik["id"]
                return redirect(url_for('klient_widok', ID_Klienta=uzytkownik["id"]))
            else:
                flash(str("Bledne haslo"))
                return render_template('login.html')
        except:
            flash(str("Nie ma takiego uzytkownika"))
            return render_template('login.html')
    return render_template('login.html')
@app.route('/wyloguj')
def wyloguj():
    session.pop('admin', None)
    flash(str("Wylogowano. Zaloguj się ponownie"))
    return redirect(url_for('homepage'))
@app.before_request
def sesja():
    g.admin = None
    g.user = None
    if 'admin' in session:
        g.admin = session['admin']
    elif 'user' in session:
        g.user = session['user']

@app.route('/<int:ID_Klienta>', methods=['GET','POST'])
def klient_widok(ID_Klienta):
    if g.user==ID_Klienta:
        Zajecia_ucz = klient_zajecia(ID_Klienta)
        Lista = klient_lista_oczekujaca(ID_Klienta)
        Wszystkie_zajecia = Zajecia.odczyt()
        for ws in Wszystkie_zajecia:
            for li in Lista:
                if ws.ID_Zajecia==li.ID_Zajecia:
                    Wszystkie_zajecia.remove(ws)
        for ws in Wszystkie_zajecia:
            for za in Zajecia_ucz:
                if ws.ID_Zajecia==za.ID_Zajecia:
                    Wszystkie_zajecia.remove(ws)
        if request.method == 'GET':
            try:

                return render_template('widok_klient.html', zajecia=Zajecia_ucz, lista=Lista, wszystkie=Wszystkie_zajecia)
            except NameError as error:
                flash(str(error))
                return render_template('widok_klient.html', zajecia=Zajecia_ucz, lista=Lista, wszystkie=Wszystkie_zajecia)
        if request.method == 'POST':
            try:
                session = create_session(bind=engine)
                q = session.query(Zajecia).filter(Zajecia.Nazwa == request.form["Zaj"])
                rekord = q.one()
                dodaj_klienta_do_zajec(ID_Klienta, rekord.ID_Zajecia)
            except NameError as error:
                flash(str(error))
            finally:
                return redirect(url_for('klient_widok', ID_Klienta=g.user))
    return redirect(url_for('homepage'))

@app.route('/lista/<int:ID_Zajecia>')
def lista(ID_Zajecia):
    usun_lista(g.user, ID_Zajecia)
    return redirect(url_for('klient_widok', ID_Klienta=g.user))

@app.route('/ucz/<int:ID_Zajecia>')
def uczestnicza(ID_Zajecia):
    usun_uczestnicza(g.user, ID_Zajecia)
    return redirect(url_for('klient_widok', ID_Klienta=g.user))


if __name__ == '__main__':
    app.debug = True
    app.run()



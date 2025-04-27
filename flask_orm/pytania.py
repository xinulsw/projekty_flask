from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from .db import db
from .models import Pytanie, Odpowiedz
from .forms import PytanieForm

bp = Blueprint('pytania', __name__, template_folder='pytania')

@bp.route('/')
def index():
    return render_template('pytania/index.html')

@bp.route('/pytania/lista')
def pytania_lista():
    """Pobranie z bazy i wyświetlenie wszystkich pytań"""
    # pytania = db.session.execute(db.select(Pytanie)).scalars()
    pytania = Pytanie.query.all()
    if not pytania:
        flash('Brak pytań!', 'kom')
        return redirect(url_for('pytania.index'))

    return render_template('pytania/pytania_lista.html', pytania=pytania)

@bp.route('/pytania/test', methods=['GET', 'POST'])
def pytania():
    """Wyświetlenie pytań i odpowiedzi w testu oraz ocena poprawności
    przesłanych odpowiedzi"""

    if request.method == 'POST':
        wynik = 0
        for pid, odp in request.form.items():
            odpok = db.session.query(Pytanie.odpok).filter(Pytanie.id == int(pid)).scalar()
            if odp == odpok:
                wynik += 1
        flash(f'Liczba poprawnych odpowiedzi, to: {wynik}', 'sukces')
        return redirect(url_for('pytania.index'))

    # GET, wyświetl pytania i odpowiedzi
    pytania = Pytanie.query.join(Odpowiedz).all()
    if not pytania:
        flash('Brak pytań w bazie.', 'kom')
        return redirect(url_for('index'))
    return render_template('pytania/pytania_pytania.html', pytania=pytania)

def flash_errors(form):
    """Odczytanie wszystkich błędów formularza i przygotowanie komunikatów"""
    for field, errors in form.errors.items():
        for error in errors:
            if type(error) is list:
                error = error[0]
            flash("Błąd: {}. Pole: {}".format(
                error,
                getattr(form, field).label.text))

@bp.route('/dodaj', methods=['GET', 'POST'])
def dodaj_pytanie():
    """Dodawanie pytań i odpowiedzi"""
    form = PytanieForm()
    if form.validate_on_submit():
        odpowiedzi = form.odpowiedzi.data
        p = Pytanie(pytanie=form.pytanie.data, odpok=odpowiedzi[int(form.odpok.data)])
        db.session.add(p)
        db.session.commit()
        for o in odpowiedzi:
            odp = Odpowiedz(pytanie_id=p.id, odpowiedz=o)
            db.session.add(odp)
        db.session.commit()
        flash(f'Dodano pytanie: {form.pytanie.data}')
        return redirect(url_for("pytania.lista"))
    elif request.method == 'POST':
        flash_errors(form)
    return render_template("pytania/pytanie_dodaj.html", form=form, radio=list(form.odpok))

@bp.errorhandler(404)
def page_not_found(e):
    """Zwrócenie szablonu 404.html w przypadku nie odnalezienia strony"""
    return render_template('404.html'), 404


@bp.route('/edytuj/<int:pid>', methods=['GET', 'POST'])
def edytuj(pid):
    """Edycja pytania o identyfikatorze pid i odpowiedzi"""
    p = Pytanie.query.get_or_404(pid)
    form = PytanieForm()

    if form.validate_on_submit():
        odp = form.odpowiedzi.data
        p.pytanie = form.pytanie.data
        p.odpok = odp[int(form.odpok.data)]
        for i, o in enumerate(p.odpowiedzi):
            o.odpowiedz = odp[i]
        db.session.commit()
        flash("Zaktualizowano pytanie: {}".format(form.pytanie.data))
        return redirect(url_for("pytania.lista"))
    elif request.method == 'POST':
        flash_errors(form)

    for i in range(3):
        if p.odpok == p.odpowiedzi[i].odpowiedz:
            p.odpok = i
            break
    form = PytanieForm(obj=p)
    return render_template("pytania/pytanie_edytuj.html", form=form, radio=list(form.odpok))


@bp.route('/usun/<int:pid>', methods=['GET', 'POST'])
def usun(pid):
    """Usunięcie pytania o identyfikatorze pid"""
    p = Pytanie.query.get_or_404(pid)
    if request.method == 'POST':
        db.session.delete(p)
        db.session.commit()
        flash('Usunięto pytanie {0}'.format(p.pytanie), 'sukces')
        return redirect(url_for('pytania.index'))
    return render_template("pytania/pytanie_usun.html", pytanie=p)

from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from flask_login import current_user, login_required
from sqlalchemy import or_

from .db import db
from .kategorie import get_kategorie_user
from .models import Pytanie, Odpowiedz, Kategoria
from .forms import PytanieForm

bp = Blueprint('pytania', __name__, template_folder='pytania')

@bp.route('/')
def index():
    return render_template('pytania/index.html')

# @bp.route('/pytania/lista')
# def pytania_lista():
#     """Pobranie z bazy i wyświetlenie wszystkich pytań"""
#     pytania = db.session.execute(db.select(Pytanie)).scalars()
#     if not pytania:
#         flash('Brak pytań!', 'kom')
#         return redirect(url_for('pytania.index'))
#
#     return render_template('pytania/pytania_lista.html', pytania=pytania)

# def flash_errors(form):
#     """Odczytanie wszystkich błędów formularza i przygotowanie komunikatów"""
#     for field, errors in form.errors.items():
#         for error in errors:
#             if type(error) is list:
#                 error = error[0]
#             flash("Błąd: {}. Pole: {}".format(
#                 error,
#                 getattr(form, field).label.text))

@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def pytanie_dodaj():
    """Dodawanie pytań i odpowiedzi"""
    form = PytanieForm()
    kategorie = get_kategorie_user(current_user.id)
    form.kategoria_id.choices = [(k.id, k.kategoria) for k in kategorie]

    if request.method == 'POST' and form.validate_on_submit():
        pytanie = form.pytanie.data
        odpowiedzi = form.odpowiedzi.data
        kategoria_id = form.kategoria_id.data
        user_id = current_user.id
        p = Pytanie(pytanie=pytanie, kategoria_id=kategoria_id, user_id=user_id)
        db.session.add(p)
        for o in odpowiedzi:
             odp = Odpowiedz(odpowiedz=o['odpowiedz'], poprawna=o['poprawna'])
             p.odpowiedzi.append(odp)
        db.session.commit()
        flash(f'Dodano pytanie: {pytanie}')
        return redirect(url_for('pytania_lista'))

    return render_template('pytania/pytanie_dodaj.html', form=form)


@bp.route('/edytuj/<int:pid>', methods=['GET', 'POST'])
def pytanie_edytuj(pid=None):
    """Edycja pytania o identyfikatorze pid i odpowiedzi"""
    p = db.get_or_404(Pytanie, pid)
    form = PytanieForm(request.form, obj=p)
    kategorie = get_kategorie_user(current_user.id)
    form.kategoria_id.choices = [(k.id, k.kategoria) for k in kategorie]
    form.kategoria_id.data = p.kategoria_id

    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash(f"Zaktualizowano pytanie: {form.pytanie.data}")
        return redirect(url_for("pytania_lista"))

    odpowiedzi = []
    for i, o in enumerate(p.odpowiedzi):
        odpowiedzi.append({'odpowiedz': o.odpowiedz, 'poprawna': o.poprawna})
        form.odpowiedzi.pop_entry()
    for o in odpowiedzi:
        form.odpowiedzi.append_entry(o)

    return render_template("pytania/pytanie_edytuj.html", form=form)


@bp.route('/usun/<int:pid>', methods=['GET', 'POST'])
def pytanie_usun(pid):
    """Usunięcie pytania o identyfikatorze pid"""
    p = db.get_or_404(Pytanie, pid)
    if request.method == 'POST':
        db.session.delete(p)
        db.session.commit()
        flash('Usunięto pytanie {0}'.format(p.pytanie), 'sukces')
        return redirect(url_for('pytania.index'))
    return render_template("pytania/pytanie_usun.html", pytanie=p)


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
    lista_pytan = Pytanie.query.join(Odpowiedz).all()
    if not lista_pytan:
        flash('Brak pytań w bazie.', 'kom')
        return redirect(url_for('index'))
    return render_template('pytania/pytania_pytania.html', pytania=pytania)

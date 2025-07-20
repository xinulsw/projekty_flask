from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from flask_login import current_user, login_required
from .db import db
from .kategorie import get_kategorie_user
from .models import Pytanie, Odpowiedz, Kategoria, Test
from .forms import TestForm, MultiCheckboxField

bp = Blueprint('testy', __name__, template_folder='testy')

@bp.route('/')
def index():
    testy = db.session.execute(
        db.select(Test, Kategoria).join(Test.kategoria).where(
            Test.user_id == current_user.id)).scalars().all()
    kategorie = get_kategorie_user()
    return render_template('testy/index.html', items=testy, kategorie=kategorie)

@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def dodaj():
    """Tworzenie testów"""
    form = TestForm()
    kategorie = get_kategorie_user()
    form.kategoria_id.choices = [(k.id, k.kategoria) for k in kategorie]
    pytania = db.session.execute(
        db.select(Pytanie.id, Pytanie.pytanie).join(Pytanie.user)
    ).scalars().all()
    for p in pytania:
        print(p)
    if request.method == 'POST':
        pass
        return redirect(url_for('testy_lista'))

    return render_template('testy/test_dodaj.html', form=form)


@bp.route('/edytuj/<int:t_id>', methods=['GET', 'POST'])
def test_edytuj(t_id=None):
    """Edycja testów"""

    if request.method == 'POST':
        pass
        flash(f"Zaktualizowano pytanie: {form.pytanie.data}")
        return redirect(url_for("pytania.index"))

    return render_template("testy/test_edytuj.html", form=form)


@bp.route('/usun/<int:t_id>', methods=['GET', 'POST'])
def test_usun(t_id=None):
    """Usunięcie pytania o identyfikatorze t_id"""
    t = db.get_or_404(Test, t_id)
    if request.method == 'POST':
        pass
        return redirect(url_for('pytania.index'))
    return render_template("testy/test_usun.html", test=t)


@bp.route('/kategoria/<int:k_id>', methods=['GET', 'POST'])
def kategoria(k_id=None):
    """Wyświetlenie pytań i odpowiedzi w testu oraz ocena poprawności
    przesłanych odpowiedzi"""
    # from werkzeug.datastructures import MultiDict
    pytania_all = db.session.execute(db.select(Pytanie).filter(Pytanie.kategoria_id == int(k_id))).scalars().all()
    # data = {'pytania': pytania_all}
    #form = InputGridTableForm(request.form, data=MultiDict(data))
    #print(MultiDict(data))
    for p in pytania_all:
        print(p)

    # print(form.data)
    if request.method == 'POST':
        print(request.form)
        wynik = 0
        # for t_id, odp in request.form.items():
        #     odpok = db.session.query(Pytanie.odpok).filter(Pytanie.id == int(t_id)).scalar()
        #     if odp == odpok:
        #         wynik += 1
        # flash(f'Liczba poprawnych odpowiedzi, to: {wynik}', 'sukces')
        # return redirect(url_for('pytania.index'))

    # GET, wyświetl pytania i odpowiedzi
    # lista_pytan = Pytanie.query.join(Odpowiedz).all()
    odpowiedzi = []
    for p in pytania_all:
        # db.session.execute(db.select(Odpowiedz)).scalars().all()
        odpowiedzi.append(p.odpowiedzi)
        # print(p.odpowiedzi)
    print(pytania_all)
    return render_template('testy/test_kategoria.html', pytania=pytania_all, odpowiedzi=odpowiedzi)

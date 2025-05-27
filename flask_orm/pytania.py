from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from flask_login import current_user, login_required
from .db import db
from .kategorie import get_kategorie_user
from .models import Pytanie, Odpowiedz, Kategoria
from .forms import PytanieForm, TestForm

bp = Blueprint('pytania', __name__, template_folder='pytania')

@bp.route('/')
def index():
    pytania = db.session.execute(
        db.select(Pytanie, Kategoria).join(Pytanie.kategoria).where(
            Pytanie.user_id == current_user.id)).scalars().all()
    kategorie = db.session.execute(db.select(Kategoria)).scalars().all()
    return render_template('pytania/index.html', items=pytania, kategorie=kategorie)

@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def pytanie_dodaj():
    """Dodawanie pytań i odpowiedzi"""
    form = PytanieForm()
    kategorie = get_kategorie_user()
    form.kategoria_id.choices = [(k.id, k.kategoria) for k in kategorie]

    if request.method == 'POST' and form.validate_on_submit():
        pytanie = form.pytanie.data
        l_poprawnych_odp = form.l_poprawnych_odp.data
        odpowiedzi = form.odpowiedzi.data
        kategoria_id = form.kategoria_id.data
        user_id = current_user.id
        p = Pytanie(pytanie=pytanie, l_poprawnych_odp=l_poprawnych_odp, kategoria_id=kategoria_id, user_id=user_id)
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

    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash(f"Zaktualizowano pytanie: {form.pytanie.data}")
        return redirect(url_for("pytania.index"))

    form.kategoria_id.data = p.kategoria_id
    odpowiedzi = []
    for i, o in enumerate(p.odpowiedzi):
        odpowiedzi.append({'odpowiedz': o.odpowiedz, 'poprawna': o.poprawna})
        form.odpowiedzi.pop_entry()
    for o in odpowiedzi:
        form.odpowiedzi.append_entry(o)

    return render_template("pytania/pytanie_edytuj.html", form=form)


@bp.route('/usun/<int:pid>', methods=['GET', 'POST'])
def pytanie_usun(pid=None):
    """Usunięcie pytania o identyfikatorze pid"""
    p = db.get_or_404(Pytanie, pid)
    if request.method == 'POST':
        db.session.delete(p)
        db.session.commit()
        flash('Usunięto pytanie {0}'.format(p.pytanie), 'sukces')
        return redirect(url_for('pytania.index'))
    return render_template("pytania/pytanie_usun.html", pytanie=p)


@bp.route('/test/<int:kid>', methods=['GET', 'POST'])
def test(kid=None):
    """Wyświetlenie pytań i odpowiedzi w testu oraz ocena poprawności
    przesłanych odpowiedzi"""
    from werkzeug.datastructures import MultiDict
    pytania_all = db.session.execute(db.select(Pytanie).filter(Pytanie.kategoria_id == int(kid))).scalars().all()
    data = {'pytania': pytania_all}
    #form = InputGridTableForm(request.form, data=MultiDict(data))
    #print(MultiDict(data))
    for p in pytania_all:
        print(p)
    form = TestForm(request.form, data=data)
    print(form.data)
    if request.method == 'POST':
        print(request.form)
        wynik = 0
        # for pid, odp in request.form.items():
        #     odpok = db.session.query(Pytanie.odpok).filter(Pytanie.id == int(pid)).scalar()
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
    print(odpowiedzi)
    return render_template('pytania/pytania_test_form.html', pytania=form, odpowiedzi=odpowiedzi)

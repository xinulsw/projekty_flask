from flask import (
    Blueprint, flash, g, render_template, request, redirect, url_for
)
from db import Kategoria, Pytanie, Odpowiedz
from forms import *

bp = Blueprint('quiz', __name__, template_folder='templates', url_prefix='/quiz')

@bp.route('/')
def index():
    """Pobranie wszystkich pytań z bazy i zwrócenie szablonu z listą pytań"""
    pytania = Pytanie().select().join(Kategoria)
    if not pytania.count():
        flash('Brak pytań w bazie.', 'kom')
        return redirect(url_for('index'))

    return render_template('quiz/index.html', pytania=pytania)

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
def dodaj():
    """Dodawanie pytań i odpowiedzi"""
    form = PytanieForm()
    if form.validate_on_submit():
        p = Pytanie(tresc=form.pytanie.data)
        p.save()
        odp = form.odpowiedzi.data
        for o in odp:
            inst = Odpowiedz(pnr=p.id, odpowiedz=o)
            inst.save()
        flash("Dodano pytanie: {}".format(form.pytanie.data))
        return redirect(url_for("lista"))
    elif request.method == 'POST':
        flash_errors(form)

    return render_template("quiz/dodaj.html", form=form, radio=list(form.odpok))
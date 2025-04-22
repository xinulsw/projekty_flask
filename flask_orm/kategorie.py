from flask import (
    Blueprint, flash, g, render_template, request, redirect, url_for
)
from .db import db
from .models import Kategoria
from .forms import KategoriaForm

bp = Blueprint('pytania', __name__, template_folder='pytania', url_prefix='/pytania')

@bp.route('/')
def index():
    return render_template('pytania/index.html')

@bp.route('/kategorie/lista')
def kategorie_lista():
    """Pobranie z bazy i wyświetlenie wszystkich pytań"""
    # pytania = db.session.execute(db.select(Pytanie)).scalars()
    pytania = Pytanie.query.all()
    if not pytania:
        flash('Brak pytań!', 'kom')
        return redirect(url_for('pytania.index'))

    return render_template('pytania/pytania_lista.html', pytania=pytania)

@bp.route('/kategorie/dodaj')
def kategoria_dodaj():
    pass

@bp.route('/kategorie/edytuj')
def kategoria_edytuj():
    pass

@bp.route('/kategorie/usun')
def kategoria_usun():
    pass
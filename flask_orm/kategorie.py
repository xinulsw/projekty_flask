from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
import flask_orm
from .views import ListView
from .models import Kategoria
from .forms import KategoriaForm

bp = Blueprint('kategorie', __name__, template_folder='kategorie')

# @bp.route('/')
# def index():
#     kategorie = Kategoria.query.all()
#     if not kategorie:
#         flash('Brak kategorii!', 'kom')
#         return redirect(url_for('kategorie.index'))
#
#     return render_template('kategorie/index.html', kategorie=kategorie)

@bp.route('/kategorie/dodaj')
def kategoria_dodaj():
    pass

@bp.route('/kategorie/edytuj')
def kategoria_edytuj():
    pass

@bp.route('/kategorie/usun')
def kategoria_usun():
    pass
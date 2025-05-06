from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from flask_login import login_required, current_user
from .db import db
from .models import User, Kategoria
from .forms import KategoriaForm

bp = Blueprint('kategorie', __name__, template_folder='kategorie')

@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def kategoria_dodaj():
    form = KategoriaForm()
    if form.validate_on_submit():
        kat = form.kategoria.data
        user = db.session.execute(db.select(User).filter_by(id=current_user.id)).scalar_one()
        kategoria = Kategoria(kategoria=kat, user=user)
        db.session.add(kategoria)
        db.session.commit()
        return redirect(url_for('kategorie_lista'))

    return render_template('kategorie/kategoria_dodaj.html', form=form)

@bp.route('/edytuj/<int:id>', methods=['GET', 'POST'])
@login_required
def kategoria_edytuj(id):
    kat = db.session.execute(db.select(Kategoria).filter_by(id=id)).scalar_one()
    form = KategoriaForm(request.form, obj=kat)
    if form.validate_on_submit():
        form.populate_obj(kat)
        db.session.commit()
        return redirect(url_for('kategorie_lista'))

    return render_template('kategorie/kategoria_edytuj.html', form=form)

@bp.route('/usun/<int:id>', methods=['GET', 'POST'])
@login_required
def kategoria_usun(id):
    kat = db.session.execute(db.select(Kategoria).filter_by(id=id)).scalar_one()
    form = KategoriaForm(request.form, obj=kat)
    if form.delete.data:
        db.session.delete(kat)
        db.session.commit()
        flash(f'Usunięto kategorię {form.kategoria.data}', 'sukces')
        return redirect(url_for('kategorie_lista'))
    return render_template('kategorie/kategoria_usun.html', form=form)

# @bp.route('/')
# def index():
#     kategorie = Kategoria.query.all()
#     if not kategorie:
#         flash('Brak kategorii!', 'kom')
#         return redirect(url_for('kategorie.index'))
#
#     return render_template('kategorie/index.html', kategorie=kategorie)
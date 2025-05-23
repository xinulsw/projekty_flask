from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from flask_login import login_required, current_user
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .db import db
from .models import User, Kategoria
from .forms import KategoriaForm

bp = Blueprint('kategorie', __name__, template_folder='kategorie')

@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def kategoria_dodaj():
    form = KategoriaForm()
    if form.validate_on_submit():
        error = False
        try:
            kat = form.kategoria.data
            user = db.session.execute(db.select(User).filter_by(id=current_user.id)).scalar_one()
            kategoria = Kategoria(kategoria=kat, user=user)
            db.session.add(kategoria)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Podana kategoria jest już w bazie!')
            error = True
        if not error:
            return redirect(url_for('kategorie_lista'))

    return render_template('kategorie/kategoria_dodaj.html', form=form, subtitle='Dodaj kategorię')

@bp.route('/edytuj/<int:id>', methods=['GET', 'POST'])
@login_required
def kategoria_edytuj(id):
    kat = db.session.execute(db.select(Kategoria).filter_by(id=id)).scalar_one()
    form = KategoriaForm(request.form, obj=kat)
    if form.validate_on_submit():
        form.populate_obj(kat)
        db.session.commit()
        return redirect(url_for('kategorie_lista'))

    return render_template('kategorie/kategoria_edytuj.html', form=form, subtitle='Edytuj kategorię')

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

def get_kategorie_user(user_id=None):
    if user_id:
        kategorie = db.session.execute(
            db.select(Kategoria).where(
                or_(Kategoria.user_id == 1, Kategoria.user_id == user_id)
            )).scalars().all()
    else:
        kategorie = db.session.execute(db.select(Kategoria)).scalars().all()
    return kategorie

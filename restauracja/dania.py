from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from werkzeug.exceptions import abort
from db import get_db

bp = Blueprint('dania', __name__, url_prefix='/dania')


@bp.route('/lista')
def lista():
    dane = get_db().execute('SELECT * FROM dania').fetchall()
    if not dane:
        flash('Brak dań!')
    return render_template('dania_lista.html', dane=dane)


@bp.route('/dodaj', methods=['GET', 'POST'])
def dodaj():
    if request.method == 'POST':
        nazwa = request.form['nazwa'].strip()
        cena = request.form['cena'].strip()
        menu = 0
        if 'menu' in request.form:
            menu = 1
        db = get_db()
        db.execute('INSERT INTO dania VALUES (?, ?, ?, ?)', [None, nazwa, cena, menu])
        db.commit()
        flash(f'Dodano danie: {nazwa}')
        return redirect(url_for('dania.lista'))

    return render_template('danie_dodaj.html')


def get_danie(d_id):
    db = get_db()
    danie = db.execute('SELECT * FROM dania WHERE id = ?', [d_id]).fetchone()
    if danie is None:
        abort(404, f"Danie o id {d_id} nie istnieje.")
    return danie


@bp.route('/<int:d_id>/edytuj', methods=['GET', 'POST'])
def edytuj(d_id):
    rekord = get_danie(d_id)
    if request.method == 'POST':
        nazwa = request.form['nazwa'].strip()
        cena = request.form['cena'].strip()
        menu = 0
        if 'menu' in request.form:
            menu = 1
        db = get_db()
        db.execute('UPDATE dania SET nazwa = ?, cena = ?, menu = ? WHERE id = ?', [nazwa, cena, menu, d_id])
        db.commit()
        flash(f'Zaktualizowano danie id {d_id} {nazwa}.')
        return redirect(url_for('dania.lista'))

    return render_template('danie_edytuj.html', rekord=rekord)


@bp.route('/<int:d_id>/usun', methods=['GET', 'POST'])
def usun(d_id):
    rekord = get_danie(d_id)
    if request.method == 'POST':
        db = get_db()
        db.execute('DELETE FROM dania WHERE id = ?', [d_id])
        db.commit()
        flash(f'Usunięto danie id {d_id} {rekord["nazwa"]}')
        return redirect(url_for('dania.lista'))

    return render_template("danie_usun.html", rekord=rekord)

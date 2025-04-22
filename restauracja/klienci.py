from flask import (
   Blueprint, flash, render_template, request, redirect, url_for
)
from db import get_db
from werkzeug.exceptions import abort

bp = Blueprint('klienci', __name__, url_prefix='/klienci')


@bp.route('/lista')
def lista():
    dane = get_db().execute('SELECT * FROM klienci').fetchall()
    if not dane:
        flash('Brak klientów!')
    return render_template('klienci_lista.html', dane=dane)


@bp.route('/dodaj', methods=['GET', 'POST'])
def dodaj():
    if request.method == 'POST':
        imie = request.form['imie'].strip()
        nazwisko = request.form['nazwisko'].strip()
        db = get_db()
        db.execute('INSERT INTO klienci VALUES (?, ?, ?)', [None, imie, nazwisko])
        db.commit()
        flash(f'Dodano klienta: {imie} {nazwisko}.')
        return redirect(url_for('klienci.lista'))

    return render_template('klient_dodaj.html')


def get_klient(k_id):
    db = get_db()
    klient = db.execute('SELECT * FROM klienci WHERE id = ?', [k_id]).fetchone()
    if klient is None:
        abort(404, f"Klient o id {k_id} nie istnieje.")
    return klient


@bp.route('/<int:k_id>/edytuj', methods=['GET', 'POST'])
def edytuj(k_id):
    rekord = get_klient(k_id)
    if request.method == 'POST':
        imie = request.form['imie'].strip()
        nazwisko = request.form['nazwisko'].strip()
        db = get_db()
        db.execute('UPDATE klienci SET imie = ?, nazwisko = ? WHERE id = ?', [imie, nazwisko, k_id])
        db.commit()
        flash(f'Zaktualizowano dane klienta id {k_id} {imie} {nazwisko}.')
        return redirect(url_for('klienci.lista'))

    return render_template('klient_edytuj.html', rekord=rekord)


@bp.route('/usun/<int:k_id>', methods=['GET', 'POST'])
def usun(k_id):
    rekord = get_klient(k_id)
    if request.method == 'POST':
        db = get_db()
        db.execute('DELETE FROM klienci WHERE id = ?', [k_id])
        db.commit()
        flash(f'Usunięto klienta {k_id} {rekord["imie"]} {rekord["nazwisko"]}!')
        return redirect(url_for('klienci.lista'))

    return render_template("klient_usun.html", rekord=rekord)

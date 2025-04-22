from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from db import get_db
from werkzeug.exceptions import abort
from datetime import datetime

bp = Blueprint('zamowienia', __name__, url_prefix='/zamowienia')


@bp.route('/lista')
def lista():
    dane = get_db().execute("""
        SELECT z.*, k.* FROM zamowienia z
        INNER JOIN klienci k ON z.id_klienta = k.id
        ORDER BY z.data
        """).fetchall()
    if not dane:
        flash('Brak zamówień!')
    return render_template('zamowienia_lista.html', dane=dane)


@bp.route('/dodaj', methods=['GET', 'POST'])
def dodaj():
    db = get_db().cursor()
    if request.method == 'POST':
        if not request.form.getlist('dania'):
            flash("Nie wybrano dań!")
        else:
            id_klienta = request.form['klient']
            data = datetime.strptime(request.form['data'], '%Y-%m-%dT%H:%M')
            rabat = request.form['rabat']

            db.execute('INSERT INTO zamowienia VALUES (?, ?, ?, ?)',
                       [None, id_klienta, data, rabat])
            z_id = db.lastrowid
            for d_id in request.form.getlist('dania'):
                liczba = request.form[f'liczba{d_id}']
                db.execute('INSERT INTO sklady_zamowien VALUES (?, ?, ?, ?)',
                           [None, z_id, d_id, liczba])
            db.execute('COMMIT')
            flash(f'Dodano dane zamówienia id {z_id}.')

        return redirect(url_for('zamowienia.lista'))

    klienci = db.execute('SELECT * FROM klienci').fetchall()
    dania = db.execute('SELECT * FROM dania WHERE menu IS TRUE').fetchall()
    dzis = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('zamowienie_dodaj.html', klienci=klienci, dania=dania, dzis=dzis)


def get_zamowienie(z_id):
    db = get_db()
    zamowienie = db.execute("""
        SELECT z.*, k.* FROM zamowienia z
        INNER JOIN klienci k ON z.id_klienta = k.id
        WHERE z.id = ?
        """, [z_id]).fetchone()

    if zamowienie is None:
        abort(404, f"Zamówienie o id {z_id} nie istnieje.")
    return zamowienie


@bp.route('/<int:z_id>/edytuj', methods=['GET', 'POST'])
def edytuj(z_id):
    dane = get_zamowienie(z_id)
    db = get_db()
    if request.method == 'POST':
        if not request.form.getlist('dania'):
            flash("Nie wybrano dań!")
        else:
            data = datetime.strptime(request.form['data'], '%Y-%m-%dT%H:%M')
            rabat = request.form['rabat']
            db.execute('UPDATE zamowienia SET data = ?, rabat = ? WHERE id = ?', [data, rabat, z_id])

            dania_z = [row[0] for row in db.execute("""
                SELECT id_dania FROM sklady_zamowien WHERE id_zamowienia = ?
                """, [z_id])]
            dania = [int(d_id) for d_id in request.form.getlist('dania')]

            for d_id in dania:
                liczba = request.form[f'liczba{d_id}']
                if d_id in dania_z:
                    db.execute(
                        'UPDATE sklady_zamowien SET liczba = ?'
                        'WHERE id_zamowienia = ? AND id_dania = ?', [liczba, z_id, d_id])
                else:
                    db.execute('INSERT INTO sklady_zamowien VALUES (?, ?, ?, ?)', [None, z_id, d_id, liczba])
            for d_id in set(dania_z) - set(dania):
                db.execute('DELETE FROM sklady_zamowien WHERE id_zamowienia = ? AND id_dania = ?',
                           [z_id, d_id])

            db.commit()

            flash(f'Zaktualizowano dane zamówienia id {z_id}.')

        return redirect(url_for('zamowienia.lista'))

    dania = db.execute('SELECT * FROM dania WHERE menu IS TRUE').fetchall()
    dania_zamowione = db.execute("""
        SELECT s_z.liczba, d.* FROM sklady_zamowien s_z
        INNER JOIN zamowienia z ON s_z.id_zamowienia = z.id
        INNER JOIN dania d ON s_z.id_dania = d.id
        WHERE z.id = ?
        """, [z_id]).fetchall()
    dania_id = [row[1] for row in dania_zamowione]
    dania = [row for row in dania if row['id'] not in dania_id]

    return render_template('zamowienie_edytuj.html', rekord=dane, dania=dania, dania_z=dania_zamowione)


@bp.route('/<int:z_id>/usun', methods=['GET', 'POST'])
def usun(z_id):
    dane = get_zamowienie(z_id)
    if request.method == 'POST':
        db = get_db()
        db.execute('PRAGMA foreign_keys=on')
        db.execute('DELETE FROM zamowienia WHERE id = ?', [z_id])
        db.commit()
        flash(f'Usunięto zamówienie {dane["imie"]} {dane["nazwisko"]}, {dane["data"]}!')
        return redirect(url_for('zamowienia.lista'))
    return render_template("zamowienie_usun.html", rekord=dane)

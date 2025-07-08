from flask import Blueprint, render_template, request, session, flash, redirect, url_for, g, abort
from db import query_db, get_db
from users import login_required

bp = Blueprint('czat', __name__, template_folder='templates', url_prefix='/czat')

@bp.route('/')
def index():
    sql = 'SELECT w.*, u.nick FROM wiadomosc w INNER JOIN user u on u.id = w.user_id ORDER BY data_dodania DESC'
    wiadomosci = query_db(sql)
    return render_template('czat/wiadomosc_lista.html', wiadomosci=wiadomosci)


@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def dodaj():
    wiadomosc = None
    if request.method == 'POST':
        wiadomosc = request.form['wiadomosc'].strip()
        db = get_db()
        try:
            db.execute('INSERT INTO wiadomosc (user_id, wiadomosc) VALUES (?, ?)',
                       [g.user['id'], wiadomosc])
            db.commit()
        except db.IntegrityError:
            flash(f'Błędne dane!')
        else:
            flash(f'Dodano wiadomosc {wiadomosc}')
            return redirect(url_for('czat.index'))

    return render_template('czat/wiadomosc_dodaj.html', akcja='Zapisz', wiadomosc=wiadomosc)


def get_wiadomosc(obj_id, autor=True):
    sql = """SELECT w.id, w.wiadomosc, w.data_dodania, w.user_id, u.nick
             FROM wiadomosc w INNER JOIN user u ON w.user_id = u.id
             WHERE w.id=?
          """
    obj = query_db(sql, [obj_id], one=True)
    if obj is None:
        abort(404, f'Obiekt o identyfikatorze {obj_id} nie istnieje.')
    if autor and obj['user_id'] != g.user['id']:
        return False
    return obj


@bp.route('/edytuj/<int:w_id>', methods=['GET', 'POST'])
@login_required
def edytuj(w_id):
    wiadomosc = get_wiadomosc(w_id)

    if request.method == 'POST':
        print(request.form)
        wiadomosc = request.form['wiadomosc'].strip()
        db = get_db()
        try:
            db.execute('UPDATE wiadomosc SET wiadomosc = ? WHERE id = ?',
                       [wiadomosc, w_id])
            db.commit()
        except db.IntegrityError:
            flash(f'Błędne dane!')
        else:
            flash(f'Zmieniono wiadomość: {wiadomosc}')
            return redirect(url_for('czat.index'))

    return render_template('czat/wiadomosc_edytuj.html', akcja='Zapisz', wiadomosc=wiadomosc)


@bp.route('/usun', methods=['GET', 'POST'])
# @login_required
def usun():
    obj_id = int(request.form['w_id'])
    if not get_wiadomosc(obj_id):
        flash('Nie jesteś autorem tej wiadomości!')
        return redirect(url_for('czat.index'))
    db = get_db()
    db.execute('DELETE FROM wiadomosc WHERE id=? AND user_id=?',
               [obj_id, g.user['id']])
    db.commit()
    flash('Usunięto wiadomość.')
    return redirect(url_for('czat.index'))

from flask import Blueprint, render_template, request, session, flash, redirect, url_for, g
from db import query_db, get_db
from users import login_required

bp = Blueprint('czat', __name__, template_folder='templates', url_prefix='/czat')

@bp.route('/')
def index():
    sql = 'SELECT * FROM wiadomosc ORDER BY data_dodania DESC'
    wiadomosci = query_db(sql)
    return render_template('czat/lista_wiadomosci.html', wiadomosci=wiadomosci)


@bp.route('/dodaj', methods=['GET', 'POST'])
# @login_required
def dodaj():
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

    return render_template('czat/wiadomosc_dodaj.html', akcja='Zapisz')

@bp.route('/usun', methods=['POST'])
# @login_required
def usun():
    id_z = request.form['id']
    db = get_db()
    db.execute('DELETE FROM wiadomosc WHERE id=? AND user_id=?',
               [id_z,g.user['id']])
    db.commit()
    flash('Usunięto wiadomość.')
    return redirect(url_for('czat.index'))

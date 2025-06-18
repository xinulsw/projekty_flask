from flask import Blueprint, render_template, request, flash, redirect, url_for, g
from db import query_db, get_db
from users import login_required

bp = Blueprint('zadania', __name__, template_folder='templates', url_prefix='/zadania')

@bp.route('/')
def index():
    sql = 'SELECT * FROM zadanie WHERE user_id=? ORDER BY data_dodania DESC'
    zadania = query_db(sql, [g.user['id']])
    return render_template('zadania/zadanie_lista.html', zadania=zadania)


@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def dodaj():
    if request.method == 'POST':
        zadanie = request.form['zadanie'].strip()
        db = get_db()
        try:
            db.execute('INSERT INTO zadanie (user_id, zadanie) VALUES (?, ?)',
                       [g.user['id'], zadanie])
            db.commit()
        except db.IntegrityError:
            flash(f'Błędne dane!')
        else:
            flash(f'Dodano zadanie {zadanie}')
            return redirect(url_for('zadania.index'))

    return render_template('zadania/zadanie_dodaj.html', akcja='Zapisz')

@bp.route('/edytuj/<int:zid>', methods=['GET', 'POST'])
@login_required
def edytuj(zid):
    zadanie = query_db('SELECT * FROM zadanie WHERE id = ?', [zid], one=True)
    return

@bp.route('/usun', methods=['POST'])
@login_required
def usun():
    id_z = request.form['id']
    db = get_db()
    db.execute('DELETE FROM zadanie WHERE id=? AND user_id=?',
               [id_z,g.user['id']])
    db.commit()
    flash('Usunięto zadanie.')
    return redirect(url_for('zadania.index'))

@bp.route('/zrobione', methods=['POST'])
@login_required
def zrobione():
    id_z = request.form['id']
    db = get_db()
    db.execute('UPDATE zadanie SET zrobione=1 WHERE id=? AND user_id=?',
               [id_z,g.user['id']])
    db.commit()
    flash('Zmieniono status zadania.')
    return redirect(url_for('zadania.index'))

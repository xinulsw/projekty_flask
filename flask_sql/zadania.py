from flask import Blueprint, render_template, request, flash, redirect, url_for, g, abort
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
    zadanie = None
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

    return render_template('zadania/zadanie_dodaj.html', akcja='Zapisz', zadanie=zadanie)


def get_zadanie(obj_id, autor=True):
    sql = """SELECT z.id, z.zadanie, z.zrobione, z.data_dodania, z.user_id, u.nick
             FROM zadanie z INNER JOIN user u ON z.user_id = u.id
             WHERE z.id=?
          """
    obj = query_db(sql, [obj_id], one=True)
    if obj is None:
        abort(404, f'Obiekt o identyfikatorze {obj_id} nie istnieje.')
    if autor and obj['user_id'] != g.user['id']:
        abort(403)
    return obj


@bp.route('/edytuj/<int:z_id>', methods=['GET', 'POST'])
@login_required
def edytuj(z_id):
    zadanie = get_zadanie(z_id)

    if request.method == 'POST':
        print(request.form)
        zadanie = request.form['zadanie'].strip()
        zrobione = True if 'zrobione' in request.form else False
        db = get_db()
        try:
            db.execute('UPDATE zadanie SET zadanie = ?, zrobione = ? WHERE id = ?',
                       [zadanie, zrobione, z_id])
            db.commit()
        except db.IntegrityError:
            flash(f'Błędne dane!')
        else:
            flash(f'Zmieniono zadanie: {zadanie}')
            return redirect(url_for('zadania.index'))

    return render_template('zadania/zadanie_edytuj.html', akcja='Zapisz', zadanie=zadanie)


@bp.route('/usun/<int:z_id>', methods=['POST',])
@login_required
def usun(z_id):
    zadanie = get_zadanie(z_id)
    db = get_db()
    db.execute('DELETE FROM zadanie WHERE id=?', [z_id])
    db.commit()
    flash(f'Usunięto zadanie: {zadanie['zadanie']}.')
    return redirect(url_for('zadania.index'))


@bp.route('/zrobione', methods=['POST'])
@login_required
def zrobione():
    id_z = request.form['z_id']
    db = get_db()
    db.execute('UPDATE zadanie SET zrobione=1 WHERE id=? AND user_id=?',
               [id_z,g.user['id']])
    db.commit()
    flash('Zmieniono status zadania.')
    return redirect(url_for('zadania.index'))

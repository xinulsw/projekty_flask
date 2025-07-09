from flask import Blueprint, render_template, request, flash, redirect, url_for, g, abort
from db import query_db, get_db
from users import login_required

bp = Blueprint('pytania', __name__, template_folder='pytania', url_prefix='/pytania')


@bp.route('/')
def index():
    sql = 'SELECT * FROM pytanie'
    pytania = query_db(sql)
    return render_template('pytania/pytanie_lista.html', pytania=pytania)


@bp.route('/dodaj', methods=['GET', 'POST'])
def dodaj():
    pytanie_form = {'pytanie':'','odpowiedzi':[], 'poprawne':[]}
    errors = []

    if request.method == 'POST':
        pytanie = request.form['pytanie'].strip()
        if not pytanie:
            errors.append('Nie wpisano pytania!')
        else:
            pytanie_form['pytanie'] = pytanie

        odpowiedzi = request.form.getlist('odpowiedzi')
        for i, o in enumerate(odpowiedzi):
            if not o.strip():
                errors.append(f'Nie wpisano odpowiedzi {i+1}!')
            else:
                odpowiedzi[i] = o.strip()

        poprawne = request.form.getlist('poprawne')
        if not len(poprawne):
            errors.append('Nie zaznaczono przynajmniej jednej poprawnej odpowiedzi!')
        else:
            pytanie_form['poprawne'] = poprawne

        if not errors:
            db = get_db()
            sql = 'INSERT INTO pytanie VALUES (?, ?, ?)'
            cur = db.execute(sql, [None, g.user['id'], pytanie])
            pid = cur.lastrowid
            for i, odp in enumerate(odpowiedzi, start=1):
                poprawna = True if str(i) in poprawne else False
                sql = 'INSERT INTO odpowiedz VALUES (?, ?, ?, ?)'
                db.execute(sql, [None, pid, odp, poprawna])
            db.commit()
            flash(f'Dodano pytanie: {pytanie}')
            return redirect(url_for('pytania.index'))

        pytanie_form['odpowiedzi'] = odpowiedzi
    return render_template('pytania/pytanie_dodaj.html', errors=errors, pytanie_form=pytanie_form)


def get_pytanie(obj_id, autor=True):
    sql = 'SELECT p.* FROM pytanie p WHERE id = ?'
    obj = query_db(sql, [obj_id], one=True)
    if obj is None:
        abort(404, f'Obiekt o identyfikatorze {obj_id} nie istnieje.')
    if autor and obj['user_id'] != g.user['id']:
        return False
    sql = 'SELECT o.id, o.odpowiedz, o.poprawna FROM odpowiedz o WHERE pytanie_id = ?'
    odpowiedzi = query_db(sql, [obj_id])
    return obj, odpowiedzi


@bp.route('/edytuj/<int:p_id>', methods=['GET', 'POST'])
@login_required
def edytuj(p_id):
    pytanie, odpowiedzi = get_pytanie(p_id)
    pytanie_form = {'id': p_id, 'pytanie': pytanie['pytanie'], 'odpowiedzi': [], 'poprawne': []}
    odp_ids = []
    for i, odp in enumerate(odpowiedzi, start=1):
        odp_ids.append(odp['id'])
        pytanie_form['odpowiedzi'].append(odp['odpowiedz'])
        if odp['poprawna']:
            pytanie_form['poprawne'].append(str(i))

    errors = []
    if request.method == 'POST':
        pytanie = request.form['pytanie'].strip()
        if not pytanie:
            errors.append('Nie wpisano pytania!')
        else:
            pytanie_form['pytanie'] = pytanie

        odpowiedzi = request.form.getlist('odpowiedzi')
        for i, o in enumerate(odpowiedzi):
            if not o.strip():
                errors.append(f'Nie wpisano odpowiedzi {i+1}!')
            else:
                odpowiedzi[i] = o.strip()

        poprawne = request.form.getlist('poprawne')
        if not len(poprawne):
            errors.append('Nie zaznaczono przynajmniej jednej poprawnej odpowiedzi!')
        else:
            pytanie_form['poprawne'] = poprawne

        if not errors:
            db = get_db()
            sql = 'UPDATE pytanie SET pytanie = ? WHERE id = ?'
            db.execute(sql, [pytanie, p_id])
            for i, odp in enumerate(odpowiedzi, start=1):
                poprawna = True if str(i) in poprawne else False
                sql = 'UPDATE odpowiedz SET odpowiedz = ?, poprawna = ? WHERE id = ?'
                db.execute(sql, [odp, poprawna, odp_ids[i-1]])
            db.commit()
            flash(f'Zaktualizowano pytanie: {pytanie}')
            return redirect(url_for('pytania.index'))

    return render_template('pytania/pytanie_edytuj.html',
                           errors=errors, pytanie_form=pytanie_form)


@bp.route('/usun/<int:p_id>', methods=['POST'])
@login_required
def usun(p_id):
    pytanie, odpowiedzi = get_pytanie(p_id)
    db = get_db()
    db.execute('PRAGMA foreign_keys = 1')
    db.execute('DELETE FROM pytanie WHERE id=?', [p_id])
    db.commit()
    flash(f'Usunięto zadanie: {pytanie['pytanie']}.')
    return redirect(url_for('pytania.index'))

# sql = 'SELECT p.*, o.* FROM pytanie p INNER JOIN odpowiedz o WHERE p.id=o.pytanie_id'

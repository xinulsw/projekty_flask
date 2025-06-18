from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)
from db import query_db, get_db


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

        if not errors:
            db = get_db()
            sql = 'INSERT INTO pytanie VALUES (?, ?)'
            cur = db.execute(sql, [None, pytanie])
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

# sql = 'SELECT p.*, o.* FROM pytanie p INNER JOIN odpowiedz o WHERE p.id=o.pytanie_id'

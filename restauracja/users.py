import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/zaloguj', methods=['GET', 'POST'])
def zaloguj():
    if request.method == 'POST':
        nick = request.form['nick'].strip()
        haslo = request.form['haslo'].strip()

        db = get_db()
        error = None

        user = db.execute('SELECT * FROM users WHERE nick = ?', [nick]).fetchone()

        if user is None:
            error = "Błędny nick."
        elif not check_password_hash(user["haslo"], haslo):
            error = "Błędne hasło."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            flash(f'Zalogowano użytkownika {user["nick"]}!')
            return redirect(url_for('index'))
        flash(error)
    return render_template('users_zaloguj.html')


@bp.before_app_request
def load_user():
    u_id = session.get('user_id')
    if u_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE id = ?', [u_id]).fetchone()


@bp.route('/wyloguj')
def wyloguj():
    flash(f"Wylogowano użytkownika {g.user['nick']}.")
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('users.zaloguj'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/lista')
@login_required
def lista():
    dane = get_db().execute('SELECT * FROM users').fetchall()
    if not dane:
        flash('Brak użytkowników!')
    return render_template('users_lista.html', dane=dane)


@bp.route('/dodaj', methods=['GET', 'POST'])
@login_required
def dodaj():
    if request.method == 'POST':
        nick = request.form['nick'].strip()
        haslo = request.form['haslo'].strip()
        grupa = request.form['grupa'].strip()
        db = get_db()
        try:
            db.execute('INSERT INTO users VALUES (?, ?, ?, ?)',
                       [None, nick, grupa, generate_password_hash(haslo)])
            db.commit()
        except db.IntegrityError:
            flash(f"Podany nick {nick} jest już używany.")
        else:
            flash(f"Dodano konto {nick}")
            return redirect(url_for('users.lista'))

    return render_template('user_dodaj.html')


def get_user(u_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', [u_id]).fetchone()
    if user is None:
        abort(404, f"Użytkownik o id {u_id} nie istnieje.")
    return user


@bp.route('/<int:u_id>/edytuj/', methods=['GET', 'POST'])
@login_required
def edytuj(u_id):
    user = get_user(u_id)
    if request.method == 'POST':
        nick = request.form['nick'].strip()
        haslo = request.form['haslo'].strip()
        grupa = request.form['grupa'].strip()
        db = get_db()
        try:
            if haslo:
                db.execute('UPDATE users SET nick = ?, grupa = ?, haslo = ? WHERE id = ?',
                           [nick, grupa, generate_password_hash(haslo), u_id])
            else:
                db.execute('UPDATE users SET nick = ?, grupa = ? WHERE id = ?',
                           [nick, grupa, u_id])
            db.commit()
        except db.IntegrityError:
            flash(f"Podany nick {nick} jest już używany.")
        else:
            flash(f"Zaktualizowano konto {nick}")
            return redirect(url_for('users.lista'))

    return render_template('user_edytuj.html', rekord=user)

@bp.route('/<int:u_id>/usun', methods=['GET', 'POST'])
@login_required
def usun(u_id):
    user = get_user(u_id)
    if request.method == 'POST':
        db = get_db()
        db.execute('DELETE FROM users WHERE id = ?', [u_id])
        db.commit()
        flash(f'Usunięto użytkownika {user["nick"]}!')
        return redirect(url_for('users.lista'))
    return render_template("user_usun.html", rekord=user)

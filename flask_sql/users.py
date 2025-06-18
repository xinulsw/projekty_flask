import functools

from flask import Blueprint, render_template, request, session, flash, redirect, url_for, g
from werkzeug.security import check_password_hash, generate_password_hash
from db import query_db, get_db

bp = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')

@bp.route('/loguj', methods=['GET', 'POST'])
def loguj():
    if request.method == 'POST':
        nick = request.form['nick'].strip()
        haslo = request.form['haslo'].strip()

        error = None
        user = query_db('SELECT * FROM user WHERE nick = ?', [nick], one=True)
        if user is None:
            error = 'Błędny login'
        elif not check_password_hash(user['haslo'], haslo):
            error = 'Błędne hasło!'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            flash(f'Zalogowano użytkownika {nick}!')
            return redirect(url_for('index'))

        flash(error)

    return render_template('users/user_loguj.html', akcja='Zaloguj')

@bp.before_app_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = query_db('SELECT * FROM user WHERE id = ?', [user_id], one=True)

@bp.route('/wyloguj')
def wyloguj():
    session.clear()
    flash(f'Wylogowano użytkownika {g.user['nick']}')
    return redirect(url_for('index'))

@bp.route('/dodaj', methods=['GET', 'POST'])
def dodaj():

    if request.method == 'POST':
        nick = request.form['nick'].strip()
        haslo = request.form['haslo'].strip()
        db = get_db()
        try:
            db.execute('INSERT INTO user VALUES (?, ?, ?)',
                       [None, nick, generate_password_hash(haslo)])
            db.commit()
        except db.IntegrityError:
            flash(f'Podany nick {nick} jest już używany')
        else:
            flash(f'Dodano konto {nick}')
            return redirect(url_for('users.loguj'))

    return render_template('users/user_dodaj.html', akcja='Zapisz')

@bp.route('/usun', methods=['GET', 'POST'])
def usun():
    pass

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('users.loguj'))
        return view(**kwargs)
    return wrapped_view()

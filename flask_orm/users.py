from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import exc
from .models import User
from .forms import UserFormCreate, UserFormLogin
from .db import db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

bp = Blueprint('users', __name__, template_folder='templates', url_prefix='/users')

@bp.route('/dodaj', methods=['GET', 'POST'])
def dodaj():
    form = UserFormCreate()
    if form.validate_on_submit():
        email = form.email.data
        nick = form.nick.data
        haslo = form.haslo.data
        user = User(email=email, nick=nick, haslo=generate_password_hash(haslo))
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            flash(f'Podany email {email} jest już używany.')
            return redirect(url_for('users.dodaj'))
        else:
            flash(f'Dodano konto {nick}')
            return redirect(url_for('users.loguj'))

    return render_template('users/user_dodaj.html', form=form)

login_manager = LoginManager()
login_manager.login_view = 'users.loguj'
login_manager.login_message = u'Zaloguj się, żeby wejść na tę stronę.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/loguj', methods=['GET', 'POST'])
def loguj():
    form = UserFormLogin()
    print(form.email.data)
    print(form.haslo.data)
    if form.validate_on_submit():
        email = form.email.data
        haslo = form.haslo.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.haslo, haslo):
            flash('Błędne dane logowania.')
            return redirect(url_for('users.loguj'))

        login_user(user, remember=True)
        flash(f'Zalogowano użytkownika {user.nick}!')
        return redirect(url_for('index'))

    return render_template('users/user_loguj.html', form=form)

@bp.route('/wyloguj')
@login_required
def wyloguj():
    flash(f'Wylogowano użytkownika {current_user.nick}.')
    logout_user()
    return redirect(url_for('index'))

@bp.route('/usun', methods=['GET', 'POST'])
@login_required
def usun():
    if request.method == 'POST':
        db.session.delete(current_user)
        db.session.commit()
        flash(f'Usunięto użytkownika {current_user.nick}!')
        return redirect(url_for('index'))

    return render_template('users/user_usun.html')

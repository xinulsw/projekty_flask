import os
from flask import Flask, render_template, current_app

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # konfiguracja aplikacji
    app.config.from_mapping(
        SECRET_KEY='bardzosekretnawartosc',
        DATABASE=os.path.join(app.root_path, 'db.sqlite'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' +
                                os.path.join(app.root_path, 'db.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SITE_NAME='Aplikacja Flask SQLAlchemy'
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import db
    db.init_app(app)

    from . import users
    app.register_blueprint(users.bp, url_prefix='/users')
    users.login_manager.init_app(app)

    from .views import ListView
    from .models import Kategoria

    app.add_url_rule(
        '/kategorie/',
        view_func=ListView.as_view('kategorie_lista', Kategoria, 'kategorie/index.html', 'Lista kategorii'),
    )

    from . import kategorie
    app.register_blueprint(kategorie.bp, url_prefix='/kategorie')

    from .models import Pytanie
    app.add_url_rule(
        '/pytania/',
        view_func=ListView.as_view('pytania_lista', Pytanie, 'pytania/index.html', 'Lista pytań'),
    )

    from . import pytania
    app.register_blueprint(pytania.bp, url_prefix='/pytania')

    @app.route('/')
    def index():
        # return 'Cześć, tu Python i Flask!'
        return render_template('index.html')

    with app.app_context():
        if not os.path.exists(current_app.config['DATABASE']):
            from .models import User, Kategoria, Pytanie, Odpowiedz
            # from .dane import pobierz_dane, dodaj_pytania
            db.create_all()
            # pytania = pobierz_dane(os.path.join(app.root_path, 'pytania.csv'))
            # dodaj_pytania(pytania)

    return app

# if __name__ == "__main__":
#     app.run(debug=True)

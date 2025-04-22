import os
from flask import Flask, current_app, render_template
from db import init_app, init_db

import dania
import klienci
import zamowienia
import users

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.root_path, 'restauracja.db'),
    SITE_NAME='Restauracja'
)

init_app(app)
# rejestracja projektów
app.register_blueprint(dania.bp)
app.register_blueprint(klienci.bp)
app.register_blueprint(zamowienia.bp)
app.register_blueprint(users.bp)


@app.route('/')
def index():
    # return 'Strona główna'
    return render_template('index.html')


with app.app_context():
    if not os.path.exists(current_app.config['DATABASE']):
        init_db()
    if __name__ == "__main__":
        app.run(debug=True)

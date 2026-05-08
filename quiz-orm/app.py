import os
from flask import Flask, render_template
from config import Config
from db import baza, init_db, dodaj_dane
import quiz

app = Flask(__name__)
app.config.from_object(Config)


@app.before_request
def _db_connect():
    baza.connect()

@app.teardown_request
def _db_close(exc):
    if not baza.is_closed():
        baza.close()

# rejestracja blueprintów
app.register_blueprint(quiz.bp)

@app.route('/')
def index():
    # return 'Cześć, tu Python i Flask!'
    return render_template('index.html')

with app.app_context():
    if not os.path.exists(Config.DATABASE):
        print('Nie ma bazy!')
        init_db()
        dodaj_dane()

if __name__ == "__main__":
    app.run(debug=True)

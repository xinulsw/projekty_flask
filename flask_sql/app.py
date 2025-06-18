import os
from flask import Flask, request, flash, redirect, url_for, current_app
from flask import render_template
from db import init_app, init_db
import users, zadania, czat, pytania

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='bardzosekretnymkluczem',
    SITE_NAME='Aplikacja Flask',
    DATABASE=os.path.join(app.root_path, 'db.sqlite')
))

init_app(app)
app.register_blueprint(users.bp)
app.register_blueprint(zadania.bp)
app.register_blueprint(czat.bp)
app.register_blueprint(pytania.bp)

# widok domyślny
@app.route('/')
def index():
    # return 'Cześć, tu Python i Flask'
    return render_template('index_.html')

with app.app_context():
    if not os.path.exists(current_app.config['DATABASE']):
        init_db()
    if __name__ == "__main__":
        app.run(debug=True)

# flask --app app run --debug
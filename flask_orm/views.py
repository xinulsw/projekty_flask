from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, current_app
)
from flask_login import login_required
from flask.views import View
from.models import Kategoria

bp = Blueprint('views', __name__)

class ListView(View):
    init_every_request = False
    decorators = [login_required]

    def __init__(self, model, template, tytul):
        self.model = model
        self.template = template
        self.tytul = tytul

    def dispatch_request(self):
        items = self.model.query.all()
        if not items:
            flash('Brak danych!', 'info')
        return render_template(self.template, items=items, tytul=self.tytul)


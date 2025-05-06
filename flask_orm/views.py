from flask import (
    Blueprint, flash, render_template, request, redirect, url_for, current_app
)
from flask_login import login_required, current_user
from flask.views import View
from .db import db

bp = Blueprint('views', __name__)

class ListView(View):
    init_every_request = False
    decorators = [login_required]

    def __init__(self, model, template, tytul, is_logged=True):
        self.model = model
        self.template = template
        self.tytul = tytul
        self.is_logged=True

    def dispatch_request(self):
        # items = self.model.query.all()
        if self.is_logged:
            items = db.session.execute(db.select(self.model).where(self.model.user_id == current_user.id)).scalars().all()
        else:
            items = db.session.execute(db.select(self.model)).scalars().all()
        print(items)
        if not items:
            flash('Brak danych!', 'info')
        return render_template(self.template, items=items, tytul=self.tytul)


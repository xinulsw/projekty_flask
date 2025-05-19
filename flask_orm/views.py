from flask import (
    Blueprint, flash, render_template
)
from flask_login import login_required, current_user
from flask.views import View
from .db import db
from .models import Pytanie, Kategoria

bp = Blueprint('views', __name__)

class ListView(View):
    init_every_request = False
    decorators = [login_required]

    def __init__(self, model, template, tytul, is_logged=True):
        self.model = model
        self.template = template
        self.tytul = tytul
        self.is_logged=is_logged

    def dispatch_request(self):
        # items = self.model.query.all()
        if self.is_logged:
            if isinstance(self.model, Pytanie):
                items = db.session.execute(
                    db.select(self.model, Kategoria).join(Pytanie.kategoria).where(self.model.user_id == current_user.id)).scalars().all()
            else:
                items = db.session.execute(db.select(self.model).where(self.model.user_id == current_user.id)).scalars().all()
        else:
            items = db.session.execute(db.select(self.model)).scalars().all()
        print('Lista obiektów:', items)
        if not items:
            flash('Brak danych!', 'info')
        return render_template(self.template, items=items, tytul=self.tytul)


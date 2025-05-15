from typing import List
from sqlalchemy import Integer, String, Boolean, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin
from .db import db


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    nick: Mapped[str] = mapped_column(String(50))
    haslo: Mapped[str] = mapped_column(String(256))
    kategorie: Mapped[List['Kategoria']] = relationship(
        'Kategoria', back_populates='user',
        cascade='all, delete-orphan')
    pytania: Mapped[List['Pytanie']] = relationship(
        'Pytanie', back_populates='user',
        cascade='all, delete-orphan')

    def __init__(self, email=None, nick=None, haslo=None):
        self.email = email
        self.nick = nick
        self.haslo = haslo

    def __repr__(self):
        return f'<User {self.nick!r}>'


@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    u1 = User(email="anonim@home.net", nick='anonim', haslo='')
    u2 = User(email="adam@home.net", nick='adam',
                        haslo='scrypt:32768:8:1$b6ySf4OhUqADg4os$9fab79b9175c7e1ac341d06b72a3bb3e3a213733c6211bfa7f2b388988065e837df630be38e7eb5729d59db4f5e7d0abd7886e0697125f1a0e8a0eadd6a9eb3a')
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()


class Kategoria(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kategoria: Mapped[str] = mapped_column(String(50), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='kategorie')
    pytania: Mapped[List['Pytanie']] = relationship(
        'Pytanie', back_populates='kategoria')

    def __repr__(self):
        return self.kategoria


@event.listens_for(Kategoria.__table__, 'after_create')
def create_user(*args, **kwargs):
    k = Kategoria(kategoria="brak", user_id=1)
    db.session.add(k)
    db.session.commit()


class Pytanie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pytanie: Mapped[str] = mapped_column(String(255), unique=True)
    kategoria_id: Mapped[int] = mapped_column(ForeignKey('kategoria.id', onupdate='CASCADE', ondelete='SET NULL'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', onupdate='CASCADE', ondelete='SET NULL'))
    kategoria: Mapped['Kategoria'] = relationship(back_populates='pytania')
    user: Mapped['User'] = relationship(back_populates='pytania')
    odpowiedzi: Mapped[List['Odpowiedz']] = relationship(
        'Odpowiedz', back_populates='pytanie',
        cascade='all, delete-orphan')

    def __repr__(self):
        return self.pytanie


class Odpowiedz(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pytanie_id: Mapped[int] = mapped_column(ForeignKey('pytanie.id', ondelete='CASCADE'))
    odpowiedz: Mapped[str] = mapped_column(String(100))
    poprawna: Mapped[bool] = mapped_column(Boolean, default=False)
    pytanie: Mapped['Pytanie'] = relationship(back_populates='odpowiedzi')

    def __repr__(self):
        return f'{self.odpowiedz} ({self.poprawna})'

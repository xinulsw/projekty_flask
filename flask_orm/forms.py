from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField
from wtforms import RadioField, HiddenField, FieldList
from wtforms.validators import DataRequired

blad1 = 'To pole jest wymagane'
blad2 = 'Brak zaznaczonej poprawnej odpowiedzi'


class UserFormCreate(FlaskForm):
    email = EmailField('Email:',
                       validators=[DataRequired(message=blad1)])
    nick = StringField('Nick:',
                       validators=[DataRequired(message=blad1)])
    haslo = PasswordField('Hasło:',
                          validators=[DataRequired(message=blad1)])


class UserFormLogin(FlaskForm):
    email = EmailField('Email:',
                       validators=[DataRequired(message=blad1)])
    haslo = PasswordField('Hasło:',
                          validators=[DataRequired(message=blad1)])


class KategoriaForm(FlaskForm):
    kategoria = StringField('Nazwa kategorii:',
                            validators=[DataRequired(message=blad1)])


class PytanieForm(FlaskForm):
    pytanie = StringField('Treść pytania:',
                          validators=[DataRequired(message=blad1)])
    odpowiedzi = FieldList(StringField(
        'Odpowiedź',
        validators=[DataRequired(message=blad1)]),
        min_entries=3,
        max_entries=3)
    odpok = RadioField(
        'Poprawna odpowiedź',
        validators=[DataRequired(message=blad2)],
        choices=[('0', 'o0'), ('1', 'o1'), ('2', 'o2')]
    )

    pid = HiddenField("Pytanie id")

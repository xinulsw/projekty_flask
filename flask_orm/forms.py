from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms import RadioField, HiddenField, FieldList, SelectField
from wtforms.validators import DataRequired, Length

blad1 = 'To pole jest wymagane'
blad2 = 'Brak zaznaczonej poprawnej odpowiedzi'

class UserFormLogin(FlaskForm):
    email = EmailField('Email:',
                       validators=[DataRequired(message=blad1)])
    haslo = PasswordField('Hasło:',
                          validators=[DataRequired(message=blad1)])
    submit = SubmitField(label='Zaloguj')


class UserFormCreate(UserFormLogin):
    nick = StringField('Nick:',
                       validators=[DataRequired(message=blad1)])
    submit = SubmitField(label='Utwórz konto')


class KategoriaForm(FlaskForm):
    kategoria = StringField('Nazwa kategorii:',
                            validators=[DataRequired(message=blad1), Length(min=3, max=25)])
    submit = SubmitField(label='Zapisz')
    delete = SubmitField('Usuń')

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
    kategoria_id = SelectField('Kategoria', coerce=int)
    submit = SubmitField(label='Zapisz')
    pid = HiddenField("Pytanie id")

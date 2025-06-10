from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, FormField, HiddenField, IntegerField
from wtforms import BooleanField, SelectMultipleField, FieldList, SelectField
from wtforms import widgets
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import HiddenInput

blad1 = 'To pole jest wymagane!'
blad2 = 'Brak zaznaczonej poprawnej odpowiedzi!'

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

class OdpowiedzForm(FlaskForm):
    odpowiedz = StringField('Odpowiedź', validators=[DataRequired(message=blad1)])
    poprawna = BooleanField()

class PytanieFormBase(FlaskForm):
    pytanie = StringField('Treść pytania:', validators=[DataRequired(message=blad1)])
    l_poprawnych_odp = IntegerField(widget=HiddenInput())
    odpowiedzi = FieldList(FormField(OdpowiedzForm), min_entries=3)

class PytanieForm(PytanieFormBase):
    kategoria_id = SelectField('Kategoria', coerce=int)
    submit = SubmitField(label='Zapisz')

    def validate_odpowiedzi(self, field):
        """
        Sprawdzenie, czy zaznaczono przynajmniej jedną odpowiedź jako poprawną.
        :param field: lista formularzy odpowiedzi
        :return: wyjątek walidacji
        """
        l_poprawnych_odp = 0
        print(field.data)
        for o in field.data:
            if o['poprawna']:
                l_poprawnych_odp += 1
        if not l_poprawnych_odp:
            raise ValidationError('Przynajmniej jedna odpowiedź musi być poprawna!')
        self.l_poprawnych_odp.data = l_poprawnych_odp

class TestForm(FlaskForm):
    pytania = FieldList(FormField(PytanieFormBase), min_entries=1)
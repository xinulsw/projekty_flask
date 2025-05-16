from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, FormField
from wtforms import BooleanField, SelectMultipleField, FieldList, SelectField
from wtforms import widgets
from wtforms.validators import DataRequired, Length, ValidationError

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

class PytanieForm(FlaskForm):
    pytanie = StringField('Treść pytania:', validators=[DataRequired(message=blad1)])
    odpowiedzi = FieldList(FormField(OdpowiedzForm), min_entries=3)
    kategoria_id = SelectField('Kategoria', coerce=int)
    submit = SubmitField(label='Zapisz')

    def validate_odpowiedzi(self, field):
        """
        Sprawdzenie, czy zaznaczono przynajmniej jedną odpowiedź jako poprawną.
        :param field: lista formularzy odpowiedzi
        :return: wyjątek walidacji
        """
        validate = True
        for o in field.data:
            if o['poprawna']:
                validate = False
                break
        if validate:
            raise ValidationError('Przynajmniej jedna odpowiedź musi być poprawna!')

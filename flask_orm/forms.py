from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms import BooleanField, SelectMultipleField, FieldList, SelectField
from wtforms import widgets
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

class OdpowiedzForm(FlaskForm):
    odpowiedz = StringField('Odpowiedź', validators=[DataRequired(message=blad1)])
    poprawna = BooleanField()

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PytanieForm(FlaskForm):
    pytanie = StringField('Treść pytania:', validators=[DataRequired(message=blad1)])
    odpowiedzi = FieldList(StringField(
        'Odpowiedź',
        validators=[DataRequired(message=blad1)]),
        min_entries=3,
        max_entries=3)
    odpok = SelectMultipleField(
        'Odpowiedź',
        coerce=int,
        choices=[('1', 'o0'), ('2', 'o1'), ('3', 'o2')],
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput()
    )
    kategoria_id = SelectField('Kategoria', coerce=int)
    submit = SubmitField(label='Zapisz')

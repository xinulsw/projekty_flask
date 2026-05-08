from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, HiddenField, FieldList, SelectField
from wtforms.validators import DataRequired

blad1 = 'To pole jest wymagane'
blad2 = 'Brak zaznaczonej poprawnej odpowiedzi'


class PytanieForm(FlaskForm):
    pytanie = StringField('Treść pytania:',
                          validators=[DataRequired(message=blad1)])
    kategoria_id = SelectField('Kategoria', coerce=int)
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

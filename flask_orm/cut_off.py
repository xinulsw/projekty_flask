# class PytanieForm(FlaskForm):
#     pytanie = StringField('Treść pytania:', validators=[DataRequired(message=blad1)])
#     odpowiedzi = FieldList(StringField(
#         'Odpowiedź',
#         validators=[DataRequired(message=blad1)]),
#         min_entries=3,
#         max_entries=3)
#     odpok = SelectMultipleField(
#         'Odpowiedź',
#         coerce=int,
#         choices=[('1', 'o0'), ('2', 'o1'), ('3', 'o2')],
#         widget=widgets.ListWidget(prefix_label=False),
#         option_widget=widgets.CheckboxInput()
#     )
#     kategoria_id = SelectField('Kategoria', coerce=int)
#     submit = SubmitField(label='Zapisz')
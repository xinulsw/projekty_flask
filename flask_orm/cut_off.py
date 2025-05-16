# @bp.route('/pytania/lista')
# def pytania_lista():
#     """Pobranie z bazy i wyświetlenie wszystkich pytań"""
#     pytania = db.session.execute(db.select(Pytanie)).scalars()
#     if not pytania:
#         flash('Brak pytań!', 'kom')
#         return redirect(url_for('pytania.index'))
#
#     return render_template('pytania/pytania_lista.html', pytania=pytania)

# def flash_errors(form):
#     """Odczytanie wszystkich błędów formularza i przygotowanie komunikatów"""
#     for field, errors in form.errors.items():
#         for error in errors:
#             if type(error) is list:
#                 error = error[0]
#             flash("Błąd: {}. Pole: {}".format(
#                 error,
#                 getattr(form, field).label.text))

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
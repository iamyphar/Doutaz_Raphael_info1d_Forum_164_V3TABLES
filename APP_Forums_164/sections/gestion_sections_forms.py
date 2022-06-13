"""
    File : gestion_sections_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Length, DataRequired, Regexp, Optional, InputRequired


class FormSection(FlaskForm):
    title_section = StringField("Titre*", validators=[
        Length(min=2, max=32, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        Regexp("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait union"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    description_section = TextAreaField("Description", validators=[
        Optional(True),
        Length(min=2, max=256, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    submit = SubmitField("Enregistrer")

    submit_delete = SubmitField("Supprimer")

    submit_cancel = SubmitField("Annuler")
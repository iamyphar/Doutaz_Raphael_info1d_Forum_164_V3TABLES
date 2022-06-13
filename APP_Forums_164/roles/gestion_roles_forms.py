"""
    File : gestion_roles_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired, Regexp, InputRequired


class FormRole(FlaskForm):
    name_role = StringField("Nom*", validators=[
        Length(min=2, max=32, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        Regexp("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait union"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    submit = SubmitField("Enregistrer")

    submit_delete = SubmitField("Supprimer")

    submit_cancel = SubmitField("Annuler")
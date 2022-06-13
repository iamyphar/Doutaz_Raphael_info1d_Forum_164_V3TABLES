"""
    File : gestion_chars_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, URLField, SelectField
from wtforms.validators import Length, DataRequired, Optional, Regexp, InputRequired, URL, NoneOf
from wtforms_components import DateRange


class FormChar(FlaskForm):
    last_name_char = StringField("Nom*", validators=[
        Length(min=2, max=32, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        Regexp("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait union"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()

    ])

    first_name_char = StringField("Prénom*", validators=[
        Length(min=2, max=32, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        Regexp("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait union"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    bio_char = TextAreaField("Biographie", validators=[
        Optional(True),
        Length(min=2, max=256, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    birthdate_char = DateField("Date de naissance*", validators=[
        DateRange(min=(date.fromisoformat("0001-01-01")), max=(date.today()), message="Format de date incorrect"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    icon_char = URLField("Photo de profil (URL)*", validators=[
        DataRequired(message="Champs obligatoire"),
        InputRequired(),
        Regexp("([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg|webp)",
               message="Image invalide"),
        URL(require_tld=False, message="Lien invalide"),
        Length(min=2, max=1024, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    fk_user = SelectField("Utilisateur*", validate_choice=False,
                             validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_user_text = StringField("Utilisateur*")

    submit = SubmitField("Enregistrer")

    submit_delete = SubmitField("Supprimer")

    submit_cancel = SubmitField("Annuler")
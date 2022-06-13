"""
    File : gestion_chars_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from datetime import date

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from wtforms.validators import Regexp
from wtforms_components import DateRange


class FormAddChar(FlaskForm):
    last_name_char_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    last_name_char = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                                    Regexp(last_name_char_regexp,
                                                           message="Pas de chiffres, de caractères "
                                                                   "spéciaux, "
                                                                   "d'espace à double, de double "
                                                                   "apostrophe, de double trait union"),
                                                    DataRequired(message="Champs obligatoire !")])
    first_name_char_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    first_name_char = StringField("Prénom",
                                  validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                              Regexp(first_name_char_regexp,
                                                     message="Pas de chiffres, de "
                                                             "caractères "
                                                             "spéciaux, "
                                                             "d'espace à double, de double "
                                                             "apostrophe, de double trait "
                                                             "union"),
                                              DataRequired(message="Champs obligatoire !")])

    bio_char = TextAreaField("Biographie")

    birthdate_char = DateField("Date de naissance", validators=[
        DateRange(min=(date.fromisoformat("0001-01-01")), max=(date.today()), message="Format de date incorrect"),
        DataRequired(message="Champs obligatoire !")])

    icon_char_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_char = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                 Regexp(icon_char_regexp,
                                                                        message="Chemin invalide")])
    submit = SubmitField("Ajouter le personnage")


class FormUpdateChar(FlaskForm):
    last_name_char_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    last_name_char = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                                    Regexp(last_name_char_regexp,
                                                           message="Pas de chiffres, de caractères "
                                                                   "spéciaux, "
                                                                   "d'espace à double, de double "
                                                                   "apostrophe, de double trait union"),
                                                    DataRequired(message="Champs obligatoire !")])
    first_name_char_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    first_name_char = StringField("Prénom",
                                  validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                              Regexp(first_name_char_regexp,
                                                     message="Pas de chiffres, de "
                                                             "caractères "
                                                             "spéciaux, "
                                                             "d'espace à double, de double "
                                                             "apostrophe, de double trait "
                                                             "union"),
                                              DataRequired(message="Champs obligatoire !")])

    bio_char = TextAreaField("Biographie")

    birthdate_char = DateField("Date de naissance", validators=[
        DateRange(min=(date.fromisoformat("0001-01-01")), max=(date.today()), message="Format de date incorrect"),
        DataRequired(message="Champs obligatoire !")])

    icon_char_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_char = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                 Regexp(icon_char_regexp,
                                                                        message="Chemin invalide")])
    submit = SubmitField("Mettre à jour le personnage")


class FormDeleteChar(FlaskForm):
    last_name_char = StringField("Nom")
    first_name_char = StringField("Prénom")
    bio_char = TextAreaField("Biographie")
    birthdate_char = DateField("Date de naissance")
    icon_char = StringField("Photo de profil (URL)")
    del_final_btn = SubmitField("Effacer ce personnage")
    del_conf_btn = SubmitField("Êtes-vous sûr d'effacer ?")
    cancel_btn = SubmitField("Annuler")

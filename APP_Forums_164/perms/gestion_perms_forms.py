"""
    File : gestion_perms_forms.py
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


class FormAddPerm(FlaskForm):
    name_perm_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\-_ ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    name_perm = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                                    Regexp(name_perm_regexp,
                                                           message="Pas de chiffres, de caractères "
                                                                   "spéciaux, "
                                                                   "d'espace à double, de double "
                                                                   "apostrophe, de double trait union"),
                                                    DataRequired(message="Champs obligatoire !")])

    description_perm = TextAreaField("Description")
    submit = SubmitField("Ajouter la permission")


class FormUpdatePerm(FlaskForm):
    name_perm_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\-_ ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    name_perm = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                                    Regexp(name_perm_regexp,
                                                           message="Pas de chiffres, de caractères "
                                                                   "spéciaux, "
                                                                   "d'espace à double, de double "
                                                                   "apostrophe, de double trait union"),
                                                    DataRequired(message="Champs obligatoire !")])

    description_perm = TextAreaField("Description")
    submit = SubmitField("Mettre à jour la permission")


class FormDeletePerm(FlaskForm):
    name_perm = StringField("Nom")
    description_perm = TextAreaField("Description")
    del_final_btn = SubmitField("Effacer cette permission")
    del_conf_btn = SubmitField("Êtes-vous sûr d'effacer ?")
    cancel_btn = SubmitField("Annuler")

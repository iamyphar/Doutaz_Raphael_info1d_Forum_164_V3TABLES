"""
    File : gestion_roles_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from wtforms.validators import Regexp


class FormAddRole(FlaskForm):
    name_role_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    name_role = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                               Regexp(name_role_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union"),
                                               DataRequired(message="Champs obligatoire !")])
    submit = SubmitField("Ajouter le rôle")


class FormUpdateRole(FlaskForm):
    name_role_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    name_role = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                               Regexp(name_role_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union"),
                                               DataRequired(message="Champs obligatoire !")])
    submit = SubmitField("Mettre à jour le rôle")


class FormDeleteRole(FlaskForm):
    name_role = StringField("Nom")
    del_final_btn = SubmitField("Effacer ce rôle")
    del_conf_btn = SubmitField("Êtes-vous sûr d'effacer ?")
    cancel_btn = SubmitField("Annuler")

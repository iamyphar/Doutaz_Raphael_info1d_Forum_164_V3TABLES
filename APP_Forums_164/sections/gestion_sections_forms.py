"""
    File : gestion_sections_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from wtforms.validators import Regexp


class FormAddSection(FlaskForm):
    title_section_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    title_section = StringField("Titre", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                                     Regexp(title_section_regexp,
                                                            message="Pas de chiffres, de caractères "
                                                                    "spéciaux, "
                                                                    "d'espace à double, de double "
                                                                    "apostrophe, de double trait union"),
                                                     DataRequired(message="Champs obligatoire !")])
    description_section = TextAreaField("description")
    submit = SubmitField("Ajouter la section")


class FormUpdateSection(FlaskForm):
    title_section_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    title_section = StringField("Titre", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                                     Regexp(title_section_regexp,
                                                            message="Pas de chiffres, de caractères "
                                                                    "spéciaux, "
                                                                    "d'espace à double, de double "
                                                                    "apostrophe, de double trait union"),
                                                     DataRequired(message="Champs obligatoire !")])
    description_section = TextAreaField("description")
    submit = SubmitField("Mettre à jour la section")


class FormDeleteSection(FlaskForm):
    title_section = StringField("Titre")
    description_section = TextAreaField("description")
    del_final_btn = SubmitField("Effacer ce section")
    del_conf_btn = SubmitField("Êtes-vous sûr d'effacer ?")
    cancel_btn = SubmitField("Annuler")

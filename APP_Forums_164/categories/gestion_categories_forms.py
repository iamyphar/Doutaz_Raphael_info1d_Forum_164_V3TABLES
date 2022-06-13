"""
    File : gestion_categories_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from wtforms.validators import Regexp


class FormAddCategory(FlaskForm):
    title_cat_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    title_cat = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                               Regexp(title_cat_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union"),
                                               DataRequired(message="Champs obligatoire !")])
    description_cat = TextAreaField("Description")
    icon_cat_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_cat = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                Regexp(icon_cat_regexp,
                                                                       message="Chemin invalide")])
    fk_section = SelectField("Section", validate_choice=False)
    submit = SubmitField("Ajouter la catégorie")


class FormUpdateCategory(FlaskForm):
    title_cat_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    title_cat = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                               Regexp(title_cat_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union"),
                                               DataRequired(message="Champs obligatoire !")])
    description_cat = TextAreaField("Description")
    icon_cat_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_cat = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                Regexp(icon_cat_regexp,
                                                                       message="Chemin invalide")])
    fk_section = SelectField("Section", validate_choice=False)
    submit = SubmitField("Mettre à jour la catégorie")


class FormDeleteCategory(FlaskForm):
    title_cat = StringField("Nom")
    description_cat = TextAreaField("Description")
    icon_cat = StringField("Photo de profil (URL)")
    fk_section = SelectField("Section")
    del_final_btn = SubmitField("Effacer ce catégorie")
    del_conf_btn = SubmitField("Êtes-vous sûr d'effacer ?")
    cancel_btn = SubmitField("Annuler")

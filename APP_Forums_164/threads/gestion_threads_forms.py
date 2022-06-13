"""
    File : gestion_threads_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired
from wtforms.validators import Regexp


class FormAddThread(FlaskForm):
    title_thread_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    title_thread = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                               Regexp(title_thread_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union"),
                                               DataRequired(message="Champs obligatoire !")])
    content_thread = TextAreaField("Description")
    icon_thread_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_thread = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                Regexp(icon_thread_regexp,
                                                                       message="Chemin invalide")])
    pinned_thread = BooleanField("Épinglé")
    fk_cat = SelectField("Categorie", validate_choice=False)
    submit = SubmitField("Ajouter la fils de discussions")


class FormUpdateThread(FlaskForm):
    title_thread_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    title_thread = StringField("Nom", validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                               Regexp(title_thread_regexp,
                                                      message="Pas de chiffres, de caractères "
                                                              "spéciaux, "
                                                              "d'espace à double, de double "
                                                              "apostrophe, de double trait union"),
                                               DataRequired(message="Champs obligatoire !")])
    content_thread = TextAreaField("Description")
    icon_thread_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_thread = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                Regexp(icon_thread_regexp,
                                                                       message="Chemin invalide")])
    fk_cat = SelectField("Categorie", validate_choice=False)
    submit = SubmitField("Mettre à jour la fils de discussions")


class FormDeleteThread(FlaskForm):
    title_thread = StringField("Nom")
    content_thread = TextAreaField("Description")
    icon_thread = StringField("Photo de profil (URL)")
    fk_cat = SelectField("Categorie")
    del_final_btn = SubmitField("Effacer ce fils de discussions")
    del_conf_btn = SubmitField("Êtes-vous sûr d'effacer ?")
    cancel_btn = SubmitField("Annuler")

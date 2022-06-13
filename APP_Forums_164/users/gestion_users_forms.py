"""
    File : gestion_users_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired, Email
from wtforms.validators import Regexp


class FormAddUser(FlaskForm):
    nickname_user_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nickname_user = StringField("Nom d'utilisateur",
                                validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                            Regexp(nickname_user_regexp,
                                                   message="Pas de chiffres, de caractères "
                                                           "spéciaux, "
                                                           "d'espace à double, de double "
                                                           "apostrophe, de double trait union"),
                                            DataRequired(message="Champs obligatoire !")])
    password_user = StringField("Mot de passe",
                                validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                            DataRequired(message="Champs obligatoire !")])
    name_email = StringField("Adresse email", validators=[Email(message="Email invalide"), Length(min=2, max=320,
                                                                                                  message="Minimum 2 caractères, maximum 320."),
                                                          DataRequired(message="Champs obligatoire !")])
    bio_user = TextAreaField("Biographie")
    signature_user = TextAreaField("Signature")
    discord_regexp = "[ ]*|^.{3,32}#[0-9]{4}$"
    discord_user = StringField("Discord", validators=[Regexp(discord_regexp, message="Nom discord invalide")])
    steam_regexp = "[ ]*|(?:https?:\/\/)?steamcommunity\.com\/(?:profiles|id)\/[a-zA-Z0-9]+"
    steam_user = StringField("Steam", validators=[Regexp(steam_regexp, message="Lien du profil steam invalide")])
    icon_user_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_user = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                 Regexp(icon_user_regexp,
                                                                        message="Chemin invalide")])
    submit = SubmitField("Ajouter l'utilisateur")


class FormUpdateUser(FlaskForm):
    nickname_user_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nickname_user = StringField("Nom d'utilisateur",
                                validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                            Regexp(nickname_user_regexp,
                                                   message="Pas de chiffres, de caractères "
                                                           "spéciaux, "
                                                           "d'espace à double, de double "
                                                           "apostrophe, de double trait union"),
                                            DataRequired(message="Champs obligatoire !")])
    password_user = StringField("Mot de passe",
                                validators=[Length(min=2, max=32, message="Minimum 2 caractères, maximum 32."),
                                            DataRequired(message="Champs obligatoire !")])
    name_email = StringField("Adresse email", validators=[Email(message="Email invalide"), Length(min=2, max=320,
                                                                                                  message="Minimum 2 caractères, maximum 320."),
                                                          DataRequired(message="Champs obligatoire !")])
    bio_user = TextAreaField("Biographie")
    signature_user = TextAreaField("Signature")
    discord_regexp = "[ ]*|^.{3,32}#[0-9]{4}$"
    discord_user = StringField("Discord", validators=[Regexp(discord_regexp, message="Nom discord invalide")])
    steam_regexp = "[ ]*|(?:https?:\/\/)?steamcommunity\.com\/(?:profiles|id)\/[a-zA-Z0-9]+"
    steam_user = StringField("Steam", validators=[Regexp(steam_regexp, message="Lien du profil steam invalide")])
    icon_user_regexp = "([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg)"
    icon_user = StringField("Photo de profil (URL)", validators=[DataRequired(message="Champs obligatoire !"),
                                                                 Regexp(icon_user_regexp,
                                                                        message="Chemin invalide")])
    submit = SubmitField("Mettre à jour l'utilisateur")


class FormDeleteUser(FlaskForm):
    nickname_user = StringField("Nom d'utilisateur")
    password_user = StringField("Mot de passe")
    name_email = StringField("Adresse email")
    bio_user = TextAreaField("Biographie")
    signature_user = TextAreaField("Signature")
    discord_user = StringField("Discord")
    steam_user = StringField("Steam")
    registration_date_user = DateField("Date de création du compte")
    icon_user = StringField("Photo de profil (URL)")
    del_final_btn = SubmitField("Effacer cet utilisateur")
    del_conf_btn = SubmitField("Êtes-vous sûr d'effacer ?")
    cancel_btn = SubmitField("Annuler")

"""
    File : gestion_users_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired, Email, InputRequired, Optional
from wtforms.validators import Regexp

class FormUser(FlaskForm):
    nickname_user = StringField("Nom d'utilisateur*", validators=[
        Length(min=2, max=32, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        Regexp("^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$",
               message="Pas de chiffres, de caractères spéciaux, d'espace à double, de double apostrophe, de double trait union"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    password_user = StringField("Mot de passe*", validators=[
        Length(min=2, max=32, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    name_email = EmailField("Adresse email*", validators=[
        Email(message="Email invalide"),
        Length(min=2, max=320, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    bio_user = TextAreaField("Biographie", validators=[
        Optional(True),
        Length(min=2, max=1024, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    signature_user = TextAreaField("Signature", validators=[
        Optional(True),
        Length(min=2, max=1024, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    registration_date_user = DateField("Date de création du compte")

    discord_user = StringField("Discord", validators=[Optional(), Regexp("^$|^[ ][ ]*|^.{3,32}#[0-9]{4}$", message="Nom discord invalide")])

    steam_user = StringField("Steam", validators=[Optional(), Regexp("^(?:https?:\/\/)?steamcommunity\.com\/(?:profiles|id)\/[a-zA-Z0-9_-]+$", message="Lien du profil steam invalide")])

    icon_user = StringField("Photo de profil (URL)*", validators=[
        DataRequired(message="Champs obligatoire"),
        InputRequired(),
        Regexp("([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg|webp)",
               message="Lien invalide")])
    submit = SubmitField("Enregistrer")

    submit_delete = SubmitField("Supprimer")

    submit_cancel = SubmitField("Annuler")

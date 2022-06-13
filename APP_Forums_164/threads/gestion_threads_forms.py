"""
    File : gestion_threads_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, URLField
from wtforms import SubmitField
from wtforms.validators import Length, DataRequired, Regexp, InputRequired, URL, NoneOf


class FormThread(FlaskForm):
    title_thread = StringField("Titre*", validators=[
        Length(min=2, max=64, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    content_thread = TextAreaField("Contenu*", validators=[
        DataRequired(message="Champs obligatoire"),
        InputRequired(),
        Length(min=2, max=8192, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    icon_thread = URLField("Icône (URL)*", validators=[
        DataRequired(message="Champs obligatoire"),
        InputRequired(),
        Regexp("([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg|webp)",
               message="Image invalide"),
        URL(require_tld=False, message="Lien invalide"),
        Length(min=2, max=1024, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    pinned_thread = BooleanField("Épinglé")

    fk_cat = SelectField("Catégorie*", validate_choice=False, validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_user = SelectField("Utilisateur (créateur)*", validate_choice=False, validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_user_author = SelectField("Utilisateur auteur de la suppression*", validate_choice=False, validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_cat_text = StringField("Catégorie*")

    fk_user_text = StringField("Utilisateur (créateur)*")

    submit = SubmitField("Enregistrer")

    submit_delete = SubmitField("Supprimer")

    submit_cancel = SubmitField("Annuler")
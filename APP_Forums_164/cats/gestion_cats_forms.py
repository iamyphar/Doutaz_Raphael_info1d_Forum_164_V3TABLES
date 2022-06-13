"""
    File : gestion_categories_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, URLField
from wtforms.validators import Length, DataRequired, Optional, Regexp, URL, InputRequired, NoneOf
from wtforms.widgets import URLInput


class FormCategory(FlaskForm):
    title_cat = StringField("Titre*", validators=[
        Length(min=2, max=64, message="Le champs doit contenir entre %(min)d et %(max)d caractères"),
        DataRequired(message="Champs obligatoire"),
        InputRequired()
    ])

    description_cat = TextAreaField("Description", validators=[
        Optional(True),
        Length(min=2, max=256, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    icon_cat = URLField("Icône (URL)*", validators=[
        DataRequired(message="Champs obligatoire"),
        InputRequired(),
        Regexp("([http:|https:|\/|.|\w|\s|-])*\.(?:jpg|gif|png|svg|jpeg|webp)",
               message="Image invalide"),
        URL(require_tld=False, message="Lien invalide"),
        Length(min=2, max=1024, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    fk_section = SelectField("Section*", validate_choice=False, validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_cat = SelectField("Catégorie", validate_choice=False)

    fk_section_text = StringField("Section*")

    fk_cat_text = StringField("Catégorie")

    submit = SubmitField("Enregistrer")

    submit_delete = SubmitField("Supprimer")

    submit_cancel = SubmitField("Annuler")

"""
    File : gestion_resps_forms.py
    Author : Raphaël Doutaz 09.05.22
    Form management with WTF
"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, StringField
from wtforms.validators import Length, NoneOf, DataRequired, InputRequired


class FormResp(FlaskForm):
    content_resp = TextAreaField("Contenu*", validators=[
        DataRequired(message="Champs obligatoire"),
        InputRequired(),
        Length(min=2, max=1024, message="Le champs doit contenir entre %(min)d et %(max)d caractères")
    ])

    fk_thread = SelectField("Fils de discussions*", validate_choice=False, validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_user = SelectField("Utilisateur (créateur)*", validate_choice=False, validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_user_author = SelectField("Utilisateur auteur de la suppression*", validate_choice=False, validators=[NoneOf(['None'], message="Champs obligatoire")])

    fk_thread_text = StringField("Fils de discussions*")

    fk_user_text = StringField("Utilisateur (créateur)*")

    submit = SubmitField("Enregistrer")

    submit_delete = SubmitField("Supprimer")

    submit_cancel = SubmitField("Annuler")

"""
    File : msg_avertissements.py
    Author : Raphaël Doutaz 09.05.22

"""
from flask import render_template

from APP_Forums_164 import app


@app.route("/warning")
def warning():
    return render_template("users_have_roles/avertissement_projet.html")

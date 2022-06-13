"""
    File : home.py
    Author : Raphaël Doutaz 09.05.22
"""

from APP_Forums_164.erreurs.exceptions import *


@app.route('/')
@app.route('/homepage')
def homepage():
    return render_template("home.html")

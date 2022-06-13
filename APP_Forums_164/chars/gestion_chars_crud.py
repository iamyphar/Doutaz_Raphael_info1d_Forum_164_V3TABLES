"""Route for characters CRUD
File : gestion_chars_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from datetime import date
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.chars.gestion_chars_forms import FormChar
from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /chars_display route
    
    Test : ex : http://127.0.0.1:5005/chars_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_char = 0 >> all characters.
                id_char = "n" display characters who id is "n"
"""


@app.route("/chars_display/<string:order_by>/<int:id_char>", methods=['GET', 'POST'])
def chars_display(order_by, id_char):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_char == 0:
                    mc_display.execute("""SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char, GROUP_CONCAT(nickname_user) as nickname_user FROM t_characters INNER JOIN t_users_have_characters ON id_char = fk_char INNER JOIN t_users ON id_user = fk_user GROUP BY id_char ORDER BY id_char ASC""")
                elif order_by == "ASC":
                    mc_display.execute("""SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char, GROUP_CONCAT(nickname_user) as nickname_user FROM t_characters INNER JOIN t_users_have_characters ON id_char = fk_char INNER JOIN t_users ON id_user = fk_user WHERE id_char = %(id_charected)s GROUP BY id_char ORDER BY id_char ASC""",
                                       {"id_charected": id_char}
                                       )
                else:
                    mc_display.execute("""SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char, GROUP_CONCAT(nickname_user) as nickname_user FROM t_characters INNER JOIN t_users_have_characters ON id_char = fk_char INNER JOIN t_users ON id_user = fk_user GROUP BY id_char ORDER BY id_char DESC""")

                data = mc_display.fetchall()

                print("Data characters : ", data)

                if not data and id_char == 0:
                    flash("""La table "t_characters" est vide.""", "warning")
                elif not data and id_char > 0:
                    flash(f"Le personnage que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des personnages ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                        f"{chars_display.__name__} ; "
                                        f"{exception_pass}")

    return render_template("chars/chars_display.html", data=data)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /char_add route
    
    Test : ex : http://127.0.0.1:5005/char_add
    
    Settings : -
    
    Goal : Add a character
"""


@app.route("/char_add", methods=['GET', 'POST'])
def char_add():
    form = FormChar()
    with DBconnection() as mybd_conn:
        mybd_conn.execute("SELECT id_user, nickname_user FROM t_users ORDER BY nickname_user")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
    form.fk_user.choices = [(i["id_user"], i["nickname_user"]) for i in data]

    if request.method == "POST":
        try:
            if form.validate_on_submit():
                form.fk_user.data = None if form.fk_user.data == 'None' else form.fk_user.data

                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""INSERT INTO t_characters (id_char,last_name_char, first_name_char, bio_char, birthdate_char, icon_char) VALUES (NULL,%(first_name_char)s,%(last_name_char)s,%(bio_char)s,%(birthdate_char)s,%(icon_char)s) """,
                                     {
                                        "first_name_char": form.first_name_char.data,
                                        "last_name_char": form.last_name_char.data,
                                        "bio_char": form.bio_char.data,
                                        "birthdate_char": form.birthdate_char.data,
                                        "icon_char": form.icon_char.data
                                     }
                                     )
                    mconn_bd.execute("""INSERT INTO t_users_have_characters (id_user_has_char, fk_user, fk_char, add_date_user_has_char) VALUES (NULL, %(fk_user)s, %(fk_char)s,%(date)s)""",
                                     {
                                         'fk_user': form.fk_user.data,
                                         'fk_char': mconn_bd.lastrowid,
                                         'date': date.today()
                                     })

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('chars_display', order_by='ASC', id_char=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                   f"{char_add.__name__} ; "
                                   f"{exception_pass}")

    return render_template("chars/char_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /char_update route
    
    Test : ex : http://127.0.0.1:5005/char_update
    
    Settings : -
    
    Goal : Update a character who has been selected in /chars_display
"""


@app.route("/char_update/<int:id_char>", methods=['GET', 'POST'])
def char_update(id_char):
    form = FormChar()
    with DBconnection() as mybd_conn:
        mybd_conn.execute("SELECT id_user, nickname_user FROM t_users ORDER BY nickname_user")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
    form.fk_user.choices = [(i["id_user"], i["nickname_user"]) for i in data]

    try:
        if form.validate_on_submit():
            with DBconnection() as mconn_bd:
                form.fk_user.data = None if form.fk_user.data == 'None' else form.fk_user.data

                mconn_bd.execute("""UPDATE t_characters SET first_name_char = %(first_name_char)s, last_name_char = %(last_name_char)s, bio_char = %(bio_char)s, birthdate_char = %(birthdate_char)s, icon_char = %(icon_char)s WHERE id_char = %(id_char)s;
                                    UPDATE t_users_have_characters SET fk_user = %(fk_user)s, fk_char = %(id_char)s WHERE fk_char = %(id_char)s""",
                                 {
                                    "id_char": id_char,
                                    "first_name_char": form.first_name_char.data,
                                    "last_name_char": form.last_name_char.data,
                                    "bio_char": form.bio_char.data,
                                    "birthdate_char": form.birthdate_char.data,
                                    "icon_char": form.icon_char.data,
                                    "fk_user": form.fk_user.data
                                })

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('chars_display', order_by="ASC", id_char=id_char))
        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute("SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char , GROUP_CONCAT(fk_user) as fk_user FROM t_characters INNER JOIN t_users_have_characters ON id_char = fk_char WHERE id_char = %(id_char)s GROUP BY id_char",
                                  {"id_char": id_char})
            data = mybd_conn.fetchone()
            print("Data characters ", data)

            form.last_name_char.default = data["last_name_char"]
            form.first_name_char.default = data["first_name_char"]
            form.bio_char.default = data["bio_char"]
            form.birthdate_char.default = data["birthdate_char"]
            form.icon_char.default = data["icon_char"]
            form.fk_user.default = data["fk_user"]
            form.process()

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                  f"{char_update.__name__} ; "
                                  f"{exception_pass}")

    return render_template("chars/char_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /char_delete route
    
    Test : ex : http://127.0.0.1:5005/char_delete
    
    Settings : -
    
    Goal : Delete a character who has been selected in /chars_display
"""


@app.route("/char_delete/<int:id_char>", methods=['GET', 'POST'])
def char_delete(id_char):
    form = FormChar()
    try:
        form.fk_user.choices = [('', '')]
        if request.method == "POST" and form.validate_on_submit():
            if form.submit_cancel.data:
                return redirect(url_for("chars_display", order_by="ASC", id_char=0))

            if form.submit_delete.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""DELETE FROM t_users_have_characters WHERE fk_char = %(id_char)s;DELETE FROM t_characters WHERE id_char = %(id_char)s""", {"id_char": id_char})
                flash(f"Le personnage a été supprimé !", "success")
                print(f"Characters deleted.")

                return redirect(url_for('chars_display', order_by="ASC", id_char=0))

        if request.method == "GET":
            with DBconnection() as mydb_conn:
                mydb_conn.execute("SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char , GROUP_CONCAT(nickname_user) as nickname_user FROM t_characters INNER JOIN t_users_have_characters ON id_char = fk_char INNER JOIN t_users ON id_user = fk_user GROUP BY id_char",
                                  {"id_char": id_char})
                data = mydb_conn.fetchone()
                print("Data character ", data)

            form.last_name_char.data = data["last_name_char"]
            form.first_name_char.data = data["first_name_char"]
            form.bio_char.data = data["bio_char"]
            form.birthdate_char.data = data["birthdate_char"]
            form.icon_char.data = data["icon_char"]
            form.fk_user_text.data = data["nickname_user"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                  f"{char_delete.__name__} ; "
                                  f"{exception_pass}")

    return render_template("chars/char_delete.html",
                           form=form)

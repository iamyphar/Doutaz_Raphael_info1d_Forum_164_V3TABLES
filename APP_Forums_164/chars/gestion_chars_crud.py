"""Route for characters CRUD
File : gestion_chars_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_Forums_164.chars.gestion_chars_forms import FormAddChar
from APP_Forums_164.chars.gestion_chars_forms import FormDeleteChar
from APP_Forums_164.chars.gestion_chars_forms import FormUpdateChar
from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /chars_display route
    
    Test : ex : http://127.0.0.1:5005/chars_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_char_sel = 0 >> all characters.
                id_char_sel = "n" display characters who id is "n"
"""


@app.route("/chars_display/<string:order_by>/<int:id_char_sel>", methods=['GET', 'POST'])
def chars_display(order_by, id_char_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_char_sel == 0:
                    strsql_chars_display = """SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char FROM t_characters ORDER BY last_name_char ASC"""
                    mc_display.execute(strsql_chars_display)
                elif order_by == "ASC":
                    select_dictionary = {"id_char_selected": id_char_sel}
                    strsql_chars_display = """SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char FROM t_characters WHERE id_char = %(id_char_selected)s"""

                    mc_display.execute(strsql_chars_display, select_dictionary)
                else:
                    strsql_chars_display = """SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char FROM t_characters  ORDER BY id_char DESC"""

                    mc_display.execute(strsql_chars_display)

                data_chars = mc_display.fetchall()

                print("Data characters : ", data_chars, " Type : ", type(data_chars))

                # If table is empty
                if not data_chars and id_char_sel == 0:
                    flash("""La table "t_characters" est vide.""", "warning")
                elif not data_chars and id_char_sel > 0:
                    # If no characters with id = id_char_sel found
                    flash(f"Le personnage que vous avez demandé n'existe pas.", "warning")
                else:
                    # In all others cases, this means the table is empty.
                    flash(f"Les données des personnages ont été affichées !", "success")

        except Exception as Exception_chars_display:
            raise ExceptionCharsDisplay(f"file : {Path(__file__).name}  ;  "
                                        f"{chars_display.__name__} ; "
                                        f"{Exception_chars_display}")

    return render_template("chars/chars_display.html", data=data_chars)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /char_add route
    
    Test : ex : http://127.0.0.1:5005/char_add
    
    Settings : -
    
    Goal : Add a characters
"""


@app.route("/char_add", methods=['GET', 'POST'])
def char_add():
    form = FormAddChar()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                insertion_dictionary = {"first_name_char": form.first_name_char.data,
                                        "last_name_char": form.last_name_char.data,
                                        "bio_char": form.bio_char.data,
                                        "birthdate_char": form.birthdate_char.data,
                                        "icon_char": form.icon_char.data}
                print("Dictionary : ", insertion_dictionary)

                strsql_insert_char = """INSERT INTO t_characters (id_char,last_name_char, first_name_char, bio_char, birthdate_char, icon_char) VALUES (NULL,%(first_name_char)s,%(last_name_char)s,%(bio_char)s,%(birthdate_char)s,%(icon_char)s) """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_char, insertion_dictionary)

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('chars_display', order_by='DESC', id_char_sel=0))

        except Exception as Exception_char_add:
            raise ExceptionCharAdd(f"file : {Path(__file__).name}  ;  "
                                   f"{char_add.__name__} ; "
                                   f"{Exception_char_add}")

    return render_template("chars/char_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /char_update route
    
    Test : ex : http://127.0.0.1:5005/char_update
    
    Settings : -
    
    Goal : Update a characters who has been selected in /chars_display
"""


@app.route("/char_update", methods=['GET', 'POST'])
def char_update():
    id_char = request.values['id_char']

    form = FormUpdateChar()
    try:
        print(" on submit ", form.validate_on_submit())
        if form.validate_on_submit():
            update_dictionary = {"id_char": id_char,
                                 "first_name_char": form.first_name_char.data,
                                 "last_name_char": form.last_name_char.data,
                                 "bio_char": form.bio_char.data,
                                 "birthdate_char": form.birthdate_char.data,
                                 "icon_char": form.icon_char.data
                                 }
            print("Dictionnary : ", update_dictionary)

            strsql_update_char = """UPDATE t_characters SET first_name_char = %(first_name_char)s, last_name_char = %(last_name_char)s, bio_char = %(bio_char)s, birthdate_char = %(birthdate_char)s, icon_char = %(icon_char)s WHERE id_char = %(id_char)s;"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_char, update_dictionary)

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('chars_display', order_by="ASC", id_char_sel=id_char))
        elif request.method == "GET":
            strsql_id_char = "SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char FROM t_characters WHERE id_char = %(id_char)s"
            select_dictionary = {"id_char": id_char}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(strsql_id_char, select_dictionary)
            data_char = mybd_conn.fetchone()
            print("Data characters ", data_char, " type ", type(data_char), " char ",
                  data_char["first_name_char"], data_char["last_name_char"], data_char["bio_char"],
                  data_char["birthdate_char"])

            form.last_name_char.data = data_char["last_name_char"]
            form.first_name_char.data = data_char["first_name_char"]
            form.bio_char.data = data_char["bio_char"]
            form.birthdate_char.data = data_char["birthdate_char"]
            form.icon_char.data = data_char["icon_char"]

    except Exception as Exception_char_update:
        raise ExceptionCharUpdate(f"file : {Path(__file__).name}  ;  "
                                  f"{char_update.__name__} ; "
                                  f"{Exception_char_update}")

    return render_template("chars/char_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /char_delete route
    
    Test : ex : http://127.0.0.1:5005/char_delete
    
    Settings : -
    
    Goal : Delete a characters who has been selected in /chars_display
"""


@app.route("/char_delete", methods=['GET', 'POST'])
def char_delete():
    data_delete = None
    delete_btn = None
    id_char = request.values['id_char']

    form = FormDeleteChar()
    try:
        print(" on submit ", form.validate_on_submit())
        if request.method == "POST" and form.validate_on_submit():

            if form.cancel_btn.data:
                return redirect(url_for("chars_display", order_by="ASC", id_char_sel=0))

            if form.del_conf_btn.data:
                data_delete = session['data_delete']
                print("Data to delete ", data_delete)

                flash(f"Supprimer le personnage définitivement ?", "danger")
                delete_btn = True

            if form.del_final_btn.data:
                delete_dictionary = {"id_char": id_char}
                print("Dictionary : ", delete_dictionary)

                strsql_delete_users_have_char = """DELETE FROM t_users_have_characters WHERE fk_char = %(id_char)s"""
                strsql_delete_id_char = """DELETE FROM t_characters WHERE id_char = %(id_char)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_users_have_char, delete_dictionary)
                    mconn_bd.execute(strsql_delete_id_char, delete_dictionary)

                flash(f"Le personnage a été supprimé !", "success")
                print(f"Characters deleted.")

                return redirect(url_for('chars_display', order_by="ASC", id_char_sel=0))

        if request.method == "GET":
            select_dictionary = {"id_char": id_char}
            print(id_char, type(id_char))

            strsql_users_have_chars_delete = """SELECT id_user_has_char, nickname_user, id_char, id_user FROM t_users u
                                            LEFT JOIN t_users_have_characters ur ON u.id_user = ur.fk_user
                                            LEFT JOIN t_characters r ON ur.fk_char = r.id_char
                                            WHERE ur.fk_char = %(id_char)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(strsql_users_have_chars_delete, select_dictionary)
                data_delete = mydb_conn.fetchall()
                print("Data to delete : ", data_delete)

                session['data_delete'] = data_delete

                strsql_id_char = "SELECT id_char, last_name_char, first_name_char, bio_char, birthdate_char, icon_char FROM t_characters WHERE id_char = %(id_char)s"

                mydb_conn.execute(strsql_id_char, select_dictionary)
                data_name_char = mydb_conn.fetchone()
                print("Data character ", data_name_char, " type ", type(data_name_char), " char ",
                      data_name_char["last_name_char"], data_name_char["first_name_char"], data_name_char["bio_char"],
                      data_name_char["birthdate_char"])

            form.last_name_char.data = data_name_char["last_name_char"]
            form.first_name_char.data = data_name_char["first_name_char"]
            form.bio_char.data = data_name_char["bio_char"]
            form.birthdate_char.data = data_name_char["birthdate_char"]
            form.icon_char.data = data_name_char["icon_char"]

            delete_btn = False

    except Exception as Exception_char_delete:
        raise ExceptionCharDelete(f"file : {Path(__file__).name}  ;  "
                                  f"{char_delete.__name__} ; "
                                  f"{Exception_char_delete}")

    return render_template("chars/char_delete.html",
                           form=form,
                           delete_btn=delete_btn,
                           data_users_linked=data_delete)

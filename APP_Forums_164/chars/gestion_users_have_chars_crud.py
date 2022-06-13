"""Route for chars and users association CRUD
File : gestion_users_have_chars_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from datetime import date
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /update_chars_user_have route

    Test : ex : http://127.0.0.1:5005/update_chars_user_have

    Settings :  id_user = 0 >> all users_have_chars.
                id_user = "n" display users_have_chars who id is "n"
"""


@app.route("/update_chars_user_have", methods=['GET', 'POST'])
def update_chars_user_have():
    if request.method == "GET":
        try:
            id_user = request.values['id_user']
            session['id_user'] = id_user
            id_user = {"id_user": id_user}

            user, chars_user_has_not, chars_user_has = \
                chars_user_has_data(id_user)

            chars_user_has_int = [item['id_char'] for item in chars_user_has]
            session['chars_user_has_int'] = chars_user_has_int

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_chars_user_have.__name__} ; "
                                                  f"{exception_pass}")

    return render_template("chars/update_chars_user_has.html",
                           user=user,
                           chars_user_has=chars_user_has,
                           chars_user_has_not=chars_user_has_not)


@app.route("/update_chars_user_had", methods=['GET', 'POST'])
def update_chars_user_had():
    if request.method == "POST":
        try:
            id_user = session['id_user']
            chars_user_had = session['chars_user_has_int']
            session.clear()

            chars_user_has_int = list(map(int, request.form.getlist('select_tags')))
            chars_user_had_not = list(set(chars_user_had) - set(chars_user_has_int))
            chars_user_has = list(set(chars_user_has_int) - set(chars_user_had))

            with DBconnection() as mconn_bd:
                for id_char in chars_user_has:
                    mconn_bd.execute("""INSERT INTO t_users_have_characters (id_user_has_char, fk_char, fk_user, add_date_user_has_char)
                                                    VALUES (NULL, %(fk_char)s, %(fk_user)s, %(add_date)s)""",
                                     {
                                         "fk_char": id_char,
                                         "fk_user": id_user,
                                         "add_date": date.today()
                                     }
                                     )

                for id_char in chars_user_had_not:
                    mconn_bd.execute("""DELETE FROM t_users_have_characters WHERE fk_char = %(fk_char)s AND fk_user = %(fk_user)s""",
                                     {
                                         "fk_char": id_char,
                                         "fk_user": id_user
                                     }
                                     )

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_chars_user_had.__name__} ; "
                                                  f"{exception_pass}")

    return redirect(url_for('users_display', order_by='ASC', id_user=id_user))


def chars_user_has_data(id_user):
    try:
        with DBconnection() as mc_display:
            mc_display.execute("""SELECT id_char, CONCAT(last_name_char, " ", first_name_char) as name_char FROM t_characters WHERE id_char not in(SELECT id_char as idcharsusers FROM t_users_have_characters
                                                    INNER JOIN t_users ON t_users.id_user = t_users_have_characters.fk_user
                                                    INNER JOIN t_characters ON t_characters.id_char = t_users_have_characters.fk_char
                                                    WHERE id_user = %(id_user)s)
                                                    ORDER BY name_char""", id_user)
            chars_user_has_not_int = mc_display.fetchall()

            mc_display.execute("""SELECT id_user, GROUP_CONCAT(name_email) as name_email, nickname_user, steam_user, discord_user, bio_user, signature_user, icon_user, registration_date_user FROM t_users u
                                        INNER JOIN t_users_have_emails ue ON u.id_user = ue.fk_user
                                        INNER JOIN t_emails e ON e.id_email = ue.fk_email
                                        WHERE id_user = %(id_user)s""", id_user)
            data_user = mc_display.fetchall()

            mc_display.execute("""SELECT id_char, CONCAT(last_name_char, " ", first_name_char) as name_char FROM t_characters WHERE id_char in(SELECT id_char as idcharsusers FROM t_users_have_characters
                                                    INNER JOIN t_users ON t_users.id_user = t_users_have_characters.fk_user
                                                    INNER JOIN t_characters ON t_characters.id_char = t_users_have_characters.fk_char
                                                    WHERE id_user = %(id_user)s)
                                                    ORDER BY name_char""", id_user)
            chars_user_has_int = mc_display.fetchall()

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                             f"{chars_user_has_data.__name__} ; "
                                             f"{exception_pass}")
    return data_user, chars_user_has_not_int, chars_user_has_int

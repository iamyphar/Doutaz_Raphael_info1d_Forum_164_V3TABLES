"""Route for roles and users association CRUD
File : gestion_users_have_roles_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from datetime import date
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /update_roles_user_have route

    Test : ex : http://127.0.0.1:5005/update_roles_user_have

    Settings :  id_user = 0 >> all users_have_roles.
                id_user = "n" display users_have_roles who id is "n"
"""


@app.route("/update_roles_user_have/<int:id_user>", methods=['GET', 'POST'])
def update_roles_user_have(id_user):
    if request.method == "GET":
        try:
            session['id_user'] = id_user
            id_user = {"id_user": id_user}

            user, roles_user_has_not, roles_user_has = \
                roles_user_has_data(id_user)

            roles_user_has_int = [item['id_role'] for item in roles_user_has]
            session['roles_user_has_int'] = roles_user_has_int

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_roles_user_have.__name__} ; "
                                                  f"{exception_pass}")

    return render_template("roles/update_roles_user_has.html",
                           user=user,
                           roles_user_has=roles_user_has,
                           roles_user_has_not=roles_user_has_not)


@app.route("/update_roles_user_had", methods=['GET', 'POST'])
def update_roles_user_had():
    if request.method == "POST":
        try:
            id_user = session['id_user']
            roles_user_had = session['roles_user_has_int']
            session.clear()

            roles_user_has_int = request.form.getlist('select_tags')
            roles_user_has_int = list(map(int, roles_user_has_int))
            roles_user_had_not = list(set(roles_user_had) - set(roles_user_has_int))
            roles_user_has = list(set(roles_user_has_int) - set(roles_user_had))

            with DBconnection() as mconn_bd:
                for id_role in roles_user_has:
                    mconn_bd.execute("""INSERT INTO t_users_have_roles (id_user_has_role, fk_role, fk_user, add_date_user_has_role)
                                                    VALUES (NULL, %(fk_role)s, %(fk_user)s, %(add_date)s)""",
                                     {
                                         "fk_user": id_user,
                                         "fk_role": id_role,
                                         "add_date": date.today()
                                     }
                                     )

                for id_role in roles_user_had_not:
                    mconn_bd.execute("""DELETE FROM t_users_have_roles WHERE fk_role = %(fk_role)s AND fk_user = %(fk_user)s""",
                                     {
                                         "fk_user": id_user,
                                         "fk_role": id_role
                                     }
                                     )

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_roles_user_had.__name__} ; "
                                                  f"{exception_pass}")

    return redirect(url_for('users_display', order_by='ASC', id_user=id_user))


def roles_user_has_data(id_user):
    try:
        with DBconnection() as mc_display:
            mc_display.execute("""SELECT id_role, name_role FROM t_roles WHERE id_role not in(SELECT id_role as idrolesusers FROM t_users_have_roles
                                                    INNER JOIN t_users ON t_users.id_user = t_users_have_roles.fk_user
                                                    INNER JOIN t_roles ON t_roles.id_role = t_users_have_roles.fk_role
                                                    WHERE id_user = %(id_user)s)""", id_user)
            roles_user_has_not_int = mc_display.fetchall()

            mc_display.execute("""SELECT id_user, GROUP_CONCAT(name_email) as name_email, nickname_user, steam_user, discord_user, bio_user, signature_user, icon_user, registration_date_user FROM t_users u
                                        INNER JOIN t_users_have_emails ue ON u.id_user = ue.fk_user
                                        INNER JOIN t_emails e ON e.id_email = ue.fk_email
                                        WHERE id_user = %(id_user)s""", id_user)
            data_user = mc_display.fetchall()

            mc_display.execute("""SELECT id_user, id_role, name_role FROM t_users_have_roles
                                            INNER JOIN t_users ON t_users.id_user = t_users_have_roles.fk_user
                                            INNER JOIN t_roles ON t_roles.id_role = t_users_have_roles.fk_role
                                            WHERE id_user = %(id_user)s""", id_user)
            roles_user_has_int = mc_display.fetchall()

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                             f"{roles_user_has_data.__name__} ; "
                                             f"{exception_pass}")
    return data_user, roles_user_has_not_int, roles_user_has_int

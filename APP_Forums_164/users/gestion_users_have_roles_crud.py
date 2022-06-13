"""Route for roles and users association CRUD
File : gestion_users_have_roles_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from datetime import date
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /users_have_roles_display route
    
    Test : ex : http://127.0.0.1:5005/users_have_roles_display
    
    Settings :  id_user = 0 >> all users_have_roles.
                id_user = "n" display users_have_roles who id is "n"
"""


@app.route("/users_have_roles_display/<int:id_user>", methods=['GET', 'POST'])
def users_have_roles_display(id_user):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                strsql_users_have_roles_display = """SELECT id_user, nickname_user, name_email, steam_user, discord_user, bio_user, signature_user, icon_user, registration_date_user, GROUP_CONCAT(DISTINCT name_role) as name_role, GROUP_CONCAT(DISTINCT CONCAT(last_name_char, " ", first_name_char)) as name_char FROM t_users 
                                                                            LEFT JOIN t_users_have_roles ur ON id_user = ur.fk_user
                                                                            LEFT JOIN t_users_have_emails ue ON id_user = ue.fk_user
                                                                            LEFT JOIN t_users_have_characters uc ON id_user = uc.fk_user
                                                                            LEFT JOIN t_characters ON id_char = fk_char
                                                                            LEFT JOIN t_emails ON id_email = fk_email
                                                                            LEFT JOIN t_roles ON id_role = fk_role
                                                                            GROUP BY id_user, id_email"""
                if id_user == 0:
                    mc_display.execute(strsql_users_have_roles_display)
                else:
                    id_user_dictionary = {"id_user": id_user}
                    strsql_users_have_roles_display += """ HAVING id_user = %(id_user)s"""

                    mc_display.execute(strsql_users_have_roles_display, id_user_dictionary)

                data_users_have_roles = mc_display.fetchall()

                if not data_users_have_roles and id_user == 0:
                    flash("""La table "t_users_have_roles" est vide.""", "warning")
                elif not data_users_have_roles and id_user > 0:
                    flash(f"L'utilisateur que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des utilisateurs ont été affichées !", "success")

        except Exception as Exception_users_have_roles_display:
            raise ExceptionUsersHaveRolesDisplay(f"file : {Path(__file__).name}  ;  "
                                                 f"{users_have_roles_display.__name__} ; "
                                                 f"{Exception_users_have_roles_display}")

    return render_template("users/users_display.html", data=data_users_have_roles)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /update_roles_user_have route

    Test : ex : http://127.0.0.1:5005/update_roles_user_have

    Settings :  id_user = 0 >> all users_have_roles.
                id_user = "n" display users_have_roles who id is "n"
"""


@app.route("/update_roles_user_have", methods=['GET', 'POST'])
def update_roles_user_have():
    if request.method == "GET":
        try:
            id_user = request.values['id_user']
            session['id_user'] = id_user
            id_user = {"id_user": id_user}

            user, roles_user_has_not, roles_user_has = \
                roles_user_has_data(id_user)

            roles_user_has_int = [item['id_role'] for item in roles_user_has]
            session['roles_user_has_int'] = roles_user_has_int

        except Exception as Exception_update_roles_user_have:
            raise ExceptionUpdateRoleUserSelected(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_roles_user_have.__name__} ; "
                                                  f"{Exception_update_roles_user_have}")

    return render_template("users/update_roles_user_has.html",
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

            strsql_insert_users_have_roles = """INSERT INTO t_users_have_roles (id_user_has_role, fk_role, fk_user, add_date_user_has_role)
                                                    VALUES (NULL, %(fk_role)s, %(fk_user)s, %(add_date)s)"""

            strsql_delete_users_have_roles = """DELETE FROM t_users_have_roles WHERE fk_role = %(fk_role)s AND fk_user = %(fk_user)s"""

            with DBconnection() as mconn_bd:
                for id_role in roles_user_has:
                    users_have_roles_dictionary = {"fk_user": id_user,
                                                   "fk_role": id_role,
                                                   "add_date": date.today()}

                    mconn_bd.execute(strsql_insert_users_have_roles, users_have_roles_dictionary)

                for id_role in roles_user_had_not:
                    users_have_roles_dictionary = {"fk_user": id_user,
                                                   "fk_role": id_role}

                    mconn_bd.execute(strsql_delete_users_have_roles, users_have_roles_dictionary)

        except Exception as Exception_update_role_user_selected:
            raise ExceptionUpdateRoleUserSelected(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_roles_user_had.__name__} ; "
                                                  f"{Exception_update_role_user_selected}")

    return redirect(url_for('users_have_roles_display', id_user=id_user))


def roles_user_has_data(id_user):
    try:
        strsql_user = """SELECT id_user, GROUP_CONCAT(name_email) as name_email, nickname_user, steam_user, discord_user, bio_user, signature_user, icon_user, registration_date_user FROM t_users u
                                        INNER JOIN t_users_have_emails ue ON u.id_user = ue.fk_user
                                        INNER JOIN t_emails e ON e.id_email = ue.fk_email
                                        WHERE id_user = %(id_user)s"""

        strsql_roles_user_had_not = """SELECT id_role, name_role FROM t_roles WHERE id_role not in(SELECT id_role as idrolesusers FROM t_users_have_roles
                                                    INNER JOIN t_users ON t_users.id_user = t_users_have_roles.fk_user
                                                    INNER JOIN t_roles ON t_roles.id_role = t_users_have_roles.fk_role
                                                    WHERE id_user = %(id_user)s)"""

        strsql_roles_user_had = """SELECT id_user, id_role, name_role FROM t_users_have_roles
                                            INNER JOIN t_users ON t_users.id_user = t_users_have_roles.fk_user
                                            INNER JOIN t_roles ON t_roles.id_role = t_users_have_roles.fk_role
                                            WHERE id_user = %(id_user)s"""

        with DBconnection() as mc_display:
            mc_display.execute(strsql_roles_user_had_not, id_user)
            roles_user_has_not_int = mc_display.fetchall()

            mc_display.execute(strsql_user, id_user)
            data_user = mc_display.fetchall()

            mc_display.execute(strsql_roles_user_had, id_user)
            roles_user_has_int = mc_display.fetchall()

    except Exception as Exception_roles_user_has_int_data:
        raise ExceptionRolesUsersDisplayData(f"file : {Path(__file__).name}  ;  "
                                             f"{roles_user_has_data.__name__} ; "
                                             f"{Exception_roles_user_has_int_data}")
    return data_user, roles_user_has_not_int, roles_user_has_int

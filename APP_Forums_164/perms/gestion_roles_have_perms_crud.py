"""Route for perms and roles association CRUD
File : gestion_roles_have_perms_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /update_perms_role_have route

    Test : ex : http://127.0.0.1:5005/update_perms_role_have

    Settings :  id_role = 0 >> all roles_have_perms.
                id_role = "n" display roles_have_perms who id is "n"
"""


@app.route("/update_perms_role_have", methods=['GET', 'POST'])
def update_perms_role_have():
    if request.method == "GET":
        try:
            id_role = request.values['id_role']
            session['id_role'] = id_role
            id_role = {"id_role": id_role}

            role, perms_role_has_not, perms_role_has = \
                perms_role_has_data(id_role)

            perms_role_has_int = [item['id_perm'] for item in perms_role_has]
            session['perms_role_has_int'] = perms_role_has_int

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_perms_role_have.__name__} ; "
                                                  f"{exception_pass}")

    return render_template("perms/update_perms_role_has.html",
                           role=role,
                           perms_role_has=perms_role_has,
                           perms_role_has_not=perms_role_has_not)


@app.route("/update_perms_role_had", methods=['GET', 'POST'])
def update_perms_role_had():
    if request.method == "POST":
        try:
            id_role = session['id_role']
            perms_role_had = session['perms_role_has_int']
            session.clear()

            perms_role_has_int = request.form.getlist('select_tags')
            perms_role_has_int = list(map(int, perms_role_has_int))
            perms_role_had_not = list(set(perms_role_had) - set(perms_role_has_int))
            perms_role_has = list(set(perms_role_has_int) - set(perms_role_had))

            strsql_insert_roles_have_permissions = """INSERT INTO t_roles_have_permissions (id_role_has_perm, fk_perm, fk_role)
                                                    VALUES (NULL, %(fk_perm)s, %(fk_role)s)"""

            strsql_delete_roles_have_perms = """DELETE FROM t_roles_have_permissions WHERE fk_perm = %(fk_perm)s AND fk_role = %(fk_role)s"""

            with DBconnection() as mconn_bd:
                for id_perm in perms_role_has:
                    roles_have_perms_dictionary = {"fk_perm": id_perm,
                                                   "fk_role": id_role}

                    mconn_bd.execute(strsql_insert_roles_have_permissions, roles_have_perms_dictionary)

                for id_perm in perms_role_had_not:
                    roles_have_perms_dictionary = {"fk_perm": id_perm,
                                                   "fk_role": id_role}

                    mconn_bd.execute(strsql_delete_roles_have_perms, roles_have_perms_dictionary)

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                                  f"{update_perms_role_had.__name__} ; "
                                                  f"{exception_pass}")

    return redirect(url_for('roles_display', order_by='ASC', id_role=id_role))


def perms_role_has_data(id_role):
    try:
        strsql_role = """SELECT id_role, name_role FROM t_roles
                                        WHERE id_role = %(id_role)s"""

        strsql_perms_role_had_not = """SELECT id_perm, name_perm FROM t_permissions WHERE id_perm not in(SELECT id_perm as idpermsroles FROM t_roles_have_permissions
                                                    INNER JOIN t_roles ON t_roles.id_role = t_roles_have_permissions.fk_role
                                                    INNER JOIN t_permissions ON t_permissions.id_perm = t_roles_have_permissions.fk_perm
                                                    WHERE id_role = %(id_role)s)"""

        strsql_perms_role_had = """SELECT id_perm, name_perm FROM t_permissions WHERE id_perm in(SELECT id_perm as idpermsroles FROM t_roles_have_permissions
                                                    INNER JOIN t_roles ON t_roles.id_role = t_roles_have_permissions.fk_role
                                                    INNER JOIN t_permissions ON t_permissions.id_perm = t_roles_have_permissions.fk_perm
                                                    WHERE id_role = %(id_role)s)"""

        with DBconnection() as mc_display:
            mc_display.execute(strsql_perms_role_had_not, id_role)
            perms_role_has_not_int = mc_display.fetchall()

            mc_display.execute(strsql_role, id_role)
            data_role = mc_display.fetchall()

            mc_display.execute(strsql_perms_role_had, id_role)
            perms_role_has_int = mc_display.fetchall()

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                             f"{perms_role_has_data.__name__} ; "
                                             f"{exception_pass}")
    return data_role, perms_role_has_not_int, perms_role_has_int

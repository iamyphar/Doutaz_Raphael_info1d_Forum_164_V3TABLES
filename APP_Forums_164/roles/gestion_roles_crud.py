"""Route for roles CRUD
File : gestion_roles_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.roles.gestion_roles_forms import FormRole

"""
    Author : Raphaël Doutaz 09.05.22
    Set /roles_display route
    
    Test : ex : http://127.0.0.1:5005/roles_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_role = 0 >> all roles.
                id_role = "n" display roles who id is "n"
"""


@app.route("/roles_display/<string:order_by>/<int:id_role>", methods=['GET', 'POST'])
def roles_display(order_by, id_role):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                strsql_roles_display = """SELECT id_role, name_role, GROUP_CONCAT(DISTINCT name_perm ORDER BY name_perm) as name_perm FROM t_roles 
                                                                            LEFT JOIN t_roles_have_permissions ON id_role = fk_role
                                                                            LEFT JOIN t_permissions ON id_perm = fk_perm
                                                                            GROUP BY id_role"""
                if order_by == "ASC" and id_role == 0:
                    strsql_roles_display += """ ORDER BY id_role ASC"""
                    mc_display.execute(strsql_roles_display)
                elif order_by == "ASC":
                    strsql_roles_display += """ HAVING id_role = %(id_role)s"""
                    mc_display.execute(strsql_roles_display, {"id_role": id_role})
                else:
                    strsql_roles_display += """ ORDER BY id_role DESC"""
                    mc_display.execute(strsql_roles_display)

                data = mc_display.fetchall()

                if not data and id_role == 0:
                    flash("""La table "t_roles" est vide.""", "warning")
                elif not data and id_role > 0:
                    flash(f"Le rôle que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des rôles ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                                 f"{roles_display.__name__} ; "
                                                 f"{exception_pass}")

    return render_template("roles/roles_display.html", data=data)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /role_add route
    
    Test : ex : http://127.0.0.1:5005/role_add
    
    Settings : -
    
    Goal : Add a role
"""


@app.route("/role_add", methods=['GET', 'POST'])
def role_add():
    form = FormRole()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""INSERT INTO t_roles (id_role,name_role) VALUES (NULL,%(name_role)s)""", {"name_role": form.name_role.data})

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('roles_display', order_by='ASC', id_role=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                   f"{role_add.__name__} ; "
                                   f"{exception_pass}")

    return render_template("roles/role_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /role_update route
    
    Test : ex : http://127.0.0.1:5005/role_update
    
    Settings : -
    
    Goal : Update a role who has been selected in /roles_display
"""


@app.route("/role_update/<int:id_role>", methods=['GET', 'POST'])
def role_update(id_role):
    form = FormRole()
    try:
        if form.validate_on_submit():
            with DBconnection() as mconn_bd:
                mconn_bd.execute("""UPDATE t_roles SET name_role = %(name_role)s WHERE id_role = %(id_role)s;""",
                                 {
                                     "id_role": id_role,
                                     "name_role": form.name_role.data
                                 }
                                 )

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('roles_display', order_by='ASC', id_role=id_role))

        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute("SELECT id_role, name_role FROM t_roles WHERE id_role = %(id_role)s", {"id_role": id_role})
            data = mybd_conn.fetchone()
            print("Data roles ", data, " type ")

            form.name_role.data = data["name_role"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                  f"{role_update.__name__} ; "
                                  f"{exception_pass}")

    return render_template("roles/role_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /role_delete route
    
    Test : ex : http://127.0.0.1:5005/role_delete
    
    Settings : -
    
    Goal : Delete a role who has been selected in /roles_display
"""


@app.route("/role_delete/<int:id_role>", methods=['GET', 'POST'])
def role_delete(id_role):
    form = FormRole()
    try:
        if request.method == "POST" and form.validate_on_submit():
            if form.submit_cancel.data:
                return redirect(url_for("roles_display", order_by='ASC', id_role=0))

            if form.submit_delete.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""DELETE FROM t_users_have_roles WHERE fk_role = %(id_role)s;DELETE FROM t_roles_have_permissions WHERE fk_role = %(id_role)s;DELETE FROM t_roles WHERE id_role = %(id_role)s""", {"id_role": id_role})

                flash(f"Le rôle a été supprimé !", "success")
                print(f"Roles deleted.")

                return redirect(url_for('roles_display', order_by='ASC', id_role=0))

        if request.method == "GET":
            with DBconnection() as mydb_conn:
                mydb_conn.execute("""SELECT id_user_has_role, nickname_user, id_role, id_user FROM t_users u
                                            LEFT JOIN t_users_have_roles ur ON u.id_user = ur.fk_user
                                            LEFT JOIN t_roles r ON ur.fk_role = r.id_role
                                            WHERE ur.fk_role = %(id_role)s""", {"id_role": id_role})
                data_linked = mydb_conn.fetchall()
                session['data_linked'] = data_linked

                mydb_conn.execute("SELECT id_role, name_role FROM t_roles WHERE id_role = %(id_role)s", {"id_role": id_role})
                data = mydb_conn.fetchone()
                print("Data role ", data)

            form.name_role.data = data["name_role"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                  f"{role_delete.__name__} ; "
                                  f"{exception_pass}")

    return render_template("roles/role_delete.html",
                           form=form,
                           data_linked=data_linked)

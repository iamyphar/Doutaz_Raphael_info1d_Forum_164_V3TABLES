"""Route for roles CRUD
File : gestion_roles_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.roles.gestion_roles_forms import FormAddRole
from APP_Forums_164.roles.gestion_roles_forms import FormDeleteRole
from APP_Forums_164.roles.gestion_roles_forms import FormUpdateRole

"""
    Author : Raphaël Doutaz 09.05.22
    Set /roles_have_perms_display route
    
    Test : ex : http://127.0.0.1:5005/roles_have_perms_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_role_sel = 0 >> all roles.
                id_role_sel = "n" display roles who id is "n"
"""

@app.route("/roles_have_perms_display/<int:id_role>", methods=['GET', 'POST'])
def roles_have_perms_display(id_role):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                strsql_roles_have_perms_display = """SELECT id_role, name_role, GROUP_CONCAT(DISTINCT name_perm) as name_perm FROM t_roles 
                                                                            LEFT JOIN t_roles_have_permissions ON id_role = fk_role
                                                                            LEFT JOIN t_permissions ON id_perm = fk_perm
                                                                            GROUP BY id_role"""
                if id_role == 0:
                    mc_display.execute(strsql_roles_have_perms_display)
                else:
                    id_role_dictionary = {"id_role": id_role}
                    strsql_roles_have_perms_display += """ HAVING id_role = %(id_role)s"""

                    mc_display.execute(strsql_roles_have_perms_display, id_role_dictionary)

                data_roles_have_perms = mc_display.fetchall()

                if not data_roles_have_perms and id_role == 0:
                    flash("""La table "t_roles_have_permissions" est vide.""", "warning")
                elif not data_roles_have_perms and id_role > 0:
                    flash(f"L'utilisateur que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des utilisateurs ont été affichées !", "success")

        except Exception as Exception_roles_have_perms_display:
            raise ExceptionRolesHavePermsDisplay(f"file : {Path(__file__).name}  ;  "
                                                 f"{roles_have_perms_display.__name__} ; "
                                                 f"{Exception_roles_have_perms_display}")

    return render_template("roles/roles_display.html", data=data_roles_have_perms)

"""
    Author : Raphaël Doutaz 09.05.22
    Set /role_add route
    
    Test : ex : http://127.0.0.1:5005/role_add
    
    Settings : -
    
    Goal : Add a roles
"""


@app.route("/role_add", methods=['GET', 'POST'])
def role_add():
    form = FormAddRole()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                insertion_dictionary = {"name_role": form.name_role.data}
                print("Dictionary : ", insertion_dictionary)

                strsql_insert_role = """INSERT INTO t_roles (id_role,name_role) VALUES (NULL,%(name_role)s) """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_role, insertion_dictionary)

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('roles_have_perms_display', id_role=0))

        except Exception as Exception_roles_add:
            raise ExceptionRoleAdd(f"file : {Path(__file__).name}  ;  "
                                   f"{role_add.__name__} ; "
                                   f"{Exception_roles_add}")

    return render_template("roles/role_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /role_update route
    
    Test : ex : http://127.0.0.1:5005/role_update
    
    Settings : -
    
    Goal : Update a roles who has been selected in /roles_have_perms_display
"""


@app.route("/role_update", methods=['GET', 'POST'])
def role_update():
    id_role = request.values['id_role']

    form = FormUpdateRole()
    try:
        print(" on submit ", form.validate_on_submit())
        if form.validate_on_submit():
            update_dictionary = {"id_role": id_role,
                                 "name_role": form.name_role.data
                                 }
            print("Dictionnary : ", update_dictionary)

            strsql_update_role = """UPDATE t_roles SET name_role = %(name_role)s WHERE id_role = %(id_role)s;"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_role, update_dictionary)

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('roles_have_perms_display', id_role=id_role))
        elif request.method == "GET":
            strsql_id_role = "SELECT id_role, name_role FROM t_roles WHERE id_role = %(id_role)s"
            select_dictionary = {"id_role": id_role}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(strsql_id_role, select_dictionary)
            data_role = mybd_conn.fetchone()
            print("Data roles ", data_role, " type ", type(data_role), " role ",
                  data_role["name_role"])

            form.name_role.data = data_role["name_role"]

    except Exception as Exception_role_update:
        raise ExceptionRoleUpdate(f"file : {Path(__file__).name}  ;  "
                                  f"{role_update.__name__} ; "
                                  f"{Exception_role_update}")

    return render_template("roles/role_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /role_delete route
    
    Test : ex : http://127.0.0.1:5005/role_delete
    
    Settings : -
    
    Goal : Delete a roles who has been selected in /roles_have_perms_display
"""


@app.route("/role_delete", methods=['GET', 'POST'])
def role_delete():
    data_delete = None
    delete_btn = None
    id_role = request.values['id_role']

    form = FormDeleteRole()
    try:
        print(" on submit ", form.validate_on_submit())
        if request.method == "POST" and form.validate_on_submit():

            if form.cancel_btn.data:
                return redirect(url_for("roles_have_perms_display", id_role=0))

            if form.del_conf_btn.data:
                data_delete = session['data_delete']
                print("Data to delete ", data_delete)

                flash(f"Supprimer le rôle définitivement ?", "danger")
                delete_btn = True

            if form.del_final_btn.data:
                delete_dictionary = {"id_role": id_role}
                print("Dictionary : ", delete_dictionary)

                strsql_delete_users_have_role = """DELETE FROM t_users_have_roles WHERE fk_role = %(id_role)s"""
                strsql_delete_id_role = """DELETE FROM t_roles WHERE id_role = %(id_role)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_users_have_role, delete_dictionary)
                    mconn_bd.execute(strsql_delete_id_role, delete_dictionary)

                flash(f"Le rôle a été supprimé !", "success")
                print(f"Roles deleted.")

                return redirect(url_for('roles_have_perms_display', id_role=0))

        if request.method == "GET":
            select_dictionary = {"id_role": id_role}
            print(id_role, type(id_role))

            strsql_users_have_roles_delete = """SELECT id_user_has_role, nickname_user, id_role, id_user FROM t_users u
                                            LEFT JOIN t_users_have_roles ur ON u.id_user = ur.fk_user
                                            LEFT JOIN t_roles r ON ur.fk_role = r.id_role
                                            WHERE ur.fk_role = %(id_role)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(strsql_users_have_roles_delete, select_dictionary)
                data_delete = mydb_conn.fetchall()
                print("Data to delete : ", data_delete)

                session['data_delete'] = data_delete

                strsql_id_role = "SELECT id_role, name_role FROM t_roles WHERE id_role = %(id_role)s"

                mydb_conn.execute(strsql_id_role, select_dictionary)
                data_name_role = mydb_conn.fetchone()
                print("Data role ", data_name_role, " type ", type(data_name_role), " role ",
                      data_name_role["name_role"])

            form.name_role.data = data_name_role["name_role"]

            delete_btn = False

    except Exception as Exception_role_delete:
        raise ExceptionRoleDelete(f"file : {Path(__file__).name}  ;  "
                                  f"{role_delete.__name__} ; "
                                  f"{Exception_role_delete}")

    return render_template("roles/role_delete.html",
                           form=form,
                           delete_btn=delete_btn,
                           data_users_linked=data_delete)

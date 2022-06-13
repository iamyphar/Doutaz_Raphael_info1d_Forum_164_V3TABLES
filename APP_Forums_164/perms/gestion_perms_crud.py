"""Route for permissions CRUD
File : gestion_perms_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_Forums_164.perms.gestion_perms_forms import FormAddPerm
from APP_Forums_164.perms.gestion_perms_forms import FormDeletePerm
from APP_Forums_164.perms.gestion_perms_forms import FormUpdatePerm
from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /perms_display route
    
    Test : ex : http://127.0.0.1:5005/perms_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_perm_sel = 0 >> all permissions.
                id_perm_sel = "n" display permissions who id is "n"
"""


@app.route("/perms_display/<string:order_by>/<int:id_perm_sel>", methods=['GET', 'POST'])
def perms_display(order_by, id_perm_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_perm_sel == 0:
                    strsql_perms_display = """SELECT id_perm, name_perm, description_perm FROM t_permissions ORDER BY name_perm ASC"""
                    mc_display.execute(strsql_perms_display)
                elif order_by == "ASC":
                    select_dictionary = {"id_perm_selected": id_perm_sel}
                    strsql_perms_display = """SELECT id_perm, name_perm, description_perm FROM t_permissions WHERE id_perm = %(id_perm_selected)s"""

                    mc_display.execute(strsql_perms_display, select_dictionary)
                else:
                    strsql_perms_display = """SELECT id_perm, name_perm, description_perm FROM t_permissions  ORDER BY id_perm DESC"""

                    mc_display.execute(strsql_perms_display)

                data_perms = mc_display.fetchall()

                print("Data permissions : ", data_perms, " Type : ", type(data_perms))

                # If table is empty
                if not data_perms and id_perm_sel == 0:
                    flash("""La table "t_permissions" est vide.""", "warning")
                elif not data_perms and id_perm_sel > 0:
                    # If no permissions with id = id_perm_sel found
                    flash(f"la permission que vous avez demandé n'existe pas.", "warning")
                else:
                    # In all others cases, this means the table is empty.
                    flash(f"Les données des permissions ont été affichées !", "success")

        except Exception as Exception_perms_display:
            raise ExceptionPermsDisplay(f"file : {Path(__file__).name}  ;  "
                                        f"{perms_display.__name__} ; "
                                        f"{Exception_perms_display}")

    return render_template("perms/perms_display.html", data=data_perms)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /perm_add route
    
    Test : ex : http://127.0.0.1:5005/perm_add
    
    Settings : -
    
    Goal : Add a permissions
"""


@app.route("/perm_add", methods=['GET', 'POST'])
def perm_add():
    form = FormAddPerm()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                insertion_dictionary = {"name_perm": form.name_perm.data,
                                        "description_perm": form.description_perm.data}
                print("Dictionary : ", insertion_dictionary)

                strsql_insert_perm = """INSERT INTO t_permissions (id_perm,name_perm, description_perm) VALUES (NULL,%(name_perm)s,%(description_perm)s) """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_perm, insertion_dictionary)

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('perms_display', order_by='DESC', id_perm_sel=0))

        except Exception as Exception_perm_add:
            raise ExceptionPermAdd(f"file : {Path(__file__).name}  ;  "
                                   f"{perm_add.__name__} ; "
                                   f"{Exception_perm_add}")

    return render_template("perms/perm_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /perm_update route
    
    Test : ex : http://127.0.0.1:5005/perm_update
    
    Settings : -
    
    Goal : Update a permissions who has been selected in /perms_display
"""


@app.route("/perm_update", methods=['GET', 'POST'])
def perm_update():
    id_perm = request.values['id_perm']

    form = FormUpdatePerm()
    try:
        print(" on submit ", form.validate_on_submit())
        if form.validate_on_submit():
            update_dictionary = {"id_perm": id_perm,
                                 "name_perm": form.name_perm.data,
                                 "description_perm": form.description_perm.data,
                                 }
            print("Dictionnary : ", update_dictionary)

            strsql_update_perm = """UPDATE t_permissions SET name_perm = %(name_perm)s, description_perm = %(description_perm)s WHERE id_perm = %(id_perm)s;"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_perm, update_dictionary)

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('perms_display', order_by="ASC", id_perm_sel=id_perm))
        elif request.method == "GET":
            strsql_id_perm = "SELECT id_perm, name_perm, description_perm FROM t_permissions WHERE id_perm = %(id_perm)s"
            select_dictionary = {"id_perm": id_perm}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(strsql_id_perm, select_dictionary)
            data_perm = mybd_conn.fetchone()
            print("Data permissions ", data_perm, " type ", type(data_perm), " perm ", data_perm["name_perm"], data_perm["description_perm"],)

            form.name_perm.data = data_perm["name_perm"]
            form.description_perm.data = data_perm["description_perm"]

    except Exception as Exception_perm_update:
        raise ExceptionPermUpdate(f"file : {Path(__file__).name}  ;  "
                                  f"{perm_update.__name__} ; "
                                  f"{Exception_perm_update}")

    return render_template("perms/perm_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /perm_delete route
    
    Test : ex : http://127.0.0.1:5005/perm_delete
    
    Settings : -
    
    Goal : Delete a permissions who has been selected in /perms_display
"""


@app.route("/perm_delete", methods=['GET', 'POST'])
def perm_delete():
    data_delete = None
    delete_btn = None
    id_perm = request.values['id_perm']

    form = FormDeletePerm()
    try:
        print(" on submit ", form.validate_on_submit())
        if request.method == "POST" and form.validate_on_submit():

            if form.cancel_btn.data:
                return redirect(url_for("perms_display", order_by="ASC", id_perm_sel=0))

            if form.del_conf_btn.data:
                data_delete = session['data_delete']
                print("Data to delete ", data_delete)

                flash(f"Supprimer la permission définitivement ?", "danger")
                delete_btn = True

            if form.del_final_btn.data:
                delete_dictionary = {"id_perm": id_perm}
                print("Dictionary : ", delete_dictionary)

                strsql_delete_roles_have_perm = """DELETE FROM t_roles_have_permissions WHERE fk_perm = %(id_perm)s"""
                strsql_delete_id_perm = """DELETE FROM t_permissions WHERE id_perm = %(id_perm)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_roles_have_perm, delete_dictionary)
                    mconn_bd.execute(strsql_delete_id_perm, delete_dictionary)

                flash(f"la permission a été supprimé !", "success")
                print(f"Permissions deleted.")

                return redirect(url_for('perms_display', order_by="ASC", id_perm_sel=0))

        if request.method == "GET":
            select_dictionary = {"id_perm": id_perm}
            print(id_perm, type(id_perm))

            strsql_roles_have_perms_delete = """SELECT id_role_has_perm, name_role, id_perm, id_role FROM t_roles u
                                            LEFT JOIN t_roles_have_permissions ur ON u.id_role = ur.fk_role
                                            LEFT JOIN t_permissions r ON ur.fk_perm = r.id_perm
                                            WHERE ur.fk_perm = %(id_perm)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(strsql_roles_have_perms_delete, select_dictionary)
                data_delete = mydb_conn.fetchall()
                print("Data to delete : ", data_delete)

                session['data_delete'] = data_delete

                strsql_id_perm = "SELECT id_perm, name_perm, description_perm FROM t_permissions WHERE id_perm = %(id_perm)s"

                mydb_conn.execute(strsql_id_perm, select_dictionary)
                data_name_perm = mydb_conn.fetchone()
                print("Data permission ", data_name_perm, " type ", type(data_name_perm), " perm ",
                      data_name_perm["name_perm"], data_name_perm["description_perm"])

            form.name_perm.data = data_name_perm["name_perm"]
            form.description_perm.data = data_name_perm["description_perm"]

            delete_btn = False

    except Exception as Exception_perm_delete:
        raise ExceptionPermDelete(f"file : {Path(__file__).name}  ;  "
                                  f"{perm_delete.__name__} ; "
                                  f"{Exception_perm_delete}")

    return render_template("perms/perm_delete.html",
                           form=form,
                           delete_btn=delete_btn,
                           data_roles_linked=data_delete)

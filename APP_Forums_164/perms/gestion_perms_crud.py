"""Route for permissions CRUD
File : gestion_perms_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.perms.gestion_perms_forms import FormPerm

"""
    Author : Raphaël Doutaz 09.05.22
    Set /perms_display route
    
    Test : ex : http://127.0.0.1:5005/perms_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_perm = 0 >> all permissions.
                id_perm = "n" display permissions who id is "n"
"""


@app.route("/perms_display/<string:order_by>/<int:id_perm>", methods=['GET', 'POST'])
def perms_display(order_by, id_perm):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_perm == 0:
                    mc_display.execute("""SELECT id_perm, name_perm, description_perm FROM t_permissions ORDER BY id_perm ASC""")
                elif order_by == "ASC":
                    mc_display.execute("""SELECT id_perm, name_perm, description_perm FROM t_permissions WHERE id_perm = %(id_perm)s ORDER BY id_perm ASC""", 
                                       {"id_perm": id_perm})
                else:
                    mc_display.execute("""SELECT id_perm, name_perm, description_perm FROM t_permissions ORDER BY id_perm DESC""")

                data = mc_display.fetchall()

                print("Data permissions : ", data)

                if not data and id_perm == 0:
                    flash("""La table "t_permissions" est vide.""", "warning")
                elif not data and id_perm > 0:
                    flash(f"La permission que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des permissions ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                        f"{perms_display.__name__} ; "
                                        f"{exception_pass}")

    return render_template("perms/perms_display.html", data=data)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /perm_add route
    
    Test : ex : http://127.0.0.1:5005/perm_add
    
    Settings : -
    
    Goal : Add a permission
"""


@app.route("/perm_add", methods=['GET', 'POST'])
def perm_add():
    form = FormPerm()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""INSERT INTO t_permissions (id_perm,name_perm, description_perm) VALUES (NULL,%(name_perm)s,%(description_perm)s) """,
                                     {
                                        "name_perm": form.name_perm.data,
                                        "description_perm": form.description_perm.data
                                     }
                                     )

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('perms_display', order_by='ASC', id_perm=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                   f"{perm_add.__name__} ; "
                                   f"{exception_pass}")

    return render_template("perms/perm_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /perm_update route
    
    Test : ex : http://127.0.0.1:5005/perm_update
    
    Settings : -
    
    Goal : Update a permission who has been selected in /perms_display
"""


@app.route("/perm_update/<int:id_perm>", methods=['GET', 'POST'])
def perm_update(id_perm):
    form = FormPerm()
    try:
        if form.validate_on_submit():
            with DBconnection() as mconn_bd:
                mconn_bd.execute("""UPDATE t_permissions SET name_perm = %(name_perm)s, description_perm = %(description_perm)s WHERE id_perm = %(id_perm)s;""", 
                                 {
                                    "id_perm": id_perm,
                                    "name_perm": form.name_perm.data,
                                    "description_perm": form.description_perm.data,
                                 }
                                 )

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('perms_display', order_by="ASC", id_perm=id_perm))
        
        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute("SELECT id_perm, name_perm, description_perm FROM t_permissions WHERE id_perm = %(id_perm)s", {"id_perm": id_perm})
            data = mybd_conn.fetchone()
            print("Data permissions ", data)

            form.name_perm.data = data["name_perm"]
            form.description_perm.data = data["description_perm"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                  f"{perm_update.__name__} ; "
                                  f"{exception_pass}")

    return render_template("perms/perm_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /perm_delete route
    
    Test : ex : http://127.0.0.1:5005/perm_delete
    
    Settings : -
    
    Goal : Delete a permission who has been selected in /perms_display
"""


@app.route("/perm_delete/<int:id_perm>", methods=['GET', 'POST'])
def perm_delete(id_perm):
    form = FormPerm()
    try:
        if request.method == "POST" and form.validate_on_submit():

            if form.submit_cancel.data:
                return redirect(url_for("perms_display", order_by="ASC", id_perm=0))

            if form.submit_delete.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""DELETE FROM t_roles_have_permissions WHERE fk_perm = %(id_perm)s;DELETE FROM t_permissions WHERE id_perm = %(id_perm)s""", {"id_perm": id_perm})

                flash(f"La permission a été supprimé !", "success")
                print(f"Permissions deleted.")

                return redirect(url_for('perms_display', order_by="ASC", id_perm=0))

        if request.method == "GET":
            with DBconnection() as mydb_conn:
                mydb_conn.execute("""SELECT id_role_has_perm, name_role, id_perm, id_role FROM t_roles u
                                            LEFT JOIN t_roles_have_permissions ur ON u.id_role = ur.fk_role
                                            LEFT JOIN t_permissions r ON ur.fk_perm = r.id_perm
                                            WHERE ur.fk_perm = %(id_perm)s""", {"id_perm": id_perm})
                data_linked = mydb_conn.fetchall()
                session['data_linked'] = data_linked

                mydb_conn.execute("SELECT id_perm, name_perm, description_perm FROM t_permissions WHERE id_perm = %(id_perm)s", {"id_perm": id_perm})
                data = mydb_conn.fetchone()
                print("Data permission ", data)

            form.name_perm.data = data["name_perm"]
            form.description_perm.data = data["description_perm"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                  f"{perm_delete.__name__} ; "
                                  f"{exception_pass}")

    return render_template("perms/perm_delete.html",
                           form=form,
                           data_linked=data_linked)

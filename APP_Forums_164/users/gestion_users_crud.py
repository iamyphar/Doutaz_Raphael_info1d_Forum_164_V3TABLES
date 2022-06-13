"""Route for users CRUD
File : gestion_users_crud.py
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
from APP_Forums_164.users.gestion_users_forms import FormAddUser
from APP_Forums_164.users.gestion_users_forms import FormDeleteUser
from APP_Forums_164.users.gestion_users_forms import FormUpdateUser

"""
    Author : Raphaël Doutaz 09.05.22
    Set /user_add route
    
    Test : ex : http://127.0.0.1:5005/user_add
    
    Settings : -
    
    Goal : Add a users
"""


@app.route("/user_add", methods=['GET', 'POST'])
def user_add():
    form = FormAddUser()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                insertion_dictionary = {"password_user": form.password_user.data,
                                        "nickname_user": form.nickname_user.data,
                                        "name_email": form.name_email.data,
                                        "bio_user": form.bio_user.data,
                                        "signature_user": form.signature_user.data,
                                        "discord_user": form.discord_user.data,
                                        "steam_user": form.steam_user.data,
                                        "registration_date_user": date.today(),
                                        "icon_user": form.icon_user.data}
                print("Dictionary : ", insertion_dictionary)

                strsql_insert_user = """INSERT INTO t_users (id_user,nickname_user, password_user, bio_user, registration_date_user, icon_user, signature_user,discord_user, steam_user) VALUES (NULL,%(nickname_user)s,%(password_user)s,%(bio_user)s,%(registration_date_user)s,%(icon_user)s,%(signature_user)s,%(discord_user)s,%(steam_user)s); 
                INSERT INTO t_emails (id_email, name_email) VALUES (NULL,%(name_email)s);
                INSERT INTO t_users_have_emails (id_user_has_email,fk_user,fk_email,add_date_user_has_email) VALUES (NULL,(SELECT id_user FROM t_users WHERE nickname_user = %(nickname_user)s ORDER BY id_user DESC LIMIT 1),(SELECT id_email FROM t_emails WHERE name_email = %(name_email)s ORDER BY id_email DESC LIMIT 1),%(registration_date_user)s)"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_user, insertion_dictionary)

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('users_have_roles_display', id_user=0))

        except Exception as Exception_user_add:
            raise ExceptionUserAdd(f"file : {Path(__file__).name}  ;  "
                                   f"{user_add.__name__} ; "
                                   f"{Exception_user_add}")

    return render_template("users/user_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /user_update route
    
    Test : ex : http://127.0.0.1:5005/user_update
    
    Settings : -
    
    Goal : Update a users who has been selected in /users_display
"""


@app.route("/user_update", methods=['GET', 'POST'])
def user_update():
    id_user = request.values['id_user']

    form = FormUpdateUser()
    try:
        print(" on submit ", form.validate_on_submit())
        if form.validate_on_submit():
            update_dictionary = {"id_user": id_user,
                                 "password_user": form.password_user.data,
                                 "nickname_user": form.nickname_user.data,
                                 "name_email": form.name_email.data,
                                 "bio_user": form.bio_user.data,
                                 "signature_user": form.signature_user.data,
                                 "discord_user": form.discord_user.data,
                                 "steam_user": form.steam_user.data,
                                 "icon_user": form.icon_user.data
                                 }
            print("Dictionnary : ", update_dictionary)

            strsql_update_user = """UPDATE t_users SET nickname_user = %(nickname_user)s, 
            icon_user = %(icon_user)s, steam_user = %(steam_user)s, discord_user = %(discord_user)s, bio_user = %(bio_user)s, signature_user = %(signature_user)s,  password_user = %(password_user)s WHERE id_user = %(id_user)s; 
            UPDATE t_emails INNER JOIN t_users_have_emails ue ON fk_email = id_email SET name_email = %(name_email)s WHERE fk_user = %(id_user)s"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_user, update_dictionary)

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('users_have_roles_display', id_user=id_user))
        elif request.method == "GET":
            strsql_id_user = "SELECT id_user, nickname_user, name_email, password_user, bio_user, signature_user, registration_date_user, icon_user, discord_user, steam_user FROM t_users INNER JOIN t_users_have_emails ON fk_user = id_user INNER JOIN t_emails ON fk_email = id_email WHERE id_user = %(id_user)s"
            select_dictionary = {"id_user": id_user}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(strsql_id_user, select_dictionary)
            data_user = mybd_conn.fetchone()
            print("Data users ", data_user, " type ", type(data_user), " user ",
                  data_user["password_user"], data_user["nickname_user"], data_user["bio_user"],
                  data_user["registration_date_user"])

            form.nickname_user.data = data_user["nickname_user"]
            form.password_user.data = data_user["password_user"]
            form.name_email.data = data_user["name_email"]
            form.discord_user.data = data_user["discord_user"]
            form.steam_user.data = data_user["steam_user"]
            form.bio_user.data = data_user["bio_user"]
            form.signature_user.data = data_user["signature_user"]
            form.icon_user.data = data_user["icon_user"]

    except Exception as Exception_user_update:
        raise ExceptionUserUpdate(f"file : {Path(__file__).name}  ;  "
                                  f"{user_update.__name__} ; "
                                  f"{Exception_user_update}")

    return render_template("users/user_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /user_delete route
    
    Test : ex : http://127.0.0.1:5005/user_delete
    
    Settings : -
    
    Goal : Delete a users who has been selected in /users_display
"""


@app.route("/user_delete", methods=['GET', 'POST'])
def user_delete():
    data_delete = None
    delete_btn = None
    id_user = request.values['id_user']

    form = FormDeleteUser()
    try:
        print(" on submit ", form.validate_on_submit())
        if request.method == "POST" and form.validate_on_submit():

            if form.cancel_btn.data:
                return redirect(url_for("users_have_roles_display", id_user=0))

            if form.del_conf_btn.data:
                data_delete = session['data_delete']
                print("Data to delete ", data_delete)

                flash(f"Supprimer le utilisateur définitivement ?", "danger")
                delete_btn = True

            if form.del_final_btn.data:
                delete_dictionary = {"id_user": id_user}
                print("Dictionary : ", delete_dictionary)

                strsql_delete_users_have_emails = """DELETE FROM t_users_have_emails WHERE fk_user = %(id_user)s"""
                strsql_delete_users_have_roles = """DELETE FROM t_users_have_roles WHERE fk_user = %(id_user)s"""
                strsql_delete_id_user = """DELETE FROM t_users WHERE id_user = %(id_user)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_users_have_emails, delete_dictionary)
                    mconn_bd.execute(strsql_delete_users_have_roles, delete_dictionary)
                    mconn_bd.execute(strsql_delete_id_user, delete_dictionary)

                flash(f"Le utilisateur a été supprimé !", "success")
                print(f"Users deleted.")

                return redirect(url_for('users_have_roles_display', id_user=0))

        if request.method == "GET":
            select_dictionary = {"id_user": id_user}
            print(id_user, type(id_user))

            strsql_users_have_emails_delete = """SELECT id_user_has_email, nickname_user, id_user, id_user FROM t_emails
                                            LEFT JOIN t_users_have_emails ON id_email = fk_email
                                            LEFT JOIN t_users r ON fk_user = id_user
                                            WHERE fk_user = %(id_user)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(strsql_users_have_emails_delete, select_dictionary)
                data_delete = mydb_conn.fetchall()
                print("Data to delete : ", data_delete)

                session['data_delete'] = data_delete

                strsql_id_user = "SELECT id_user, nickname_user, name_email, password_user, bio_user, signature_user, registration_date_user, icon_user, discord_user, steam_user FROM t_users INNER JOIN t_users_have_emails ON fk_user = id_user INNER JOIN t_emails ON fk_email = id_email WHERE id_user = %(id_user)s"

                mydb_conn.execute(strsql_id_user, select_dictionary)
                data_user = mydb_conn.fetchone()
                print("Data user ", data_user, " type ", type(data_user), " user ",
                      data_user["nickname_user"], data_user["password_user"], data_user["bio_user"],
                      data_user["registration_date_user"])

            form.nickname_user.data = data_user["nickname_user"]
            form.password_user.data = data_user["password_user"]
            form.name_email.data = data_user["name_email"]
            form.discord_user.data = data_user["discord_user"]
            form.steam_user.data = data_user["steam_user"]
            form.bio_user.data = data_user["bio_user"]
            form.signature_user.data = data_user["signature_user"]
            form.registration_date_user.data = data_user["registration_date_user"]
            form.icon_user.data = data_user["icon_user"]

            delete_btn = False

    except Exception as Exception_user_delete:
        raise ExceptionUserDelete(f"file : {Path(__file__).name}  ;  "
                                  f"{user_delete.__name__} ; "
                                  f"{Exception_user_delete}")

    return render_template("users/user_delete.html",
                           form=form,
                           delete_btn=delete_btn,
                           data_users_linked=data_delete)

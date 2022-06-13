"""Route for users CRUD
File : gestion_users_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from datetime import date
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.users.gestion_users_forms import FormUser

"""
    Author : Raphaël Doutaz 09.05.22
    Set /users_display route

    Test : ex : http://127.0.0.1:5005/users_display

    Settings :  id_user = 0 >> all users_have_roles.
                id_user = "n" display users_have_roles who id is "n"
"""


@app.route("/users_display/<string:order_by>/<int:id_user>", methods=['GET', 'POST'])
def users_display(order_by, id_user):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                strsql_users_display = """SELECT id_user, nickname_user, name_email, steam_user, discord_user, bio_user, signature_user, icon_user, registration_date_user, GROUP_CONCAT(DISTINCT name_role) as name_role FROM t_users 
                                                                            LEFT JOIN t_users_have_roles ur ON id_user = ur.fk_user
                                                                            LEFT JOIN t_users_have_emails ue ON id_user = ue.fk_user
                                                                            LEFT JOIN t_emails ON id_email = fk_email
                                                                            LEFT JOIN t_roles ON id_role = fk_role
                                                                            GROUP BY id_user, id_email"""
                if order_by == "ASC" and id_user == 0:
                    strsql_users_display += """ ORDER BY id_user ASC"""
                    mc_display.execute(strsql_users_display)
                elif order_by == "ASC":
                    strsql_users_display += """ HAVING id_user = %(id_user)s"""

                    mc_display.execute(strsql_users_display, {"id_user": id_user})
                else:
                    strsql_users_display += """ ORDER BY id_user DESC"""

                    mc_display.execute(strsql_users_display)

                data = mc_display.fetchall()

                if not data and id_user == 0:
                    flash("""La table "t_users_have_roles" est vide.""", "warning")
                elif not data and id_user > 0:
                    flash(f"L'utilisateur que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des utilisateurs ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{users_display.__name__} ; "
                                f"{exception_pass}")

    return render_template("users/users_display.html", data=data)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /user_add route
    
    Test : ex : http://127.0.0.1:5005/user_add
    
    Settings : -
    
    Goal : Add a user
"""


@app.route("/user_add", methods=['GET', 'POST'])
def user_add():
    form = FormUser()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""INSERT INTO t_users (id_user,nickname_user, password_user, bio_user, registration_date_user, icon_user, signature_user,discord_user, steam_user) VALUES (NULL,%(nickname_user)s,%(password_user)s,%(bio_user)s,%(registration_date_user)s,%(icon_user)s,%(signature_user)s,%(discord_user)s,%(steam_user)s); """,
                                     {
                                         "password_user": form.password_user.data,
                                         "nickname_user": form.nickname_user.data,
                                         "bio_user": form.bio_user.data,
                                         "signature_user": form.signature_user.data,
                                         "discord_user": form.discord_user.data,
                                         "steam_user": form.steam_user.data,
                                         "registration_date_user": date.today(),
                                         "icon_user": form.icon_user.data
                                     })

                    id_user = mconn_bd.lastrowid

                    mconn_bd.execute("""INSERT INTO t_emails (id_email, name_email) VALUES (NULL,%(name_email)s);""",
                                    {
                                         "name_email": form.name_email.data
                                     })

                    id_email = mconn_bd.lastrowid

                    mconn_bd.execute("""INSERT INTO t_users_have_emails (id_user_has_email,fk_user,fk_email,add_date_user_has_email) VALUES (NULL,%(fk_user)s,%(fk_email)s,%(date)s)""",
                                     {
                                         "fk_user": id_user,
                                         "fk_email": id_email,
                                         "date": date.today()
                                     })

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('users_display', order_by='ASC', id_user=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{user_add.__name__} ; "
                                f"{exception_pass}")

    return render_template("users/user_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /user_update route
    
    Test : ex : http://127.0.0.1:5005/user_update
    
    Settings : -
    
    Goal : Update a user who has been selected in /users_display
"""


@app.route("/user_update/<int:id_user>", methods=['GET', 'POST'])
def user_update(id_user):
    form = FormUser()
    try:
        if form.validate_on_submit():
            with DBconnection() as mconn_bd:
                mconn_bd.execute("""UPDATE t_users SET nickname_user = %(nickname_user)s, 
            icon_user = %(icon_user)s, steam_user = %(steam_user)s, discord_user = %(discord_user)s, bio_user = %(bio_user)s, signature_user = %(signature_user)s,  password_user = %(password_user)s WHERE id_user = %(id_user)s; 
            UPDATE t_emails INNER JOIN t_users_have_emails ue ON fk_email = id_email SET name_email = %(name_email)s WHERE fk_user = %(id_user)s""",
                                 {
                                     "id_user": id_user,
                                     "password_user": form.password_user.data,
                                     "nickname_user": form.nickname_user.data,
                                     "name_email": form.name_email.data,
                                     "bio_user": form.bio_user.data,
                                     "signature_user": form.signature_user.data,
                                     "discord_user": form.discord_user.data,
                                     "steam_user": form.steam_user.data,
                                     "icon_user": form.icon_user.data
                                 })

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('users_display', order_by='ASC', id_user=id_user))

        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute("SELECT id_user, nickname_user, name_email, password_user, bio_user, signature_user, registration_date_user, icon_user, discord_user, steam_user FROM t_users INNER JOIN t_users_have_emails ON fk_user = id_user INNER JOIN t_emails ON fk_email = id_email WHERE id_user = %(id_user)s",
                                  {"id_user": id_user})
            data = mybd_conn.fetchone()
            print("Data users ", data, " type ")

            form.nickname_user.data = data["nickname_user"]
            form.password_user.data = data["password_user"]
            form.name_email.data = data["name_email"]
            form.discord_user.data = data["discord_user"]
            form.steam_user.data = data["steam_user"]
            form.bio_user.data = data["bio_user"]
            form.signature_user.data = data["signature_user"]
            form.icon_user.data = data["icon_user"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                            f"{user_update.__name__} ; "
                            f"{exception_pass}")

    return render_template("users/user_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /user_delete route
    
    Test : ex : http://127.0.0.1:5005/user_delete
    
    Settings : -
    
    Goal : Delete a users who has been selected in /users_display
"""


@app.route("/user_delete/<int:id_user>", methods=['GET', 'POST'])
def user_delete(id_user):
    form = FormUser()
    try:
        if request.method == "POST" and form.validate_on_submit():
            if form.submit_cancel.data:
                return redirect(url_for("users_display", order_by='ASC', id_user=0))

            if form.submit_delete.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("SELECT * FROM t_threads INNER JOIN t_users_create_threads ON id_thread = fk_thread WHERE fk_user = %(id_user)s", {"id_user": id_user})
                    data_threads = mconn_bd.fetchall()

                    for x in data_threads:
                        mconn_bd.execute("""SELECT * FROM t_responses WHERE fk_thread = %(id_thread)s""", {'id_thread': x['id_thread']})
                        data_resps = mconn_bd.fetchall()

                        for y in data_resps:
                            mconn_bd.execute("""DELETE FROM t_users_create_responses WHERE fk_resp = %(id_resp)s;
                            DELETE FROM t_users_update_responses WHERE fk_resp = %(id_resp)s;
                            DELETE FROM t_users_delete_responses WHERE fk_resp = %(id_resp)s;
                            DELETE FROM t_responses WHERE id_resp = %(id_resp)s""", {'id_resp': y['id_resp']})

                    mconn_bd.execute("""DELETE FROM t_users_have_emails WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_have_roles WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_have_characters WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_create_responses WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_create_threads WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_update_responses WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_update_threads WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_delete_responses WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users_delete_threads WHERE fk_user = %(id_user)s;
                                                    DELETE r FROM t_users_create_responses ucr INNER JOIN t_responses r ON id_resp = fk_resp WHERE fk_user = %(id_user)s;
                                                    DELETE t FROM t_users_create_threads uct INNER JOIN t_threads t ON id_thread = fk_thread WHERE fk_user = %(id_user)s;
                                                    DELETE FROM t_users WHERE id_user = %(id_user)s""", {"id_user": id_user})

                flash(f"L'utilisateur a été supprimé !", "success")
                print(f"Users deleted.")

                return redirect(url_for('users_display', order_by='ASC', id_user=0))

        if request.method == "GET":
            print(id_user, type(id_user))
            with DBconnection() as mydb_conn:
                mydb_conn.execute("""SELECT content_resp FROM t_responses 
                                            INNER JOIN t_users_create_responses ON fk_resp = id_resp
                                            WHERE fk_user = %(id_user)s""", {"id_user": id_user})
                data_linked_resps = mydb_conn.fetchall()
                session['data_linked_resps'] = data_linked_resps

                mydb_conn.execute("""SELECT title_thread FROM t_threads 
                                                            INNER JOIN t_users_create_threads ON fk_thread = id_thread
                                                            WHERE fk_user = %(id_user)s""", {"id_user": id_user})
                data_linked_threads = mydb_conn.fetchall()
                session['data_linked_threads'] = data_linked_threads

                mydb_conn.execute("SELECT id_user, nickname_user, name_email, password_user, bio_user, signature_user, registration_date_user, icon_user, discord_user, steam_user FROM t_users INNER JOIN t_users_have_emails ON fk_user = id_user INNER JOIN t_emails ON fk_email = id_email WHERE id_user = %(id_user)s",
                                  {"id_user": id_user})
                data = mydb_conn.fetchone()
                print("Data user ", data)

            form.nickname_user.data = data["nickname_user"]
            form.password_user.data = data["password_user"]
            form.name_email.data = data["name_email"]
            form.discord_user.data = data["discord_user"]
            form.steam_user.data = data["steam_user"]
            form.bio_user.data = data["bio_user"]
            form.signature_user.data = data["signature_user"]
            form.registration_date_user.data = data["registration_date_user"]
            form.icon_user.data = data["icon_user"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                  f"{user_delete.__name__} ; "
                                  f"{exception_pass}")

    return render_template("users/user_delete.html",
                           form=form,
                           data_linked_resps=data_linked_resps,
                           data_linked_threads=data_linked_threads)

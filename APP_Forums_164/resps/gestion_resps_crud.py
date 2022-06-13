"""Route for resps CRUD
File : gestion_resps_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from datetime import date
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.resps.gestion_resps_forms import FormResp

"""
    Author : Raphaël Doutaz 09.05.22
    Set /resps_display route
    
    Test : ex : http://127.0.0.1:5005/resps_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_resp = 0 >> all resps.
                id_resp = "n" display resps who id is "n"
"""


@app.route("/resps_display/<string:order_by>/<int:id_resp>", methods=['GET', 'POST'])
def resps_display(order_by, id_resp):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_resp == 0:
                    mc_display.execute(
                        """SELECT id_resp, content_resp, title_thread, nickname_user FROM t_responses t LEFT JOIN t_threads ON t.fk_thread = id_thread INNER JOIN t_users_create_responses uct ON id_resp = uct.fk_resp INNER JOIN t_users ON id_user = fk_user LEFT JOIN t_users_delete_responses udt ON id_resp = udt.fk_resp WHERE udt.fk_resp IS NULL ORDER BY id_resp ASC""")
                elif order_by == "ASC":
                    mc_display.execute(
                        """SELECT id_resp, content_resp, title_thread, nickname_user FROM t_responses t LEFT JOIN t_threads ON t.fk_thread = id_thread INNER JOIN t_users_create_responses uct ON id_resp = uct.fk_resp INNER JOIN t_users ON id_user = fk_user LEFT JOIN t_users_delete_responses udt ON id_resp = udt.fk_resp WHERE udt.fk_resp IS NULL AND id_resp = %(id_resp)s ORDER BY id_resp ASC""",
                        {"id_resp": id_resp})
                else:
                    mc_display.execute(
                        """SELECT id_resp, content_resp, title_thread, nickname_user FROM t_responses t LEFT JOIN t_threads ON t.fk_thread = id_thread INNER JOIN t_users_create_responses uct ON id_resp = uct.fk_resp INNER JOIN t_users ON id_user = fk_user LEFT JOIN t_users_delete_responses udt ON id_resp = udt.fk_resp WHERE udt.fk_resp IS NULL ORDER BY id_resp DESC""")

                data_resps = mc_display.fetchall()

                print("Data resps : ", data_resps)

                if not data_resps and id_resp == 0:
                    flash("""La table "t_responses" est vide.""", "warning")
                elif not data_resps and id_resp > 0:
                    flash(f"La réponse que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des réponses ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{resps_display.__name__} ; "
                                f"{exception_pass}")

    return render_template("resps/resps_display.html", data=data_resps)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /resp_add route
    
    Test : ex : http://127.0.0.1:5005/resp_add
    
    Settings : -
    
    Goal : Add a response
"""


@app.route("/resp_add", methods=['GET', 'POST'])
def resp_add():
    form = FormResp()
    form.fk_user_author.choices = [('', '')]
    with DBconnection() as mybd_conn:
        mybd_conn.execute(
            "SELECT id_thread, title_thread FROM t_threads LEFT JOIN t_users_delete_threads udt ON id_thread = fk_thread WHERE fk_thread IS NULL ORDER BY title_thread ASC")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_thread': 'None', 'title_thread': 'Aucun'})
    form.fk_thread.choices = [(i["id_thread"], i["title_thread"]) for i in data]

    with DBconnection() as mybd_conn:
        mybd_conn.execute("SELECT id_user, nickname_user FROM t_users ORDER BY nickname_user ASC")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
    form.fk_user.choices = [(i["id_user"], i["nickname_user"]) for i in data]

    if request.method == "POST":
        try:
            if form.validate_on_submit():
                form.fk_thread.data = None if form.fk_thread.data == 'None' else form.fk_thread.data
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(
                        """INSERT INTO t_responses (id_resp,content_resp, fk_thread) VALUES (NULL,%(content_resp)s,%(fk_thread)s)""",
                        {
                            "content_resp": form.content_resp.data,
                            "fk_user": form.fk_user.data,
                            "fk_thread": form.fk_thread.data,
                            "add_date": date.today()
                        }
                        )

                    mconn_bd.execute(
                        """INSERT INTO t_users_create_responses (fk_resp, fk_user, add_date_user_creates_resp) VALUES (%(fk_resp)s, %(fk_user)s, %(add_date)s)""",
                        {
                            "fk_resp": mconn_bd.lastrowid,
                            "fk_user": form.fk_user.data,
                            "add_date": date.today()
                        }
                        )

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('resps_display', order_by='ASC', id_resp=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{resp_add.__name__} ; "
                                f"{exception_pass}")

    return render_template("resps/resp_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /resp_update route
    
    Test : ex : http://127.0.0.1:5005/resp_update
    
    Settings : -
    
    Goal : Update a response who has been selected in /resps_display
"""


@app.route("/resp_update/<int:id_resp>", methods=['GET', 'POST'])
def resp_update(id_resp):
    form = FormResp()
    try:
        form.fk_user_author.choices = [('', '')]
        with DBconnection() as mybd_conn:
            mybd_conn.execute(
                "SELECT id_thread, title_thread FROM t_threads LEFT JOIN t_users_delete_threads udt ON id_thread = fk_thread WHERE fk_thread IS NULL ORDER BY title_thread ASC")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_thread': 'None', 'title_thread': 'Aucun'})
        form.fk_thread.choices = [(i["id_thread"], i["title_thread"]) for i in data]

        with DBconnection() as mybd_conn:
            mybd_conn.execute("SELECT id_user, nickname_user FROM t_users ORDER BY nickname_user ASC")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
        form.fk_user.choices = [(i["id_user"], i["nickname_user"]) for i in data]

        if form.validate_on_submit():
            form.fk_thread.data = None if form.fk_thread.data == 'None' else form.fk_thread.data
            with DBconnection() as mconn_bd:
                mconn_bd.execute("""UPDATE t_responses SET content_resp = %(content_resp)s,fk_thread = %(fk_thread)s WHERE id_resp = %(id_resp)s;
                                        INSERT INTO t_users_update_responses (fk_resp, fk_user, update_date_user_updates_resp) VALUES (%(id_resp)s,%(fk_user)s,%(add_date)s)""",
                                 {
                                     "id_resp": id_resp,
                                     "content_resp": form.content_resp.data,
                                     "fk_thread": form.fk_thread.data,
                                     "fk_user": form.fk_user.data,
                                     "add_date": date.today()
                                 }
                                 )

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('resps_display', order_by="ASC", id_resp=id_resp))
        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute("SELECT id_resp, content_resp, fk_thread, fk_user FROM t_responses INNER JOIN t_users_create_responses ON id_resp = fk_resp WHERE id_resp = %(id_resp)s", {"id_resp": id_resp})
            data = mybd_conn.fetchone()
            print("Data resps ", data)

            form.content_resp.default = data["content_resp"]
            form.fk_thread.default = data["fk_thread"]
            form.fk_user.default = data["fk_user"]
            form.process()

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                            f"{resp_update.__name__} ; "
                            f"{exception_pass}")

    return render_template("resps/resp_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /resp_delete route
    
    Test : ex : http://127.0.0.1:5005/resp_delete
    
    Settings : -
    
    Goal : Delete a response who has been selected in /resps_display
"""


@app.route("/resp_delete/<int:id_resp>", methods=['GET', 'POST'])
def resp_delete(id_resp):
    form = FormResp()
    try:
        with DBconnection() as mybd_conn:
            mybd_conn.execute("SELECT id_user, nickname_user FROM t_users ORDER BY nickname_user ASC")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
        form.fk_user_author.choices = [(i["id_user"], i["nickname_user"]) for i in data]

        form.fk_user.choices = [('', '')]
        form.fk_thread.choices = [('', '')]
        if request.method == "POST" and form.validate_on_submit():
            form.fk_user_author.data = None if form.fk_user_author.data == 'None' else form.fk_user_author.data
            if form.submit_cancel.data:
                return redirect(url_for("resps_display", order_by="ASC", id_resp=0))

            if form.submit_delete.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""INSERT INTO t_users_delete_responses (fk_user, fk_resp, delete_date_user_deletes_resp) VALUES (%(fk_user)s,%(fk_resp)s,%(add_date)s)""",
                                     {
                                         "fk_resp": id_resp,
                                         "fk_user": form.fk_user_author.data,
                                         "add_date": date.today()
                                     }
                                     )

                flash(f"La réponse a été supprimé !", "success")
                print(f"Resps deleted.")

                return redirect(url_for('resps_display', order_by="ASC", id_resp=0))

        if request.method == "GET":
            with DBconnection() as mydb_conn:
                mydb_conn.execute("SELECT id_resp, content_resp, title_thread, nickname_user FROM t_responses t LEFT JOIN t_threads ON t.fk_thread = id_thread INNER JOIN t_users_create_responses ON id_resp = fk_resp INNER JOIN t_users ON id_user = fk_user WHERE id_resp = %(id_resp)s",
                                  {"id_resp": id_resp})
                data = mydb_conn.fetchone()
                print("Data resp ", data)

            form.content_resp.data = data["content_resp"]
            form.fk_thread_text.data = data["title_thread"]
            form.fk_user_text.data = data["nickname_user"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                            f"{resp_delete.__name__} ; "
                            f"{exception_pass}")

    return render_template("resps/resp_delete.html",
                           form=form)

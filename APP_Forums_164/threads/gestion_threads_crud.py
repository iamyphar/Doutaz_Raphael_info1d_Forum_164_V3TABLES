"""Route for threads CRUD
File : gestion_threads_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from datetime import date
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.threads.gestion_threads_forms import FormThread

"""
    Author : Raphaël Doutaz 09.05.22
    Set /threads_display route
    
    Test : ex : http://127.0.0.1:5005/threads_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_thread = 0 >> all threads.
                id_thread = "n" display threads who id is "n"
"""


@app.route("/threads_display/<string:order_by>/<int:id_thread>", methods=['GET', 'POST'])
def threads_display(order_by, id_thread):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_thread == 0:
                    mc_display.execute(
                        """SELECT id_thread, title_thread, content_thread, pinned_thread, icon_thread, title_cat, nickname_user FROM t_threads t LEFT JOIN t_categories ON t.fk_cat = id_cat INNER JOIN t_users_create_threads uct ON id_thread = uct.fk_thread INNER JOIN t_users ON uct.fk_user = id_user LEFT JOIN t_users_delete_threads udt ON id_thread = udt.fk_thread WHERE udt.fk_thread IS NULL ORDER BY id_thread ASC""")
                elif order_by == "ASC":
                    mc_display.execute(
                        """SELECT id_thread, title_thread, content_thread, pinned_thread, icon_thread, title_cat, nickname_user FROM t_threads t LEFT JOIN t_categories ON t.fk_cat = id_cat INNER JOIN t_users_create_threads uct ON id_thread = uct.fk_thread INNER JOIN t_users ON uct.fk_user = id_user LEFT JOIN t_users_delete_threads udt ON id_thread = udt.fk_thread WHERE udt.fk_thread IS NULL AND id_thread = %(id_thread)s ORDER BY id_thread ASC""",
                        {"id_thread": id_thread})
                else:
                    mc_display.execute(
                        """SELECT id_thread, title_thread, content_thread, pinned_thread, icon_thread, title_cat, nickname_user FROM t_threads t LEFT JOIN t_categories ON t.fk_cat = id_cat INNER JOIN t_users_create_threads uct ON id_thread = uct.fk_thread INNER JOIN t_users ON uct.fk_user = id_user LEFT JOIN t_users_delete_threads udt ON id_thread = udt.fk_thread WHERE udt.fk_thread IS NULL ORDER BY id_thread DESC""")

                data = mc_display.fetchall()

                print("Data threads : ", data)

                if not data and id_thread == 0:
                    flash("""La table "t_threads" est vide.""", "warning")
                elif not data and id_thread > 0:
                    flash(f"Le fils de discussions que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des fils de discussions ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{threads_display.__name__} ; "
                                f"{exception_pass}")

    return render_template("threads/threads_display.html", data=data)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /thread_add route
    
    Test : ex : http://127.0.0.1:5005/thread_add
    
    Settings : -
    
    Goal : Add a thread
"""


@app.route("/thread_add", methods=['GET', 'POST'])
def thread_add():
    form = FormThread()
    form.fk_user_author.choices = [('', '')]
    with DBconnection() as mybd_conn:
        mybd_conn.execute("SELECT id_cat, title_cat FROM t_categories")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_cat': 'None', 'title_cat': 'Aucun'})
    form.fk_cat.choices = [(i["id_cat"], i["title_cat"]) for i in data]

    with DBconnection() as mybd_conn:
        mybd_conn.execute("SELECT id_user, nickname_user FROM t_users")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
    form.fk_user.choices = [(i["id_user"], i["nickname_user"]) for i in data]

    if request.method == "POST":
        try:
            print(" on submit ", form.validate_on_submit())
            if form.validate_on_submit():
                form.fk_cat.data = None if form.fk_cat.data == 'None' else form.fk_cat.data

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(
                        """INSERT INTO t_threads (id_thread,title_thread,content_thread, icon_thread,fk_cat, pinned_thread) VALUES (NULL,%(title_thread)s,%(content_thread)s,%(icon_thread)s,%(fk_cat)s,%(pinned_thread)s)""",
                        {
                            "title_thread": form.title_thread.data,
                            "content_thread": form.content_thread.data,
                            "icon_thread": form.icon_thread.data,
                            "pinned_thread": form.pinned_thread.data,
                            "fk_user": form.fk_user.data,
                            "fk_cat": form.fk_cat.data,
                            "add_date": date.today()
                        }
                    )

                    mconn_bd.execute(
                        """INSERT INTO t_users_create_threads (fk_thread, fk_user, add_date_user_creates_thread) VALUES (%(fk_thread)s, %(fk_user)s, %(add_date)s)""",
                        {
                            "fk_thread": mconn_bd.lastrowid,
                            "fk_user": form.fk_user.data,
                            "add_date": date.today()
                        })

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('threads_display', order_by='ASC', id_thread=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{thread_add.__name__} ; "
                                f"{exception_pass}")

    return render_template("threads/thread_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /thread_update route
    
    Test : ex : http://127.0.0.1:5005/thread_update
    
    Settings : -
    
    Goal : Update a thread who has been selected in /threads_display
"""


@app.route("/thread_update/<int:id_thread>", methods=['GET', 'POST'])
def thread_update(id_thread):
    form = FormThread()
    try:
        form.fk_user_author.choices = [('', '')]
        with DBconnection() as mybd_conn:
            mybd_conn.execute("SELECT id_cat, title_cat FROM t_categories")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_cat': 'None', 'title_cat': 'Aucun'})
        form.fk_cat.choices = [(i["id_cat"], i["title_cat"]) for i in data]

        with DBconnection() as mybd_conn:
            mybd_conn.execute("SELECT id_user, nickname_user FROM t_users")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
        form.fk_user.choices = [(i["id_user"], i["nickname_user"]) for i in data]

        if form.validate_on_submit():
            form.fk_cat.data = None if form.fk_cat.data == 'None' else form.fk_cat.data

            with DBconnection() as mconn_bd:
                mconn_bd.execute("""UPDATE t_threads SET title_thread = %(title_thread)s,content_thread = %(content_thread)s,icon_thread = %(icon_thread)s ,fk_cat = %(fk_cat)s, pinned_thread = %(pinned_thread)s WHERE id_thread = %(id_thread)s;
                                        INSERT INTO t_users_update_threads (fk_thread, fk_user, update_date_user_updates_thread) VALUES (%(id_thread)s,%(fk_user)s,%(add_date)s)""",
                                 {
                                     "id_thread": id_thread,
                                     "title_thread": form.title_thread.data,
                                     "content_thread": form.content_thread.data,
                                     "pinned_thread": form.pinned_thread.data,
                                     "icon_thread": form.icon_thread.data,
                                     "fk_cat": form.fk_cat.data,
                                     "fk_user": form.fk_user.data,
                                     "add_date": date.today()
                                 })

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('threads_display', order_by="ASC", id_thread=id_thread))

        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute("SELECT id_thread, title_thread, content_thread, pinned_thread,  icon_thread, fk_cat, fk_user FROM t_threads INNER JOIN t_users_create_threads ON id_thread = fk_thread WHERE id_thread = %(id_thread)s", {"id_thread": id_thread})
            data = mybd_conn.fetchone()
            print("Data threads ", data)

            form.title_thread.default = data["title_thread"]
            form.content_thread.default = data["content_thread"]
            form.pinned_thread.default = data["pinned_thread"]
            form.icon_thread.default = data["icon_thread"]
            form.fk_cat.default = data["fk_cat"]
            form.fk_user.default = data["fk_user"]
            form.process()

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                            f"{thread_update.__name__} ; "
                            f"{exception_pass}")

    return render_template("threads/thread_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /thread_delete route
    
    Test : ex : http://127.0.0.1:5005/thread_delete
    
    Settings : -
    
    Goal : Delete a thread who has been selected in /threads_display
"""


@app.route("/thread_delete/<int:id_thread>", methods=['GET', 'POST'])
def thread_delete(id_thread):
    form = FormThread()
    data_linked = None
    try:
        with DBconnection() as mybd_conn:
            mybd_conn.execute("SELECT id_user, nickname_user FROM t_users ORDER BY nickname_user ASC")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_user': 'None', 'nickname_user': 'Aucun'})
        form.fk_user_author.choices = [(i["id_user"], i["nickname_user"]) for i in data]

        form.fk_cat.choices = [('', '')]
        form.fk_user.choices = [('', '')]
        if request.method == "POST" and form.validate_on_submit():
            form.fk_user_author.data = None if form.fk_user_author.data == 'None' else form.fk_user_author.data

            if form.submit_cancel.data:
                return redirect(url_for("threads_display", order_by="ASC", id_thread=0))

            if form.submit_delete.data:
                delete_dictionary = {"fk_thread": id_thread,
                                     "fk_user": form.fk_user_author.data,
                                     "add_date": date.today()}

                strsql_delete_id_thread = """INSERT INTO t_users_delete_threads (fk_user, fk_thread, delete_date_user_deletes_thread) VALUES (%(fk_user)s,%(fk_thread)s,%(add_date)s);"""
                strsql_resps = """SELECT id_resp FROM t_responses WHERE fk_thread = %(fk_thread)s"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_id_thread, delete_dictionary)
                    mconn_bd.execute(strsql_resps, delete_dictionary)
                    mcdata = mconn_bd.fetchall()

                    strsql_delete_resps = """"""
                    if mcdata != ():
                        delete_dictionary = {"fk_thread": id_thread,
                                             "fk_user": form.fk_user_author.data,
                                             "add_date": date.today()}
                        for x in mcdata:
                            strsql_delete_resps += """INSERT INTO t_users_delete_responses (fk_user, fk_resp, delete_date_user_deletes_resp) VALUES (%(fk_user)s,"""+str(x['id_resp'])+""",%(add_date)s);"""
                        mconn_bd.execute(strsql_delete_resps, delete_dictionary)

                flash(f"La fils de discussions a été supprimé !", "success")
                print(f"Threads deleted.")

                return redirect(url_for('threads_display', order_by="ASC", id_thread=0))

        if request.method == "GET":
            with DBconnection() as mydb_conn:
                mydb_conn.execute("""SELECT id_resp, content_resp, nickname_user FROM t_responses 
                                            INNER JOIN t_users_create_responses ON id_resp = fk_resp
                                            INNER JOIN t_users ON id_user = fk_user
                                            WHERE fk_thread = %(id_thread)s""", {"id_thread": id_thread})
                data_linked = mydb_conn.fetchall()
                session['data_linked'] = data_linked

                mydb_conn.execute("SELECT id_thread, title_thread, content_thread, pinned_thread,  icon_thread, title_cat, nickname_user FROM t_threads t LEFT JOIN t_categories ON t.fk_cat = id_cat INNER JOIN t_users_create_threads ON id_thread = fk_thread INNER JOIN t_users ON id_user = fk_user WHERE id_thread = %(id_thread)s",
                                  {"id_thread": id_thread})
                data = mydb_conn.fetchone()
                print("Data thread ", data)

            form.title_thread.data = data["title_thread"]
            form.content_thread.data = data["content_thread"]
            form.icon_thread.data = data["icon_thread"]
            form.pinned_thread.data = data["pinned_thread"]
            form.fk_cat_text.data = data["title_cat"]
            form.fk_user_text.data = data["nickname_user"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                            f"{thread_delete.__name__} ; "
                            f"{exception_pass}")

    return render_template("threads/thread_delete.html",
                           form=form,
                           data_linked=data_linked)

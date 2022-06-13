"""Route for threads CRUD
File : gestion_threads_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_Forums_164.threads.gestion_threads_forms import FormAddThread
from APP_Forums_164.threads.gestion_threads_forms import FormDeleteThread
from APP_Forums_164.threads.gestion_threads_forms import FormUpdateThread
from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /threads_display route
    
    Test : ex : http://127.0.0.1:5005/threads_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_thread_sel = 0 >> all threads.
                id_thread_sel = "n" display threads who id is "n"
"""


@app.route("/threads_display/<string:order_by>/<int:id_thread_sel>", methods=['GET', 'POST'])
def threads_display(order_by, id_thread_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_thread_sel == 0:
                    strsql_threads_display = """SELECT id_thread, title_thread, content_thread, pinned_thread,  title_cat FROM t_threads LEFT JOIN t_categories ON fk_cat = id_cat ORDER BY title_thread ASC"""
                    mc_display.execute(strsql_threads_display)
                elif order_by == "ASC":
                    select_dictionary = {"id_thread_selected": id_thread_sel}
                    strsql_threads_display = """SELECT id_thread, title_thread, content_thread, pinned_thread,  title_cat FROM t_threads LEFT JOIN t_categories ON fk_cat = id_cat WHERE id_thread = %(id_thread_selected)s"""

                    mc_display.execute(strsql_threads_display, select_dictionary)
                else:
                    strsql_threads_display = """SELECT id_thread, title_thread, content_thread, pinned_thread,  title_cat FROM t_threads LEFT JOIN t_categories ON fk_cat = id_cat ORDER BY id_thread DESC"""

                    mc_display.execute(strsql_threads_display)

                data_threads = mc_display.fetchall()

                print("Data threads : ", data_threads, " Type : ", type(data_threads))

                # If table is empty
                if not data_threads and id_thread_sel == 0:
                    flash("""La table "t_threads" est vide.""", "warning")
                elif not data_threads and id_thread_sel > 0:
                    # If no threads with id = id_thread_sel found
                    flash(f"La fils de discussions que vous avez demandé n'existe pas.", "warning")
                else:
                    # In all others cases, this means the table is empty.
                    flash(f"Les données des fils de discussions ont été affichées !", "success")

        except Exception as Exception_threads_display:
            raise ExceptionThreadsDisplay(f"file : {Path(__file__).name}  ;  "
                                             f"{threads_display.__name__} ; "
                                             f"{Exception_threads_display}")

    return render_template("threads/threads_display.html", data=data_threads)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /thread_add route
    
    Test : ex : http://127.0.0.1:5005/thread_add
    
    Settings : -
    
    Goal : Add a threads
"""


@app.route("/thread_add", methods=['GET', 'POST'])
def thread_add():
    form = FormAddThread()
    strsql_cats = "SELECT id_cat, title_cat FROM t_categories"
    with DBconnection() as mybd_conn:
        mybd_conn.execute(strsql_cats)
    data_cats = mybd_conn.fetchall()

    cats_list = []
    for i in data_cats:
        cats_list.append(i['title_cat'])
    cats_list.insert(0, 'Aucune')
    form.fk_cat.choices = cats_list
    if request.method == "POST":
        try:
            print(" on submit ", form.validate_on_submit())
            if form.validate_on_submit():
                insertion_dictionary = {
                    "title_thread": form.title_thread.data,
                    "content_thread": form.content_thread.data,
                    "icon_thread": form.icon_thread.data,
                    "fk_cat": form.fk_cat.data
                }
                print("Dictionary : ", insertion_dictionary)

                strsql_insert_thread = """INSERT INTO t_threads (id_thread,title_thread,content_thread, pinned_thread, icon_thread,fk_cat) VALUES (NULL,%(title_thread)s,%(content_thread)s,%(icon_thread)s,(SELECT id_cat FROM t_categories WHERE title_cat = %(fk_cat)s)) """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_thread, insertion_dictionary)

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('threads_display', order_by='DESC', id_thread_sel=0))

        except Exception as Exception_thread_add:
            raise ExceptionThreadAdd(f"file : {Path(__file__).name}  ;  "
                                       f"{thread_add.__name__} ; "
                                       f"{Exception_thread_add}")

    return render_template("threads/thread_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /thread_update route
    
    Test : ex : http://127.0.0.1:5005/thread_update
    
    Settings : -
    
    Goal : Update a threads who has been selected in /threads_display
"""


@app.route("/thread_update", methods=['GET', 'POST'])
def thread_update():
    id_thread = request.values['id_thread']

    form = FormUpdateThread()
    try:
        strsql_cats = "SELECT id_cat, title_cat FROM t_categories"
        with DBconnection() as mybd_conn:
            mybd_conn.execute(strsql_cats)
        data_cats = mybd_conn.fetchall()

        cats_list = [(i["id_cat"], i["title_cat"]) for i in data_cats]
        cats_list.insert(0, ('None', 'Aucune'))
        form.fk_cat.choices = cats_list
        print(cats_list)

        print(" on submit ", form.validate_on_submit())
        if form.validate_on_submit():
            form.fk_cat.data = None if form.fk_cat.data == 'None' else form.fk_cat.data
            update_dictionary = {"id_thread": id_thread,
                                 "title_thread": form.title_thread.data,
                                 "content_thread": form.content_thread.data,
                                 "icon_thread": form.icon_thread.data,
                                 "fk_cat": form.fk_cat.data
                                 }
            print("Dictionnary : ", update_dictionary)

            strsql_update_thread = """UPDATE t_threads SET title_thread = %(title_thread)s,content_thread = %(content_thread)s,icon_thread = %(icon_thread)s ,fk_cat = %(fk_cat)s WHERE id_thread = %(id_thread)s;"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_thread, update_dictionary)

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('threads_display', order_by="ASC", id_thread_sel=id_thread))
        elif request.method == "GET":
            strsql_id_thread = "SELECT id_thread, title_thread, content_thread, pinned_thread,  icon_thread, fk_cat FROM t_threads WHERE id_thread = %(id_thread)s"
            select_dictionary = {"id_thread": id_thread}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(strsql_id_thread, select_dictionary)
            data_thread = mybd_conn.fetchone()
            print("Data threads ", data_thread, " type ", type(data_thread), " thread ",
                  data_thread["title_thread"], data_thread["content_thread"], data_thread["icon_thread"])

            form.title_thread.default = data_thread["title_thread"]
            form.content_thread.default = data_thread["content_thread"]
            form.icon_thread.default = data_thread["icon_thread"]
            form.fk_cat.default = data_thread["fk_cat"]
            form.process()

    except Exception as Exception_thread_update:
        raise ExceptionThreadUpdate(f"file : {Path(__file__).name}  ;  "
                                      f"{thread_update.__name__} ; "
                                      f"{Exception_thread_update}")

    return render_template("threads/thread_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /thread_delete route
    
    Test : ex : http://127.0.0.1:5005/thread_delete
    
    Settings : -
    
    Goal : Delete a threads who has been selected in /threads_display
"""


@app.route("/thread_delete", methods=['GET', 'POST'])
def thread_delete():
    data_delete = None
    delete_btn = None
    id_thread = request.values['id_thread']

    form = FormDeleteThread()
    try:
        strsql_cats = "SELECT id_cat, title_cat FROM t_categories INNER JOIN t_threads ON fk_cat = id_cat WHERE id_thread = %(id_thread)s"
        id_thread_dict = {"id_thread": id_thread}
        with DBconnection() as mybd_conn:
            mybd_conn.execute(strsql_cats, id_thread_dict)
        data_cats = mybd_conn.fetchall()

        cats_list = []
        for i in data_cats:
            cats_list.append(i['title_cat'])
        form.fk_cat.choices = cats_list
        print(" on submit ", form.validate_on_submit())
        if request.method == "POST" and form.validate_on_submit():

            if form.cancel_btn.data:
                return redirect(url_for("threads_display", order_by="ASC", id_thread_sel=0))

            if form.del_conf_btn.data:
                data_delete = session['data_delete']
                print("Data to delete ", data_delete)

                flash(f"Supprimer la thread définitivement ?", "danger")
                delete_btn = True

            if form.del_final_btn.data:
                delete_dictionary = {"id_thread": id_thread}
                print("Dictionary : ", delete_dictionary)

                strsql_delete_threads_have_thread = """UPDATE t_threads SET fk_thread=NULL WHERE fk_thread = %(id_thread)s;UPDATE t_threads SET fk_thread=NULL WHERE fk_thread = %(id_thread)s"""
                strsql_delete_id_thread = """DELETE FROM t_threads WHERE id_thread = %(id_thread)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_threads_have_thread, delete_dictionary)
                    mconn_bd.execute(strsql_delete_id_thread, delete_dictionary)

                flash(f"La thread a été supprimé !", "success")
                print(f"Threads deleted.")

                return redirect(url_for('threads_display', order_by="ASC", id_thread_sel=0))

        if request.method == "GET":
            select_dictionary = {"id_thread": id_thread}
            print(id_thread, type(id_thread))

            strsql_threads_delete = """SELECT title_thread, content_thread, pinned_thread, icon_thread, id_thread, id_thread FROM t_threads t
                                            LEFT JOIN t_threads c ON t.fk_thread = id_thread
                                            WHERE t.fk_thread = %(id_thread)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(strsql_threads_delete, select_dictionary)
                data_delete = mydb_conn.fetchall()
                print("Data to delete : ", data_delete)

                session['data_delete'] = data_delete

                strsql_id_thread = "SELECT id_thread, title_thread, content_thread, pinned_thread,  icon_thread, title_cat FROM t_threads LEFT JOIN t_categories ON fk_cat = id_cat WHERE id_thread = %(id_thread)s"

                mydb_conn.execute(strsql_id_thread, select_dictionary)
                data_title_thread = mydb_conn.fetchone()
                print("Data thread ", data_title_thread, " type ", type(data_title_thread), " thread ",
                      data_title_thread["title_thread"], data_title_thread["content_thread"], data_title_thread["icon_thread"])

            form.title_thread.data = data_title_thread["title_thread"]
            form.content_thread.data = data_title_thread["content_thread"]
            form.icon_thread.data = data_title_thread["icon_thread"]
            form.fk_cat.data = data_title_thread["title_cat"]

            delete_btn = False

    except Exception as Exception_thread_delete:
        raise ExceptionThreadDelete(f"file : {Path(__file__).name}  ;  "
                                      f"{thread_delete.__name__} ; "
                                      f"{Exception_thread_delete}")

    return render_template("threads/thread_delete.html",
                           form=form,
                           delete_btn=delete_btn,
                           data_threads_linked=data_delete)

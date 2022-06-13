"""Route for cats CRUD
File : gestion_categories_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.cats.gestion_cats_forms import FormCategory
from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /categories_display route
    
    Test : ex : http://127.0.0.1:5005/categories_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_cat = 0 >> all cats.
                id_cat = "n" display cats who id is "n"
"""


@app.route("/categories_display/<string:order_by>/<int:id_cat>", methods=['GET', 'POST'])
def categories_display(order_by, id_cat):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_cat == 0:
                    mc_display.execute(
                        """SELECT c.id_cat, c.title_cat, c.description_cat, c.icon_cat, title_section, cc.title_cat as fk_title_cat FROM t_categories c LEFT JOIN t_sections ON c.fk_section = id_section LEFT JOIN t_categories cc ON c.fk_cat = cc.id_cat ORDER BY c.id_cat ASC"""
                    )
                elif order_by == "ASC":
                    mc_display.execute(
                        """SELECT c.id_cat, c.title_cat, c.description_cat, c.icon_cat, title_section, cc.title_cat as fk_title_cat FROM t_categories c LEFT JOIN t_sections ON c.fk_section = id_section LEFT JOIN t_categories cc ON c.fk_cat = cc.id_cat WHERE c.id_cat = %(id_cat)s ORDER BY c.id_cat ASC""",
                        {"id_cat": id_cat}
                    )
                else:
                    mc_display.execute(
                        """SELECT c.id_cat, c.title_cat, c.description_cat, c.icon_cat, title_section, cc.title_cat as fk_title_cat FROM t_categories c LEFT JOIN t_sections ON c.fk_section = id_section LEFT JOIN t_categories cc ON c.fk_cat = cc.id_cat ORDER BY c.id_cat DESC"""
                    )

                data = mc_display.fetchall()

                print("Data cats : ", data)

                if not data and id_cat == 0:
                    flash("""La table "t_categories" est vide.""", "warning")
                elif not data and id_cat > 0:
                    flash(f"La catégorie que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des catégories ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{categories_display.__name__} ; "
                                f"{exception_pass}")

    return render_template("cats/cats_display.html", data=data)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /category_add route
    
    Test : ex : http://127.0.0.1:5005/category_add
    
    Settings : -
    
    Goal : Add a category
"""


@app.route("/category_add", methods=['GET', 'POST'])
def category_add():
    form = FormCategory()
    with DBconnection() as mybd_conn:
        mybd_conn.execute("SELECT id_section, title_section FROM t_sections ORDER BY title_section")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_section': 'None', 'title_section': 'Aucun'})
    form.fk_section.choices = [(i["id_section"], i["title_section"]) for i in data]

    with DBconnection() as mybd_conn:
        mybd_conn.execute("SELECT id_cat, title_cat FROM t_categories ORDER BY title_cat")
    data = mybd_conn.fetchall()
    data.insert(0, {'id_cat': 'None', 'title_cat': 'Aucun'})
    form.fk_cat.choices = [(i["id_cat"], i["title_cat"]) for i in data]


    if request.method == "POST":
        try:
            if form.validate_on_submit():
                form.fk_section.data = None if form.fk_section.data == 'None' else form.fk_section.data
                form.fk_cat.data = None if form.fk_cat.data == 'None' else form.fk_cat.data

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(
                        """INSERT INTO t_categories (id_cat,title_cat,description_cat,icon_cat,fk_section,fk_cat) VALUES (NULL,%(title_cat)s,%(description_cat)s,%(icon_cat)s,%(fk_section)s,%(fk_cat)s) """,
                        {
                            "title_cat": form.title_cat.data,
                            "description_cat": form.description_cat.data,
                            "icon_cat": form.icon_cat.data,
                            "fk_section": form.fk_section.data,
                            "fk_cat": form.fk_cat.data
                        }
                    )

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('categories_display', order_by='ASC', id_cat=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                f"{category_add.__name__} ; "
                                f"{exception_pass}")

    return render_template("cats/cat_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /cat_update route
    
    Test : ex : http://127.0.0.1:5005/cat_update
    
    Settings : -
    
    Goal : Update a category who has been selected in /categories_display
"""


@app.route("/category_update/<int:id_cat>", methods=['GET', 'POST'])
def category_update(id_cat):
    form = FormCategory()
    try:
        with DBconnection() as mybd_conn:
            mybd_conn.execute("SELECT id_section, title_section FROM t_sections ORDER BY title_section")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_section': 'None', 'title_section': 'Aucun'})
        form.fk_section.choices = [(i["id_section"], i["title_section"]) for i in data]

        with DBconnection() as mybd_conn:
            mybd_conn.execute("SELECT id_cat, title_cat FROM t_categories ORDER BY title_cat")
        data = mybd_conn.fetchall()
        data.insert(0, {'id_cat': 'None', 'title_cat': 'Aucun'})
        form.fk_cat.choices = [(i["id_cat"], i["title_cat"]) for i in data]

        if form.validate_on_submit():
            form.fk_section.data = None if form.fk_section.data == 'None' else form.fk_section.data
            form.fk_cat.data = None if form.fk_cat.data == 'None' else form.fk_cat.data

            with DBconnection() as mconn_bd:
                mconn_bd.execute(
                    """UPDATE t_categories SET title_cat = %(title_cat)s,description_cat = %(description_cat)s,icon_cat = %(icon_cat)s ,fk_section = %(fk_section)s,fk_cat = %(fk_cat)s WHERE id_cat = %(id_cat)s;""",
                    {
                        "id_cat": id_cat,
                        "title_cat": form.title_cat.data,
                        "description_cat": form.description_cat.data,
                        "icon_cat": form.icon_cat.data,
                        "fk_section": form.fk_section.data,
                        "fk_cat": form.fk_cat.data
                    }
                )

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('categories_display', order_by="ASC", id_cat=id_cat))

        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute(
                    "SELECT id_cat, title_cat, description_cat, icon_cat, fk_section, fk_cat FROM t_categories WHERE id_cat = %(id_cat)s",
                    {
                        "id_cat": id_cat
                    }
                )

            data = mybd_conn.fetchone()
            print("Data categories ", data)

            form.title_cat.default = data["title_cat"]
            form.description_cat.default = data["description_cat"]
            form.icon_cat.default = data["icon_cat"]
            form.fk_section.default = data["fk_section"]
            form.fk_cat.default = data["fk_cat"]
            form.process()

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                            f"{category_update.__name__} ; "
                            f"{exception_pass}")

    return render_template("cats/cat_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /category_delete route
    
    Test : ex : http://127.0.0.1:5005/category_delete
    
    Settings : -
    
    Goal : Delete a category who has been selected in /categories_display
"""


@app.route("/category_delete/<int:id_cat>", methods=['GET', 'POST'])
def category_delete(id_cat):
    linked_data_threads = None
    linked_data_cats = None
    form = FormCategory()
    try:
        form.fk_section.choices = [('', '')]
        form.fk_cat.choices = [('', '')]

        if request.method == "POST" and form.validate_on_submit():
            if form.submit_cancel.data:
                return redirect(url_for("categories_display", order_by="ASC", id_cat=0))

            if form.submit_delete.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(
                        """UPDATE t_threads SET fk_cat=NULL WHERE fk_cat = %(id_cat)s;UPDATE t_categories SET fk_cat=NULL WHERE fk_cat = %(id_cat)s; DELETE FROM t_categories WHERE id_cat = %(id_cat)s""",
                        {
                            "id_cat": id_cat
                        }
                    )
                flash(f"La category a été supprimé !", "success")
                print(f"Category deleted.")

                return redirect(url_for('categories_display', order_by="ASC", id_cat=0))

        if request.method == "GET":
            with DBconnection() as mydb_conn:
                mydb_conn.execute("""SELECT title_thread, content_thread,icon_thread, pinned_thread, nickname_user, id_cat, id_thread FROM t_threads t
                                                    LEFT JOIN t_categories c ON t.fk_cat = id_cat
                                                    LEFT JOIN t_users_create_threads ON id_thread = fk_thread
                                                    LEFT JOIN t_users ON id_user = fk_user
                                                    WHERE t.fk_cat = %(id_cat)s""",
                                  {"id_cat": id_cat}
                                  )

                linked_data_threads = mydb_conn.fetchall()
                session['linked_data_threads'] = linked_data_threads

                mydb_conn.execute("""SELECT c.title_cat, c.description_cat, c.icon_cat, c.id_cat, title_section FROM t_categories cc
                                                    LEFT JOIN t_categories c ON c.fk_cat = cc.id_cat
                                                    LEFT JOIN t_sections s ON id_section = cc.fk_section
                                                    WHERE c.fk_cat = %(id_cat)s""",
                                  {"id_cat": id_cat}
                                  )
                linked_data_cats = mydb_conn.fetchall()
                session['linked_data_cats'] = linked_data_cats

                mydb_conn.execute(
                    "SELECT c.id_cat, c.title_cat, c.description_cat, title_section, cc.title_cat, c.icon_cat FROM t_categories c LEFT JOIN t_sections ON c.fk_section = id_section LEFT JOIN t_categories cc ON c.fk_cat = cc.id_cat WHERE c.id_cat = %(id_cat)s",
                    {"id_cat": id_cat})
                data = mydb_conn.fetchone()

                print("Data category ", data)

            form.title_cat.data = data["title_cat"]
            form.description_cat.data = data["description_cat"]
            form.icon_cat.data = data["icon_cat"]
            form.fk_section_text.data = data["title_section"]
            form.fk_cat_text.data = data["title_cat"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                            f"{category_delete.__name__} ; "
                            f"{exception_pass}")

    return render_template("cats/cat_delete.html",
                           form=form,
                           linked_data_threads=linked_data_threads,
                           linked_data_cats=linked_data_cats)

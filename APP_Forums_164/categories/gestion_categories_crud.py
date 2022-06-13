"""Route for cats CRUD
File : gestion_categories_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_Forums_164.categories.gestion_categories_forms import FormAddCategory
from APP_Forums_164.categories.gestion_categories_forms import FormDeleteCategory
from APP_Forums_164.categories.gestion_categories_forms import FormUpdateCategory
from APP_Forums_164.erreurs.exceptions import *

"""
    Author : Raphaël Doutaz 09.05.22
    Set /categories_display route
    
    Test : ex : http://127.0.0.1:5005/categories_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_cat_sel = 0 >> all cats.
                id_cat_sel = "n" display cats who id is "n"
"""


@app.route("/categories_display/<string:order_by>/<int:id_cat_sel>", methods=['GET', 'POST'])
def categories_display(order_by, id_cat_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_cat_sel == 0:
                    strsql_cats_display = """SELECT id_cat, title_cat, description_cat, title_section FROM t_categories LEFT JOIN t_sections ON fk_section = id_section ORDER BY title_cat ASC"""
                    mc_display.execute(strsql_cats_display)
                elif order_by == "ASC":
                    select_dictionary = {"id_cat_selected": id_cat_sel}
                    strsql_cats_display = """SELECT id_cat, title_cat, description_cat, title_section FROM t_categories LEFT JOIN t_sections ON fk_section = id_section WHERE id_cat = %(id_cat_selected)s"""

                    mc_display.execute(strsql_cats_display, select_dictionary)
                else:
                    strsql_cats_display = """SELECT id_cat, title_cat, description_cat, title_section FROM t_categories LEFT JOIN t_sections ON fk_section = id_section ORDER BY id_cat DESC"""

                    mc_display.execute(strsql_cats_display)

                data_cats = mc_display.fetchall()

                print("Data cats : ", data_cats, " Type : ", type(data_cats))

                # If table is empty
                if not data_cats and id_cat_sel == 0:
                    flash("""La table "t_categories" est vide.""", "warning")
                elif not data_cats and id_cat_sel > 0:
                    # If no cats with id = id_cat_sel found
                    flash(f"La catégorie que vous avez demandé n'existe pas.", "warning")
                else:
                    # In all others cases, this means the table is empty.
                    flash(f"Les données des catégories ont été affichées !", "success")

        except Exception as Exception_categories_display:
            raise ExceptionCategoriesDisplay(f"file : {Path(__file__).name}  ;  "
                                             f"{categories_display.__name__} ; "
                                             f"{Exception_categories_display}")

    return render_template("categories/categories_display.html", data=data_cats)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /category_add route
    
    Test : ex : http://127.0.0.1:5005/category_add
    
    Settings : -
    
    Goal : Add a categories
"""


@app.route("/category_add", methods=['GET', 'POST'])
def category_add():
    form = FormAddCategory()
    strsql_sections = "SELECT id_section, title_section FROM t_sections"
    with DBconnection() as mybd_conn:
        mybd_conn.execute(strsql_sections)
    data_sections = mybd_conn.fetchall()

    sections_list = []
    for i in data_sections:
        sections_list.append(i['title_section'])
    sections_list.insert(0, 'Aucune')
    form.fk_section.choices = sections_list
    if request.method == "POST":
        try:
            print(" on submit ", form.validate_on_submit())
            if form.validate_on_submit():
                insertion_dictionary = {
                    "title_cat": form.title_cat.data,
                    "description_cat": form.description_cat.data,
                    "icon_cat": form.icon_cat.data,
                    "fk_section": form.fk_section.data
                }
                print("Dictionary : ", insertion_dictionary)

                strsql_insert_cat = """INSERT INTO t_categories (id_cat,title_cat,description_cat,icon_cat,fk_section) VALUES (NULL,%(title_cat)s,%(description_cat)s,%(icon_cat)s,(SELECT id_section FROM t_sections WHERE title_section = %(fk_section)s)) """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_cat, insertion_dictionary)

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('categories_display', order_by='DESC', id_cat_sel=0))

        except Exception as Exception_category_add:
            raise ExceptionCategoryAdd(f"file : {Path(__file__).name}  ;  "
                                       f"{category_add.__name__} ; "
                                       f"{Exception_category_add}")

    return render_template("categories/category_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /cat_update route
    
    Test : ex : http://127.0.0.1:5005/cat_update
    
    Settings : -
    
    Goal : Update a cats who has been selected in /categories_display
"""


@app.route("/cat_update", methods=['GET', 'POST'])
def category_update():
    id_cat = request.values['id_cat']

    form = FormUpdateCategory()
    try:
        strsql_sections = "SELECT id_section, title_section FROM t_sections"
        with DBconnection() as mybd_conn:
            mybd_conn.execute(strsql_sections)
        data_sections = mybd_conn.fetchall()

        sections_list = [(i["id_section"], i["title_section"]) for i in data_sections]
        sections_list.insert(0, ('None', 'Aucune'))
        form.fk_section.choices = sections_list
        print(sections_list)

        print(" on submit ", form.validate_on_submit())
        if form.validate_on_submit():
            form.fk_section.data = None if form.fk_section.data == 'None' else form.fk_section.data
            update_dictionary = {"id_cat": id_cat,
                                 "title_cat": form.title_cat.data,
                                 "description_cat": form.description_cat.data,
                                 "icon_cat": form.icon_cat.data,
                                 "fk_section": form.fk_section.data
                                 }
            print("Dictionnary : ", update_dictionary)

            strsql_update_cat = """UPDATE t_categories SET title_cat = %(title_cat)s,description_cat = %(description_cat)s,icon_cat = %(icon_cat)s ,fk_section = %(fk_section)s WHERE id_cat = %(id_cat)s;"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_cat, update_dictionary)

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('categories_display', order_by="ASC", id_cat_sel=id_cat))
        elif request.method == "GET":
            strsql_id_cat = "SELECT id_cat, title_cat, description_cat, icon_cat, fk_section FROM t_categories WHERE id_cat = %(id_cat)s"
            select_dictionary = {"id_cat": id_cat}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(strsql_id_cat, select_dictionary)
            data_cat = mybd_conn.fetchone()
            print("Data cats ", data_cat, " type ", type(data_cat), " cat ",
                  data_cat["title_cat"], data_cat["description_cat"], data_cat["icon_cat"])

            form.title_cat.default = data_cat["title_cat"]
            form.description_cat.default = data_cat["description_cat"]
            form.icon_cat.default = data_cat["icon_cat"]
            form.fk_section.default = data_cat["fk_section"]
            form.process()

    except Exception as Exception_category_update:
        raise ExceptionCategoryUpdate(f"file : {Path(__file__).name}  ;  "
                                      f"{category_update.__name__} ; "
                                      f"{Exception_category_update}")

    return render_template("categories/category_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /category_delete route
    
    Test : ex : http://127.0.0.1:5005/category_delete
    
    Settings : -
    
    Goal : Delete a cats who has been selected in /categories_display
"""


@app.route("/category_delete", methods=['GET', 'POST'])
def category_delete():
    data_delete = None
    delete_btn = None
    id_cat = request.values['id_cat']

    form = FormDeleteCategory()
    try:
        strsql_sections = "SELECT id_section, title_section FROM t_sections INNER JOIN t_categories ON fk_section = id_section WHERE id_cat = %(id_cat)s"
        id_cat_dict = {"id_cat": id_cat}
        with DBconnection() as mybd_conn:
            mybd_conn.execute(strsql_sections, id_cat_dict)
        data_sections = mybd_conn.fetchall()

        sections_list = []
        for i in data_sections:
            sections_list.append(i['title_section'])
        form.fk_section.choices = sections_list
        print(" on submit ", form.validate_on_submit())
        if request.method == "POST" and form.validate_on_submit():

            if form.cancel_btn.data:
                return redirect(url_for("categories_display", order_by="ASC", id_cat_sel=0))

            if form.del_conf_btn.data:
                data_delete = session['data_delete']
                print("Data to delete ", data_delete)

                flash(f"Supprimer la category définitivement ?", "danger")
                delete_btn = True

            if form.del_final_btn.data:
                delete_dictionary = {"id_cat": id_cat}
                print("Dictionary : ", delete_dictionary)

                strsql_delete_threads_have_category = """UPDATE t_threads SET fk_cat=NULL WHERE fk_cat = %(id_cat)s;UPDATE t_categories SET fk_cat=NULL WHERE fk_cat = %(id_cat)s"""
                strsql_delete_id_cat = """DELETE FROM t_categories WHERE id_cat = %(id_cat)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_threads_have_category, delete_dictionary)
                    mconn_bd.execute(strsql_delete_id_cat, delete_dictionary)

                flash(f"La category a été supprimé !", "success")
                print(f"Categories deleted.")

                return redirect(url_for('categories_display', order_by="ASC", id_cat_sel=0))

        if request.method == "GET":
            select_dictionary = {"id_cat": id_cat}
            print(id_cat, type(id_cat))

            strsql_threads_delete = """SELECT title_thread, content_thread,icon_thread, id_cat, id_thread FROM t_threads t
                                            LEFT JOIN t_categories c ON t.fk_cat = id_cat
                                            WHERE t.fk_cat = %(id_cat)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(strsql_threads_delete, select_dictionary)
                data_delete = mydb_conn.fetchall()
                print("Data to delete : ", data_delete)

                session['data_delete'] = data_delete

                strsql_id_cat = "SELECT id_cat, title_cat, description_cat, icon_cat, title_section FROM t_categories LEFT JOIN t_sections ON fk_section = id_section WHERE id_cat = %(id_cat)s"

                mydb_conn.execute(strsql_id_cat, select_dictionary)
                data_title_cat = mydb_conn.fetchone()
                print("Data category ", data_title_cat, " type ", type(data_title_cat), " category ",
                      data_title_cat["title_cat"], data_title_cat["description_cat"], data_title_cat["icon_cat"])

            form.title_cat.data = data_title_cat["title_cat"]
            form.description_cat.data = data_title_cat["description_cat"]
            form.icon_cat.data = data_title_cat["icon_cat"]
            form.fk_section.data = data_title_cat["title_section"]

            delete_btn = False

    except Exception as Exception_category_delete:
        raise ExceptionCategoryDelete(f"file : {Path(__file__).name}  ;  "
                                      f"{category_delete.__name__} ; "
                                      f"{Exception_category_delete}")

    return render_template("categories/category_delete.html",
                           form=form,
                           delete_btn=delete_btn,
                           data_threads_linked=data_delete)

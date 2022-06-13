"""Route for sections CRUD
File : gestion_sections_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.sections.gestion_sections_forms import FormAddSection
from APP_Forums_164.sections.gestion_sections_forms import FormDeleteSection
from APP_Forums_164.sections.gestion_sections_forms import FormUpdateSection

"""
    Author : Raphaël Doutaz 09.05.22
    Set /sections_display route
    
    Test : ex : http://127.0.0.1:5005/sections_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_section_sel = 0 >> all sections.
                id_section_sel = "n" display sections who id is "n"
"""


@app.route("/sections_display/<string:order_by>/<int:id_section_sel>", methods=['GET', 'POST'])
def sections_display(order_by, id_section_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_section_sel == 0:
                    strsql_sections_display = """SELECT id_section, title_section, description_section FROM t_sections ORDER BY title_section ASC"""
                    mc_display.execute(strsql_sections_display)
                elif order_by == "ASC":
                    select_dictionary = {"id_section_selected": id_section_sel}
                    strsql_sections_display = """SELECT id_section, title_section, description_section FROM t_sections WHERE id_section = %(id_section_selected)s"""

                    mc_display.execute(strsql_sections_display, select_dictionary)
                else:
                    strsql_sections_display = """SELECT id_section, title_section, description_section FROM t_sections  ORDER BY id_section DESC"""

                    mc_display.execute(strsql_sections_display)

                data_sections = mc_display.fetchall()

                print("Data sections : ", data_sections, " Type : ", type(data_sections))

                # If table is empty
                if not data_sections and id_section_sel == 0:
                    flash("""La table "t_sections" est vide.""", "warning")
                elif not data_sections and id_section_sel > 0:
                    # If no sections with id = id_section_sel found
                    flash(f"La section que vous avez demandé n'existe pas.", "warning")
                else:
                    # In all others cases, this means the table is empty.
                    flash(f"Les données des sections ont été affichées !", "success")

        except Exception as Exception_sections_display:
            raise ExceptionSectionsDisplay(f"file : {Path(__file__).name}  ;  "
                                           f"{sections_display.__name__} ; "
                                           f"{Exception_sections_display}")

    return render_template("sections/sections_display.html", data=data_sections)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /section_add route
    
    Test : ex : http://127.0.0.1:5005/section_add
    
    Settings : -
    
    Goal : Add a sections
"""


@app.route("/section_add", methods=['GET', 'POST'])
def section_add():
    form = FormAddSection()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                insertion_dictionary = {"title_section": form.title_section.data,
                                        "description_section": form.description_section.data}
                print("Dictionary : ", insertion_dictionary)

                strsql_insert_section = """INSERT INTO t_sections (id_section,title_section,description_section) VALUES (NULL,%(title_section)s,%(description_section)s) """

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_section, insertion_dictionary)

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('sections_display', order_by='DESC', id_section_sel=0))

        except Exception as Exception_sections_add:
            raise ExceptionSectionAdd(f"file : {Path(__file__).name}  ;  "
                                      f"{section_add.__name__} ; "
                                      f"{Exception_sections_add}")

    return render_template("sections/section_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /section_update route
    
    Test : ex : http://127.0.0.1:5005/section_update
    
    Settings : -
    
    Goal : Update a sections who has been selected in /sections_display
"""


@app.route("/section_update", methods=['GET', 'POST'])
def section_update():
    id_section = request.values['id_section']

    form = FormUpdateSection()
    try:
        print(" on submit ", form.validate_on_submit())
        if form.validate_on_submit():
            update_dictionary = {"id_section": id_section,
                                 "title_section": form.title_section.data,
                                 "description_section": form.description_section.data
                                 }
            print("Dictionnary : ", update_dictionary)

            strsql_update_section = """UPDATE t_sections SET title_section = %(title_section)s,description_section = %(description_section)s WHERE id_section = %(id_section)s;"""
            with DBconnection() as mconn_bd:
                mconn_bd.execute(strsql_update_section, update_dictionary)

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('sections_display', order_by="ASC", id_section_sel=id_section))
        elif request.method == "GET":
            strsql_id_section = "SELECT id_section, title_section, description_section FROM t_sections WHERE id_section = %(id_section)s"
            select_dictionary = {"id_section": id_section}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(strsql_id_section, select_dictionary)
            data_section = mybd_conn.fetchone()
            print("Data sections ", data_section, " type ", type(data_section), " section ",
                  data_section["title_section"], data_section["description_section"])

            form.title_section.data = data_section["title_section"]
            form.description_section.data = data_section["description_section"]

    except Exception as Exception_section_update:
        raise ExceptionSectionUpdate(f"file : {Path(__file__).name}  ;  "
                                     f"{section_update.__name__} ; "
                                     f"{Exception_section_update}")

    return render_template("sections/section_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /section_delete route
    
    Test : ex : http://127.0.0.1:5005/section_delete
    
    Settings : -
    
    Goal : Delete a sections who has been selected in /sections_display
"""


@app.route("/section_delete", methods=['GET', 'POST'])
def section_delete():
    data_delete = None
    delete_btn = None
    id_section = request.values['id_section']

    form = FormDeleteSection()
    try:
        print(" on submit ", form.validate_on_submit())
        if request.method == "POST" and form.validate_on_submit():

            if form.cancel_btn.data:
                return redirect(url_for("sections_display", order_by="ASC", id_section_sel=0))

            if form.del_conf_btn.data:
                data_delete = session['data_delete']
                print("Data to delete ", data_delete)

                flash(f"Supprimer la section définitivement ?", "danger")
                delete_btn = True

            if form.del_final_btn.data:
                delete_dictionary = {"id_section": id_section}
                print("Dictionary : ", delete_dictionary)

                strsql_delete_cats_have_section = """UPDATE t_categories SET fk_section=NULL WHERE fk_section = %(id_section)s"""
                strsql_delete_id_section = """DELETE FROM t_sections WHERE id_section = %(id_section)s"""
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_delete_cats_have_section, delete_dictionary)
                    mconn_bd.execute(strsql_delete_id_section, delete_dictionary)

                flash(f"La section a été supprimé !", "success")
                print(f"Sections deleted.")

                return redirect(url_for('sections_display', order_by="ASC", id_section_sel=0))

        if request.method == "GET":
            select_dictionary = {"id_section": id_section}
            print(id_section, type(id_section))

            strsql_cats_delete = """SELECT title_cat, description_cat,icon_cat, id_section, id_cat FROM t_categories
                                            LEFT JOIN t_sections r ON fk_section = id_section
                                            WHERE fk_section = %(id_section)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(strsql_cats_delete, select_dictionary)
                data_delete = mydb_conn.fetchall()
                print("Data to delete : ", data_delete)

                session['data_delete'] = data_delete

                strsql_id_section = "SELECT id_section, title_section, description_section FROM t_sections WHERE id_section = %(id_section)s"

                mydb_conn.execute(strsql_id_section, select_dictionary)
                data_title_section = mydb_conn.fetchone()
                print("Data section ", data_title_section, " type ", type(data_title_section), " section ",
                      data_title_section["title_section"], data_title_section["description_section"])

            form.title_section.data = data_title_section["title_section"]
            form.description_section.data = data_title_section["description_section"]

            delete_btn = False

    except Exception as Exception_section_delete:
        raise ExceptionSectionDelete(f"file : {Path(__file__).name}  ;  "
                                     f"{section_delete.__name__} ; "
                                     f"{Exception_section_delete}")

    return render_template("sections/section_delete.html",
                           form=form,
                           delete_btn=delete_btn,
                           data_cats_linked=data_delete)

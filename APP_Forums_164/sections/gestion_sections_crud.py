"""Route for sections CRUD
File : gestion_sections_crud.py
Author : Raphaël Doutaz 09.05.22
"""
from pathlib import Path

from APP_Forums_164.database.database_tools import DBconnection
from flask import redirect, request, session, url_for

from APP_Forums_164.erreurs.exceptions import *
from APP_Forums_164.sections.gestion_sections_forms import FormSection

"""
    Author : Raphaël Doutaz 09.05.22
    Set /sections_display route
    
    Test : ex : http://127.0.0.1:5005/sections_display
    
    Settings :  order_by : ASC : Ascendant, DESC : Descendant
                id_section = 0 >> all sections.
                id_section = "n" display sections who id is "n"
"""


@app.route("/sections_display/<string:order_by>/<int:id_section>", methods=['GET', 'POST'])
def sections_display(order_by, id_section):
    if request.method == "GET":
        try:
            with DBconnection() as mc_display:
                if order_by == "ASC" and id_section == 0:
                    mc_display.execute("""SELECT id_section, title_section, description_section FROM t_sections ORDER BY id_section ASC""")
                elif order_by == "ASC":
                    mc_display.execute("""SELECT id_section, title_section, description_section FROM t_sections WHERE id_section = %(id_sectionected)s ORDER BY id_section ASC""", {"id_sectionected": id_section})
                else:
                    mc_display.execute("""SELECT id_section, title_section, description_section FROM t_sections  ORDER BY id_section DESC""")

                data = mc_display.fetchall()

                print("Data sections : ", data)

                if not data and id_section == 0:
                    flash("""La table "t_sections" est vide.""", "warning")
                elif not data and id_section > 0:
                    flash(f"La section que vous avez demandé n'existe pas.", "warning")
                else:
                    flash(f"Les données des sections ont été affichées !", "success")

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                           f"{sections_display.__name__} ; "
                                           f"{exception_pass}")

    return render_template("sections/sections_display.html", data=data)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /section_add route
    
    Test : ex : http://127.0.0.1:5005/section_add
    
    Settings : -
    
    Goal : Add a section
"""


@app.route("/section_add", methods=['GET', 'POST'])
def section_add():
    form = FormSection()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""INSERT INTO t_sections (id_section,title_section,description_section) VALUES (NULL,%(title_section)s,%(description_section)s)""",
                                     {
                                         "title_section": form.title_section.data,
                                         "description_section": form.description_section.data
                                     })

                flash(f"Les données ont été insérées !", "success")
                print(f"Data inserted !")

                return redirect(url_for('sections_display', order_by='ASC', id_section=0))

        except Exception as exception_pass:
            raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                      f"{section_add.__name__} ; "
                                      f"{exception_pass}")

    return render_template("sections/section_add.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /section_update route
    
    Test : ex : http://127.0.0.1:5005/section_update
    
    Settings : -
    
    Goal : Update a section who has been selected in /sections_display
"""


@app.route("/section_update/<int:id_section>", methods=['GET', 'POST'])
def section_update(id_section):
    form = FormSection()
    try:
        if form.validate_on_submit():
            with DBconnection() as mconn_bd:
                mconn_bd.execute("""UPDATE t_sections SET title_section = %(title_section)s,description_section = %(description_section)s WHERE id_section = %(id_section)s;""",
                                 {
                                     "id_section": id_section,
                                     "title_section": form.title_section.data,
                                     "description_section": form.description_section.data
                                 })

            flash(f"Les données ont été mises à jour !", "success")
            print(f"Data updated !")

            return redirect(url_for('sections_display', order_by="ASC", id_section=id_section))

        elif request.method == "GET":
            with DBconnection() as mybd_conn:
                mybd_conn.execute("SELECT id_section, title_section, description_section FROM t_sections WHERE id_section = %(id_section)s", {"id_section": id_section})
            data = mybd_conn.fetchone()
            print("Data sections ", data)

            form.title_section.data = data["title_section"]
            form.description_section.data = data["description_section"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                     f"{section_update.__name__} ; "
                                     f"{exception_pass}")

    return render_template("sections/section_update.html", form=form)


"""
    Author : Raphaël Doutaz 09.05.22
    Set /section_delete route
    
    Test : ex : http://127.0.0.1:5005/section_delete
    
    Settings : -
    
    Goal : Delete a section who has been selected in /sections_display
"""


@app.route("/section_delete/<int:id_section>", methods=['GET', 'POST'])
def section_delete(id_section):
    form = FormSection()
    try:
        if request.method == "POST" and form.validate_on_submit():
            if form.submit_cancel.data:
                return redirect(url_for("sections_display", order_by="ASC", id_section=0))

            if form.submit_delete.data:
                with DBconnection() as mconn_bd:
                    mconn_bd.execute("""UPDATE t_categories SET fk_section=NULL WHERE fk_section = %(id_section)s; DELETE FROM t_sections WHERE id_section = %(id_section)s""", {"id_section": id_section})

                flash(f"La section a été supprimé !", "success")
                print(f"Sections deleted.")

                return redirect(url_for('sections_display', order_by="ASC", id_section=0))

        if request.method == "GET":
            with DBconnection() as mydb_conn:
                mydb_conn.execute("""SELECT title_cat, description_cat,icon_cat, id_section, id_cat FROM t_categories
                                            LEFT JOIN t_sections r ON fk_section = id_section
                                            WHERE fk_section = %(id_section)s""", {"id_section": id_section})
                data_linked = mydb_conn.fetchall()
                session['data_linked'] = data_linked

                mydb_conn.execute("SELECT id_section, title_section, description_section FROM t_sections WHERE id_section = %(id_section)s", {"id_section": id_section})
                data = mydb_conn.fetchone()
                print("Data section ", data)

            form.title_section.data = data["title_section"]
            form.description_section.data = data["description_section"]

    except Exception as exception_pass:
        raise ExceptionPass(f"file : {Path(__file__).name}  ;  "
                                     f"{section_delete.__name__} ; "
                                     f"{exception_pass}")

    return render_template("sections/section_delete.html",
                           form=form,
                           data_linked=data_linked)

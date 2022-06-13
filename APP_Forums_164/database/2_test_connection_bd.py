"""
File : 2_test_connection_bd.py
Author : Raphaël Doutaz 18.05.22
"""

from APP_Forums_164.database.database_tools import DBconnection

try:
    """
        Une seule requête pour montrer la récupération des données de la BD en MySql.
    """
    strsql_roles_display = """SELECT id_user, nickname_user FROM t_users ORDER BY nickname_user ASC"""

    with DBconnection() as db:
        db.execute(strsql_roles_display)
        result = db.fetchall()
        print("data_users ", result, " Type : ", type(result))


except Exception as erreur:
    # print(f"2547821146 Connection à la BD Impossible ! {type(erreur)} args {erreur.args}")
    print(f"2547821146 Test connection BD !"
          f"{__name__, erreur} , "
          f"{repr(erreur)}, "
          f"{type(erreur)}")

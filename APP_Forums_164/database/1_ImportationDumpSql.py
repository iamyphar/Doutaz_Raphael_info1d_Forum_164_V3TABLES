"""
    File : 1_ImportationDumpSql.py
    Author : Raphaël Doutaz 18.05.22

    On obtient un objet "objet_dumpbd"

    Cela permet de construire la base de donnée à partir de votre file DUMP en SQL
    obtenu par l'exportation de votre bd dans PhpMyAdmin.
    Le file .env doit être correctement paramétré. (host, user, password, nomdevotrebd)
    Le file DUMP de la BD doit se trouver dans le répertoire "database" de votre projet Python.

    On signale les erreurs importantes
"""
from APP_Forums_164.database import database_tools

try:
    objet_dumpbd = database_tools.ToolsBd().load_dump_sql_bd_init()
except Exception as erreur_load_dump_sql:
    print(f"Initialisation de la BD Impossible ! (voir DUMP ou .env) "
          f"{erreur_load_dump_sql.args[0]} , "
          f"{erreur_load_dump_sql}")

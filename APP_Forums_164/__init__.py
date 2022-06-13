"""Initialisation des variables d'environnement
    Author : Raphaël Doutaz 2021.03.03 Indispensable pour définir les variables indispensables dans tout le projet.
"""
import sys

from environs import Env
from flask import Flask

try:
    try:
        obj_env = Env()
        obj_env.read_env()
        HOST_MYSQL = obj_env("HOST_MYSQL")
        USER_MYSQL = obj_env("USER_MYSQL")
        PASS_MYSQL = obj_env("PASS_MYSQL")
        PORT_MYSQL = int(obj_env("PORT_MYSQL"))
        NAME_BD_MYSQL = obj_env("NAME_BD_MYSQL")
        NAME_FILE_DUMP_SQL_BD = obj_env("NAME_FILE_DUMP_SQL_BD")

        ADRESSE_SRV_FLASK = obj_env("ADRESSE_SRV_FLASK")
        DEBUG_FLASK = obj_env("DEBUG_FLASK")
        PORT_FLASK = obj_env("PORT_FLASK")
        SECRET_KEY_FLASK = obj_env("SECRET_KEY_FLASK")

        # Raphaël Doutaz 2022.04.11 Début de l'application
        app = Flask(__name__, template_folder="templates")
        print("app.url_map ____> ", app.url_map)

    except Exception as erreur:
        print(f"45677564530 init application variables d'environnement ou avec le file (son nom, son contenu)\n"
              f"{__name__}, "
              f"{erreur.args[0]}, "
              f"{repr(erreur)}, "
              f"{type(erreur)}")
        sys.exit()

    """
        Tout commence ici. Il faut "indiquer" les routes de l'applicationn.    
        Dans l'application les lignes ci-dessous doivent se trouver ici... soit après l'instanciation de la classe "Flask"
    """
    from APP_Forums_164.database import database_tools
    from APP_Forums_164.roles import gestion_roles_crud, gestion_users_have_roles_crud
    from APP_Forums_164.chars import gestion_chars_crud
    from APP_Forums_164.chars import gestion_chars_forms
    from APP_Forums_164.sections import gestion_sections_crud
    from APP_Forums_164.sections import gestion_sections_forms
    from APP_Forums_164.cats import gestion_cats_crud
    from APP_Forums_164.cats import gestion_cats_forms
    from APP_Forums_164.threads import gestion_threads_crud
    from APP_Forums_164.threads import gestion_threads_forms
    from APP_Forums_164.resps import gestion_resps_crud
    from APP_Forums_164.resps import gestion_resps_forms
    from APP_Forums_164.perms import gestion_perms_crud
    from APP_Forums_164.perms import gestion_perms_forms
    from APP_Forums_164.home import home

    from APP_Forums_164.erreurs import msg_avertissements

    from APP_Forums_164.users import gestion_users_crud
    from APP_Forums_164.chars import gestion_users_have_chars_crud
    from APP_Forums_164.perms import gestion_roles_have_perms_crud
    from APP_Forums_164.users import gestion_users_forms

except Exception as Exception_init_app_users_164:
    print(f"4567756434 Une erreur est survenue {type(Exception_init_app_users_164)} dans "
          f"__init__ {Exception_init_app_users_164.args}")
    sys.exit()

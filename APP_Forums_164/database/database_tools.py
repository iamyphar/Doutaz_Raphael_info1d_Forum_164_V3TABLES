"""
File : database_tools.py
Author : Raphaël Doutaz 18.05.22
Nécessite un file de configuration externe : ".env"
Nécessite un file DUMP en MySql de la BD : /database/NOM_PRENOM_INFO1X_SUJET_164_2022.sql
"""
import os
import re

import pymysql
import sqlparse
from pymysql.constants import CLIENT
from pymysql.err import ProgrammingError

from APP_Forums_164 import HOST_MYSQL
from APP_Forums_164 import NAME_BD_MYSQL
from APP_Forums_164 import NAME_FILE_DUMP_SQL_BD
from APP_Forums_164 import PASS_MYSQL
from APP_Forums_164 import PORT_MYSQL
from APP_Forums_164 import USER_MYSQL
from APP_Forums_164.erreurs.exceptions import *


class ToolsBd:
    """Outils en rapport avec la base de données.
    Author : Raphaël Doutaz 2021.03.03
    Nom classe : ToolsBd
    Classe pour définir quelques outils en rapport avec la base de données.
    """

    @staticmethod
    def extract_name_bd_from_dump_file():
        """Automatise la création de la bd par la lecture du nom de file contenu dans le DUMP;
        Author : Raphaël Doutaz 2021.03.09
        Nom : extract_name_bd_from_dump_file(self)
        But : Extrait la chaîne de caractère du nom de la base de donnée contenu dans le file :
                    "NOM_PRENOM_INFO1X_SUJET_164_2022.sql"
                    à la ligne de commande "USE NOM_PRENOM_INFO1X_SUJET_164_2021;"
        """
        extract_nom_bd = ""
        try:

            if os.path.exists(NAME_FILE_DUMP_SQL_BD):
                file_dump_sql_bd = open(NAME_FILE_DUMP_SQL_BD, "r", encoding="utf8")
                lignes_file_dump = file_dump_sql_bd.read()
                extract_nom_bd = re.search(r'USE(.*?);', lignes_file_dump).group(1)

                # Extrait le nom de la BD après suppression des espaces autour de la chaîne de caractères.
                extract_nom_bd = extract_nom_bd.strip()
                print("extract_nom_bd ", extract_nom_bd)
                file_dump_sql_bd.close()
            else:
                print(f"Le file DUMP n'existe pas !!!")
        except Exception as erreur_extract_name_bd:
            # raise ErreurExtractNameBD(f"Problème avec l'extraction du nom de la BD {erreur_extract_name_bd.args[0]}")
            print(f"Problème avec l'extraction du nom de la BD ! (voir DUMP ou .env) "
                  f"{erreur_extract_name_bd.args[0]} , "
                  f"{erreur_extract_name_bd}")
        return extract_nom_bd

    @staticmethod
    def test_cmd_CRD_file_dump_sql():
        """Lecture du file DUMP et détection des erreurs à la création de la bd.
        Author : Raphaël Doutaz 2021.03.09
        Nom : test_cmd_CRD_file_dump_sql(self)
        Tester si il y a des problèmes éventuels sur le file : "NOM_PRENOM_INFO1X_SUJET_164_2022.sql"
        Son emplacement, son nom, son ouverture et s'il contient les commandes MySql suivantes :
            DROP DATABASE IF EXIST nom_bd; CREATE DATABASE IF NOT EXISTS nom_bd; USE nom_bd;
            (Commandes obligatoires pour le MODULE 164, afin de garantir la dernière version de la BD)
        """
        lignes_file_sql = ""
        try:
            if os.path.exists(NAME_FILE_DUMP_SQL_BD):
                file_dump_sql_bd = open(NAME_FILE_DUMP_SQL_BD, "r", encoding="utf8")
                lignes_file_dump = file_dump_sql_bd.read()
                """Si le file DUMP en SQL "../database/NOM_PRENOM_INFO1X_SUJET_164_2022.sql" existe, 
                    on l'ouvre et il est "découpé" dans une LISTE ligne par ligne.
                    Dans une boucle FOR chaque élément de la liste (ligne du file) est "executée"
                    sur le Serveur MySql
                    On valide la transaction par un "commit".
                    On ferme ce qui est ouvert (file, curseur de la BD, connection à la BD)
                """

                lignes_file_sql = sqlparse.split(lignes_file_dump)
                print(" lignes_sql ", lignes_file_sql, "....", type(lignes_file_sql))

                sql_cmd_drop_bd = lignes_file_dump.find("DROP DATABASE IF EXISTS")
                sql_cmd_create_bd = lignes_file_dump.find("CREATE DATABASE IF NOT EXISTS")
                sql_cmd_use_bd = lignes_file_dump.find("USE")

                """
                    Pour CE projet et uniquement dans des projets (d'école) ou l'on doit reconstruire la BD.
                    Ne jamais oublier qu'il faut les 3 instructions dans le file DUMP en SQL
                    DROP DATABASE IF EXIST nom_bd; CREATE DATABASE IF NOT EXISTS nom_bd; USE nom_bd;
                """
                if sql_cmd_drop_bd == -1:
                    raise ErreurFileSqlDump("File DUMP : Il manque une commande \"DROP DATABASE IF EXIST\"")
                elif sql_cmd_create_bd == -1:
                    raise ErreurFileSqlDump(
                        "File DUMP : Il manque une commande \"CREATE DATABASE IF NOT EXISTS\"")
                elif sql_cmd_use_bd == -1:
                    raise ErreurFileSqlDump("File DUMP : Il manque une commande \"USE\"")
                else:
                    file_dump_sql_bd.close()
                    print(f"Les instructions DROP; CREATE ; USE sont ok dans le file DUMP en SQL")
            else:
                print(f"Problème avec le File DUMP SQL")

        except Exception as erreur_file_sql_dump:
            print(f"Mauvais paramètres dans (.env) "
                  f"{erreur_file_sql_dump.args[0]}, "
                  f"{erreur_file_sql_dump}")
            raise ErreurFileSqlDump("Problème avec le File DUMP SQL !!! (nom, emplacement, etc)")

        return lignes_file_sql

    def load_dump_sql_bd_init(self):
        """
            Author : Raphaël Doutaz 2021.03.09
            Nom : load_dump_sql_bd_init(self)
            Méthode pour charger le file DUMP en SQL dans le serveur MySql.

            autocommit=False ==> Oblige le programmeur à ordonner la confirmation (commit) de la transaction dans la BD.

            1) Récupérer les paramètres de la configuration dans le file ".env"
            2) Se connecter à la BD
            3) Tester si les instructions MySql
                DROP DATABASE IF EXIST nom_bd; CREATE DATABASE IF NOT EXISTS nom_bd; USE nom_bd;
            4) Parcourir les lignes du file DUMP en MySql et les exécuter dans le serveur MySql.
        """
        try:
            try:
                print("HOST_MYSQL", HOST_MYSQL)
                conn_bd_dump = pymysql.connect(
                    host=HOST_MYSQL,
                    user=USER_MYSQL,
                    password=PASS_MYSQL,
                    port=PORT_MYSQL,
                    autocommit=False)

                lignes_file_sql = self.test_cmd_CRD_file_dump_sql()

                if lignes_file_sql:
                    for ligne in lignes_file_sql:
                        nb_row_sql = conn_bd_dump.cursor().execute(ligne)
                        print("lignes sql executées  ", nb_row_sql)
                    conn_bd_dump.commit()
                else:
                    raise ErreurFileSqlDump("File DUMP SQL vide, C'EST étrange !!!")

            except AttributeError as erreur_attr:
                print(f"Mauvais paramètres dans (.env) "
                      f"{erreur_attr.args[0]}, "
                      f"{erreur_attr}")
                raise
            except pymysql.OperationalError as erreur_connection:
                print(f"Erreur de configu. dans la connection de la BD "
                      f"{erreur_connection.args[0]}, "
                      f"{erreur_connection}")
                raise
            except Exception as erreur_load_dump:
                print(f"Erreur particulière load_dump_sql_bd_init "
                      f"{erreur_load_dump.args[0]}, "
                      f"{erreur_load_dump}")
                raise
            else:
                conn_bd_dump.close()
                print("File DUMP SQL chargé dans le serveur MySql")
        except (Exception,
                ConnectionRefusedError,
                AttributeError,
                pymysql.err.OperationalError,
                pymysql.err.DatabaseError) as erreur_load_dump_file:
            print(f"Erreur particulière load_dump_sql_bd_init "
                  f"{erreur_load_dump_file.args[0]}, "
                  f"{erreur_load_dump_file}")
            raise ErreurFileSqlDump("Problème avec le File DUMP SQL !!!")


"""
    Author : Raphaël Doutaz 2022.03.29
    Nom : DBconnection
    Se connecter à la BD avec les paramètres de connection suivants :
        1) Dans le file : .env

    client_flag=CLIENT.MULTI_STATEMENTS ==> Indispensable pour pouvoir passer plusieurs
    requêtes en une seule fois.

    autocommit=False ==> Oblige le programmeur à ordonner la confirmation (commit) de la transaction dans la BD.

    cursorclass=pymysql.cursors.DictCursor ==> Retourne les données de la BD sous la forme d'un Dictionary

"""


class DBconnection:
    # Quand on instancie la classe il interprète le code __init__
    def __init__(self):

        connection = pymysql.connect(
            host=HOST_MYSQL,
            user=USER_MYSQL,
            password=PASS_MYSQL,
            port=PORT_MYSQL,
            database=NAME_BD_MYSQL,
            client_flag=CLIENT.MULTI_STATEMENTS,
            autocommit=False,
            cursorclass=pymysql.cursors.DictCursor)

        try:
            print(f'Connection avec la BD active !')
            self.connection = connection

        except Exception as erreur:
            # raise print(f"11145522154 Problème de connection dans {self.__class__.__name__} constructor")
            print(f"2547821167 Connection à la BD Impossible !"
                  f"{erreur.args[0]} , "
                  f"{repr(erreur)}, "
                  f"{type(erreur)}")

    def __enter__(self):
        print("__enter__ CM")
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type == ProgrammingError:
            print(f"77324234687788 Erreur Database exception {self.__class__.__name__} methode exit ")
            # raise raise_mysql_exception(exc_val)
            raise SqlSyntaxError(f"Erreur de syntaxe : {exc_val}")
        # # if exc_type == ProgrammingError or exc_type == OperationalError:
        # #     print(f"23436677 Exit CM  !"
        # #           f"{exc_type} , "
        # #           f"{repr(exc_val)}, "
        # #           f"{type(exc_val)}")
        # # if exc_type == ProgrammingError or exc_type == OperationalError:
        # #     self.close(1)
        # #     # raise SqlSyntaxError(f"Erreur de syntaxe : {exc_val}")
        # #     print(f"3435553 Erreur de syntaxe : {exc_val}")
        #
        # elif exc_type == IntegrityError:
        #     self.close(1)
        #     # raise IntegrityConstraintException(f"Doublons {exc_val}")
        #     print(f"566473 Doublons {exc_val}")
        #
        # elif exc_type == DataError:
        #     self.close(1)
        #     # raise DatabaseException(f"Erreur Database exception {self.__class__.__name__} methode exit ")
        #     print(f"773242346 Erreur Database exception {self.__class__.__name__} methode exit ")

        elif exc_type is not None:
            self.close(1)
            raise DatabaseException(f"{exc_type} exception dans {self.__class__.__name__} methode exit :  {exc_val}")
            # print(f"{exc_type} exception dans {self.__class__.__name__} methode exit :  {exc_val}")

        if exc_val is None:
            self.close(0)

        else:
            print("exc_type ", exc_type, "  ", exc_val.args[1])
            print("exc_val ", exc_val, "  ", exc_val.args[0])
            print("traceback ", traceback)
            print("sys.exc_info() --> ", sys.exc_info())
            raise DatabaseException(f"{exc_type} exception dans {self.__class__.__name__} methode exit :  {exc_val}")
            self.close(1)

    def close(self, closetype: int):
        if closetype == 1:
            print("Aucun changement dans la BD, rollback")
            self.connection.rollback()

        else:
            print("Commit effectué ! ")
            self.connection.commit()

        self.connection.close()
        print("Fermeture connection BD")

# Module 164 2022.06.11

---

#### Pré-requis

* Un serveur MySql doit être installé
    * UWAMP : sur le site de "UWAMP", lire "Prerequisites IMPORTANT!!" (vous devez installer une des distributions
      Visual C++, j'ai choisi la plus récente)
    * UWAMP : installer la version "EXE" (Choisir : Télécharger Exe/Install) est préférable à la version "PORTABLE"
    * UWAMP : accepter les 2 alertes de sécurité d'accès aux réseaux (apache et MySql)
    * MAC : MAMP ou https://www.codeur.com/tuto/creation-de-site-internet/version-mysql/
    * Contrôler que tout fonctionne bien. Ouvrir "UWAMP". Cliquer sur le bouton "PhpMyAdmin". Utilisateur : root Mot de
      passe : root
* Python doit être installé.
    * ATTENTION : Cocher la case pour que le "PATH" intègre le programme Python
    * Une fois la "case à cocher" du PATH cochée, il faut choisir d'installer
    * Un peu avant la fin du processus d'intallation, cliquer sur "disabled length limit" et cliquer sur "CLOSE"
    * Le test de Python se fait après avec le programme "PyCharm"
* "PyCharm" (community) doit être intallé, car toutes mes démonstrations sont faites avec cette version de l'IDE. INFO :
  Vous pouvez télécharger tous les produits de JetBrains car vous êtes étudiant.
    * Lors de l'installation, il faut cocher toutes les options ASSOCIATIONS, ADD PATH, etc
    * Ouvrir "PyCharm" pour la première fois pour le configurer. Choisir le bouton "New Project"
    * Changer le répertoire pour ce nouveau projet, il faut créer un nouveau répertoire "vide" dans votre ordi en local.
    * Il est important d'avoir sélectionné le répertoire que vous venez de créer car "PyCharm" va automatiquement créer
      un environnement virtuel (venv) dans ce répertoire
    * Menu : File->Settings->Updateor->General->Auto Import (rubrique Python) cocher "Show auto-import tooltip"
    * PyCharm vient d'ouvrir une fenêtre avec le contenu du "main.py" pour configurer les actions "UNDO" et "REDO"
    * Sélectionner tout le texte avec "CTRL-A" puis "CTRL-X" (Couper), puis "CTL-Z" (UNDO) et faites un REDO "CTRL-Y"
      et "PyCharm" va vous demander de choisir l'action du "CTRL-Y" raccourci pour faire un "REDO". (Dans 98% des
      éditeurs de texte, le "CTRL-Y" représente l'action "REDO"... pas chez JetBrains)

## Mode d'emploi de cette démonstration

* Démarrer le serveur MySql (uwamp ou xamp ou mamp, etc)
* Dans "PyCharm", importer la BD à partir du file DUMP
    * Ouvrir le file "database/1_ImportationDumpSql.py"
    * Cliquer avec le bouton droit sur l'onglet de ce file et choisir "run" (CTRL-MAJ-F10)
    * En cas d'erreurs : ouvrir le file ".env" à la racine du projet, contrôler les indications de connexion pour la bd.
* Test simple de la connexion à la BD
    * Ouvrir le file "database/2_test_connection_bd.py"
    * Cliquer avec le bouton droit sur l'onglet de ce file et choisir "run" (CTRL-MAJ-F10)
* Démarrer le microframework FLASK
    * Dans le répertoire racine du projet, ouvrir le file "run_mon_app.py"
    * Cliquer avec le bouton droit sur l'onglet de ce file et choisir "run" (CTRL-MAJ-F10)
    
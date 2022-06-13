--

-- Database: Doutaz_Raphael_info1d_164
-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS Doutaz_Raphael_info1d_164;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS Doutaz_Raphael_info1d_164;

-- Utilisation de cette base de donnée

USE Doutaz_Raphael_info1d_164;

# ************************************************************
# Sequel Ace SQL dump
# Version 20031
#
# https://sequel-ace.com/
# https://github.com/Sequel-Ace/Sequel-Ace
#
# Host: localhost (MySQL 5.7.36)
# Database: Doutaz_Raphael_info1d_164
<<<<<<< HEAD
# Generation Time: 2022-05-25 05:08:12 +0000
=======
# Generation Time: 2022-06-12 19:47:56 +0000
>>>>>>> 5a0505c (BD changes)
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE='NO_AUTO_VALUE_ON_ZERO', SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table t_categories
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_categories`;

CREATE TABLE `t_categories` (
  `id_cat` int(11) NOT NULL AUTO_INCREMENT,
  `title_cat` varchar(64) NOT NULL,
  `description_cat` text NOT NULL,
  `icon_cat` text NOT NULL,
  `fk_cat` int(11) DEFAULT NULL,
  `fk_section` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_cat`),
  KEY `fk_cat` (`fk_cat`),
  KEY `fk_section` (`fk_section`),
  CONSTRAINT `t_categories_ibfk_1` FOREIGN KEY (`fk_cat`) REFERENCES `t_categories` (`id_cat`),
  CONSTRAINT `t_categories_ibfk_2` FOREIGN KEY (`fk_section`) REFERENCES `t_sections` (`id_section`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

LOCK TABLES `t_categories` WRITE;
/*!40000 ALTER TABLE `t_categories` DISABLE KEYS */;

INSERT INTO `t_categories` (`id_cat`, `title_cat`, `description_cat`, `icon_cat`, `fk_cat`, `fk_section`)
VALUES
<<<<<<< HEAD
	(1,'Annonces','Vous retrouvez ici les annonces','/img/categories/default.png',NULL,1),
	(2,'Super','Super2','/img/categories/default.png',NULL,1);
=======
	(1,'Annonces','Vous retrouverez toutes les annonces ici','https://img.freepik.com/free-vector/illustrationn-megaphone-monochrome-style-isolated-white-background_1284-38767.jpg',NULL,1),
	(2,'Questions','Posez vos questions sur tout et n\'importe quoi ici','https://www.zwookedu.ch/miege/zwook/3h-4h-frossard---schriber/defis-du-jour-/questions-/question-mark-1019820_960_720.jpg',NULL,2);
>>>>>>> 5a0505c (BD changes)

/*!40000 ALTER TABLE `t_categories` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_characters
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_characters`;

CREATE TABLE `t_characters` (
  `id_char` int(11) NOT NULL AUTO_INCREMENT,
  `last_name_char` varchar(64) NOT NULL,
  `first_name_char` varchar(64) NOT NULL,
  `bio_char` text,
  `birthdate_char` date NOT NULL,
  `icon_char` text NOT NULL,
  PRIMARY KEY (`id_char`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

LOCK TABLES `t_characters` WRITE;
/*!40000 ALTER TABLE `t_characters` DISABLE KEYS */;

INSERT INTO `t_characters` (`id_char`, `last_name_char`, `first_name_char`, `bio_char`, `birthdate_char`, `icon_char`)
VALUES
<<<<<<< HEAD
	(5,'Raphy','Morte','hey','1998-07-14','/img/chars/default.png'),
	(6,'Álvaro','Morte','eheh','1994-04-12','https://cdn.unitycms.io/images/7Gy45MHQKYq95NMHeMShzK.jpg?op=ocroped&val=1200,1200,1000,450,69,0&sum=cwofrY6nXl4');
=======
	(1,'Raphy','Morte','Salut c\'est Raphy, je viens d\'espagne','1996-07-12','https://staticg.sportskeeda.com/editor/2020/09/6106d-15989009861655-800.jpg'),
	(2,'Morte','Álvaro','Je m\'appelle Álvaro et j\'ai le même nom que l\'acteur du professeur de la casa de papel','1995-04-06','https://cdn.unitycms.io/images/7Gy45MHQKYq95NMHeMShzK.jpg');
>>>>>>> 5a0505c (BD changes)

/*!40000 ALTER TABLE `t_characters` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_emails
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_emails`;

CREATE TABLE `t_emails` (
  `id_email` int(11) NOT NULL AUTO_INCREMENT,
  `name_email` varchar(320) NOT NULL,
  PRIMARY KEY (`id_email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

LOCK TABLES `t_emails` WRITE;
/*!40000 ALTER TABLE `t_emails` DISABLE KEYS */;

INSERT INTO `t_emails` (`id_email`, `name_email`)
VALUES
<<<<<<< HEAD
	(1,'raphaeldoutaz3@gmail.com'),
	(2,'raphaeldoutaz2@gmail.com'),
	(3,'raphaeldoutaz5@gmail.com'),
	(4,'fasdfasdf'),
	(8,'raphaeldoutaz4@gmail.com'),
	(9,'raphaeldoutaz4@gmail.com'),
	(11,'mail'),
	(13,'sadf@sadf.casdf'),
	(14,'ssafdaasdfsdf@asdf.com');
=======
	(1,'contact@yphar.dev'),
	(2,'azecko@gmail.com');
>>>>>>> 5a0505c (BD changes)

/*!40000 ALTER TABLE `t_emails` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_permissions`;

CREATE TABLE `t_permissions` (
  `id_perm` int(11) NOT NULL AUTO_INCREMENT,
  `name_perm` varchar(64) NOT NULL,
  `description_perm` varchar(64) NOT NULL,
  PRIMARY KEY (`id_perm`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

LOCK TABLES `t_permissions` WRITE;
/*!40000 ALTER TABLE `t_permissions` DISABLE KEYS */;

INSERT INTO `t_permissions` (`id_perm`, `name_perm`, `description_perm`)
VALUES
	(1,'ADD_RESPS','ajouter une réponse'),
	(2,'CREATE_THREADS','créer un fil de discussions'),
	(3,'VIEW_THREADS','voir les fils de discussions'),
	(4,'VIEW_RESPS','voir les réponses');

/*!40000 ALTER TABLE `t_permissions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_responses
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_responses`;

CREATE TABLE `t_responses` (
  `id_resp` int(11) NOT NULL AUTO_INCREMENT,
  `content_resp` text NOT NULL,
  `fk_thread` int(11) NOT NULL,
  PRIMARY KEY (`id_resp`),
  KEY `fk_thread` (`fk_thread`),
  CONSTRAINT `t_responses_ibfk_1` FOREIGN KEY (`fk_thread`) REFERENCES `t_threads` (`id_thread`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

LOCK TABLES `t_responses` WRITE;
/*!40000 ALTER TABLE `t_responses` DISABLE KEYS */;

INSERT INTO `t_responses` (`id_resp`, `content_resp`, `fk_thread`)
VALUES
<<<<<<< HEAD
	(2,'trop bien !',1),
	(3,'super !',1);
=======
	(1,'oui raphy insulte ses professeurs et ne réfléchis pas plus loin. il pensait être drôle et dans la continuité de ce qui ce dit encore mais ce n\'est pas le cas.',1),
	(2,'tout à fait d\'accord !',2),
	(3,'merci de la réponse sincère',1);
>>>>>>> 5a0505c (BD changes)

/*!40000 ALTER TABLE `t_responses` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_roles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_roles`;

CREATE TABLE `t_roles` (
  `id_role` int(11) NOT NULL AUTO_INCREMENT,
  `name_role` varchar(64) NOT NULL,
  PRIMARY KEY (`id_role`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

LOCK TABLES `t_roles` WRITE;
/*!40000 ALTER TABLE `t_roles` DISABLE KEYS */;

INSERT INTO `t_roles` (`id_role`, `name_role`)
VALUES
	(1,'USER'),
	(2,'SUPERADMIN'),
	(3,'ADMIN');

/*!40000 ALTER TABLE `t_roles` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_roles_have_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_roles_have_permissions`;

CREATE TABLE `t_roles_have_permissions` (
  `id_role_has_perm` int(11) NOT NULL AUTO_INCREMENT,
  `fk_role` int(11) NOT NULL,
  `fk_perm` int(11) NOT NULL,
  PRIMARY KEY (`id_role_has_perm`),
  KEY `fk_role` (`fk_role`),
  KEY `fk_perm` (`fk_perm`),
  CONSTRAINT `t_roles_have_permissions_ibfk_1` FOREIGN KEY (`fk_role`) REFERENCES `t_roles` (`id_role`),
  CONSTRAINT `t_roles_have_permissions_ibfk_2` FOREIGN KEY (`fk_perm`) REFERENCES `t_permissions` (`id_perm`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

LOCK TABLES `t_roles_have_permissions` WRITE;
/*!40000 ALTER TABLE `t_roles_have_permissions` DISABLE KEYS */;

INSERT INTO `t_roles_have_permissions` (`id_role_has_perm`, `fk_role`, `fk_perm`)
VALUES
	(1,1,1),
	(2,1,2),
	(4,1,3),
	(5,1,4);

/*!40000 ALTER TABLE `t_roles_have_permissions` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_sections
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_sections`;

CREATE TABLE `t_sections` (
  `id_section` int(11) NOT NULL AUTO_INCREMENT,
  `title_section` varchar(64) NOT NULL,
  `description_section` text NOT NULL,
  PRIMARY KEY (`id_section`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

LOCK TABLES `t_sections` WRITE;
/*!40000 ALTER TABLE `t_sections` DISABLE KEYS */;

INSERT INTO `t_sections` (`id_section`, `title_section`, `description_section`)
VALUES
	(1,'Accueil','Chaleureuse accueil à vous'),
	(3,'Deuxième','');

/*!40000 ALTER TABLE `t_sections` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_threads
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_threads`;

CREATE TABLE `t_threads` (
  `id_thread` int(11) NOT NULL AUTO_INCREMENT,
  `title_thread` varchar(64) NOT NULL,
  `content_thread` text NOT NULL,
  `icon_thread` text NOT NULL,
  `pinned_thread` varchar(64) NOT NULL,
  `fk_cat` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_thread`),
  KEY `fk_cat` (`fk_cat`),
  CONSTRAINT `t_threads_ibfk_1` FOREIGN KEY (`fk_cat`) REFERENCES `t_categories` (`id_cat`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

LOCK TABLES `t_threads` WRITE;
/*!40000 ALTER TABLE `t_threads` DISABLE KEYS */;

INSERT INTO `t_threads` (`id_thread`, `title_thread`, `content_thread`, `icon_thread`, `pinned_thread`, `fk_cat`)
VALUES
<<<<<<< HEAD
	(1,'Ouverture du forum','Le forum est ouvert !','/img/threads/default.png','true',1),
	(2,'Super','Super','/img/threads/default.png','true',1),
	(3,'trop bien','yes','/img/threads/default.png','true',1);
=======
	(1,'Raphy est-il un con ?','Dites moi dans les réponses svp','https://cdn-icons-png.flaticon.com/512/16/16268.png',0,2),
	(2,'Raphy est un con !','Et oui, vous l\'avez bien lu. ANNONCES TRES IMPORTANTES','https://png.pngtree.com/element_our/20200702/ourlarge/pngtree-cartoon-exclamation-mark-icon-free-button-image_2291932.jpg',1,1);
>>>>>>> 5a0505c (BD changes)

/*!40000 ALTER TABLE `t_threads` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users`;

CREATE TABLE `t_users` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `nickname_user` varchar(64) NOT NULL,
  `password_user` text NOT NULL,
  `steam_user` text,
  `discord_user` varchar(37) DEFAULT NULL,
  `bio_user` text,
  `signature_user` text,
  `icon_user` text NOT NULL,
  `registration_date_user` date NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users` WRITE;
/*!40000 ALTER TABLE `t_users` DISABLE KEYS */;

INSERT INTO `t_users` (`id_user`, `nickname_user`, `password_user`, `steam_user`, `discord_user`, `bio_user`, `signature_user`, `icon_user`, `registration_date_user`)
VALUES
<<<<<<< HEAD
	(2,'Yphar','24352536','yphar_gamer','Yphar#3702','je m\'appelle yphar','yphar','https://yphar.dev/img/logo.png','2022-03-22'),
	(3,'Yphar','123456',NULL,NULL,NULL,NULL,'/img/users/default.png','2022-04-25'),
	(4,'Yphar','1234567',NULL,NULL,NULL,NULL,'/img/users/default.png','2022-04-25'),
	(5,'Yphar','asdpijfasdèofin',NULL,NULL,NULL,NULL,'/img/users/default3.png','2022-04-27'),
	(6,'Yphar','123456',NULL,NULL,NULL,NULL,'/img/users/default.png','2022-04-27');
=======
	(1,'Yphar','123456','https://steamcommunity.com/id/yphar_','Yphar#3702','Salut moi c\'est Yphar','Meilleures salutations,\r\nYphar','https://yphar.dev/img/logo.png','2022-06-11'),
	(2,'Azecko','grattelamoi','','','Bonjour, je m\'appelle Azecko','Bonne journée,\r\nAzecko','https://cdn.futura-sciences.com/buildsv6/images/wide1920/4/7/3/47343047c5_105832_ciel-bleu-01.jpg','2022-06-11');
>>>>>>> 5a0505c (BD changes)

/*!40000 ALTER TABLE `t_users` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_create_responses
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_create_responses`;

CREATE TABLE `t_users_create_responses` (
  `id_user_creates_resp` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_resp` int(11) NOT NULL,
  `add_date_user_creates_resp` datetime NOT NULL,
  PRIMARY KEY (`id_user_creates_resp`),
  KEY `fk_resp` (`fk_resp`),
  KEY `fk_user` (`fk_user`),
  CONSTRAINT `t_users_create_responses_ibfk_1` FOREIGN KEY (`fk_resp`) REFERENCES `t_responses` (`id_resp`),
  CONSTRAINT `t_users_create_responses_ibfk_2` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_create_responses` WRITE;
/*!40000 ALTER TABLE `t_users_create_responses` DISABLE KEYS */;

INSERT INTO `t_users_create_responses` (`id_user_creates_resp`, `fk_user`, `fk_resp`, `add_date_user_creates_resp`)
VALUES
	(1,2,2,'2022-03-22 00:00:00'),
	(2,2,3,'2022-03-22 00:00:00');

/*!40000 ALTER TABLE `t_users_create_responses` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_create_threads
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_create_threads`;

CREATE TABLE `t_users_create_threads` (
  `id_user_creates_thread` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_thread` int(11) NOT NULL,
  `add_date_user_creates_thread` datetime NOT NULL,
  PRIMARY KEY (`id_user_creates_thread`),
  KEY `fk_thread` (`fk_thread`),
  KEY `fk_user` (`fk_user`),
  CONSTRAINT `t_users_create_threads_ibfk_1` FOREIGN KEY (`fk_thread`) REFERENCES `t_threads` (`id_thread`),
  CONSTRAINT `t_users_create_threads_ibfk_2` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_create_threads` WRITE;
/*!40000 ALTER TABLE `t_users_create_threads` DISABLE KEYS */;

INSERT INTO `t_users_create_threads` (`id_user_creates_thread`, `fk_user`, `fk_thread`, `add_date_user_creates_thread`)
VALUES
	(2,2,2,'2022-03-22 00:00:00');

/*!40000 ALTER TABLE `t_users_create_threads` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_delete_responses
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_delete_responses`;

CREATE TABLE `t_users_delete_responses` (
  `id_user_deletes_resp` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_resp` int(11) NOT NULL,
  `delete_date_user_deletes_resp` datetime NOT NULL,
  PRIMARY KEY (`id_user_deletes_resp`),
  KEY `fk_resp` (`fk_resp`),
  KEY `fk_user` (`fk_user`),
  CONSTRAINT `t_users_delete_responses_ibfk_1` FOREIGN KEY (`fk_resp`) REFERENCES `t_responses` (`id_resp`),
  CONSTRAINT `t_users_delete_responses_ibfk_2` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_delete_responses` WRITE;
/*!40000 ALTER TABLE `t_users_delete_responses` DISABLE KEYS */;

INSERT INTO `t_users_delete_responses` (`id_user_deletes_resp`, `fk_user`, `fk_resp`, `delete_date_user_deletes_resp`)
VALUES
	(1,2,2,'2022-03-22 00:00:00');

/*!40000 ALTER TABLE `t_users_delete_responses` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_delete_threads
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_delete_threads`;

CREATE TABLE `t_users_delete_threads` (
  `id_user_deletes_thread` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_thread` int(11) NOT NULL,
  `delete_date_user_deletes_thread` datetime NOT NULL,
  PRIMARY KEY (`id_user_deletes_thread`),
  KEY `fk_thread` (`fk_thread`),
  KEY `fk_user` (`fk_user`),
  CONSTRAINT `t_users_delete_threads_ibfk_1` FOREIGN KEY (`fk_thread`) REFERENCES `t_threads` (`id_thread`),
  CONSTRAINT `t_users_delete_threads_ibfk_2` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_delete_threads` WRITE;
/*!40000 ALTER TABLE `t_users_delete_threads` DISABLE KEYS */;

INSERT INTO `t_users_delete_threads` (`id_user_deletes_thread`, `fk_user`, `fk_thread`, `delete_date_user_deletes_thread`)
VALUES
	(1,2,1,'2022-03-22 00:00:00');

/*!40000 ALTER TABLE `t_users_delete_threads` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_have_characters
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_have_characters`;

CREATE TABLE `t_users_have_characters` (
  `id_user_has_char` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_char` int(11) NOT NULL,
  `add_date_user_has_char` datetime NOT NULL,
  PRIMARY KEY (`id_user_has_char`),
  KEY `fk_char` (`fk_char`),
  KEY `fk_user` (`fk_user`),
  CONSTRAINT `t_users_have_characters_ibfk_1` FOREIGN KEY (`fk_char`) REFERENCES `t_characters` (`id_char`),
  CONSTRAINT `t_users_have_characters_ibfk_2` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_have_characters` WRITE;
/*!40000 ALTER TABLE `t_users_have_characters` DISABLE KEYS */;

INSERT INTO `t_users_have_characters` (`id_user_has_char`, `fk_user`, `fk_char`, `add_date_user_has_char`)
VALUES
	(10,2,6,'2022-05-23 00:00:00');

/*!40000 ALTER TABLE `t_users_have_characters` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_have_emails
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_have_emails`;

CREATE TABLE `t_users_have_emails` (
  `id_user_has_email` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_email` int(11) NOT NULL,
  `add_date_user_has_email` datetime NOT NULL,
  PRIMARY KEY (`id_user_has_email`),
  KEY `fk_user` (`fk_user`),
  KEY `fk_email` (`fk_email`),
  CONSTRAINT `t_users_have_emails_ibfk_1` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`),
  CONSTRAINT `t_users_have_emails_ibfk_2` FOREIGN KEY (`fk_email`) REFERENCES `t_emails` (`id_email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_have_emails` WRITE;
/*!40000 ALTER TABLE `t_users_have_emails` DISABLE KEYS */;

INSERT INTO `t_users_have_emails` (`id_user_has_email`, `fk_user`, `fk_email`, `add_date_user_has_email`)
VALUES
	(2,6,2,'2022-04-27 00:00:00'),
	(4,2,9,'2022-05-05 00:00:00');

/*!40000 ALTER TABLE `t_users_have_emails` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_have_roles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_have_roles`;

CREATE TABLE `t_users_have_roles` (
  `id_user_has_role` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_role` int(11) NOT NULL,
  `add_date_user_has_role` datetime NOT NULL,
  PRIMARY KEY (`id_user_has_role`),
  KEY `fk_role` (`fk_role`),
  KEY `fk_user` (`fk_user`),
  CONSTRAINT `t_users_have_roles_ibfk_1` FOREIGN KEY (`fk_role`) REFERENCES `t_roles` (`id_role`),
  CONSTRAINT `t_users_have_roles_ibfk_2` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_have_roles` WRITE;
/*!40000 ALTER TABLE `t_users_have_roles` DISABLE KEYS */;

INSERT INTO `t_users_have_roles` (`id_user_has_role`, `fk_user`, `fk_role`, `add_date_user_has_role`)
VALUES
	(3,2,1,'2022-04-29 00:00:00'),
	(19,6,1,'2022-05-13 00:00:00'),
	(23,6,3,'2022-05-13 00:00:00'),
	(30,2,3,'2022-05-19 00:00:00'),
	(31,2,2,'2022-05-19 00:00:00');

/*!40000 ALTER TABLE `t_users_have_roles` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_update_responses
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_update_responses`;

CREATE TABLE `t_users_update_responses` (
  `id_user_updates_resp` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_resp` int(11) NOT NULL,
  `update_date_user_updates_resp` datetime NOT NULL,
  PRIMARY KEY (`id_user_updates_resp`),
  KEY `fk_user` (`fk_user`),
  KEY `fk_resp` (`fk_resp`),
  CONSTRAINT `t_users_update_responses_ibfk_1` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`),
  CONSTRAINT `t_users_update_responses_ibfk_2` FOREIGN KEY (`fk_resp`) REFERENCES `t_responses` (`id_resp`)
<<<<<<< HEAD
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_update_responses` WRITE;
/*!40000 ALTER TABLE `t_users_update_responses` DISABLE KEYS */;

INSERT INTO `t_users_update_responses` (`id_user_updates_resp`, `fk_user`, `fk_resp`, `update_date_user_updates_resp`)
VALUES
	(1,2,2,'2022-03-22 00:00:00');

=======
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_update_responses` WRITE;
/*!40000 ALTER TABLE `t_users_update_responses` DISABLE KEYS */;

INSERT INTO `t_users_update_responses` (`id_user_updates_resp`, `fk_user`, `fk_resp`, `update_date_user_updates_resp`)
VALUES
	(1,1,1,'2022-06-12 00:00:00'),
	(2,1,1,'2022-06-12 00:00:00');

>>>>>>> 5a0505c (BD changes)
/*!40000 ALTER TABLE `t_users_update_responses` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table t_users_update_threads
# ------------------------------------------------------------

DROP TABLE IF EXISTS `t_users_update_threads`;

CREATE TABLE `t_users_update_threads` (
  `id_user_updates_thread` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user` int(11) NOT NULL,
  `fk_thread` int(11) NOT NULL,
  `update_date_user_updates_thread` datetime NOT NULL,
  PRIMARY KEY (`id_user_updates_thread`),
  KEY `fk_thread` (`fk_thread`),
  KEY `fk_user` (`fk_user`),
  CONSTRAINT `t_users_update_threads_ibfk_1` FOREIGN KEY (`fk_thread`) REFERENCES `t_threads` (`id_thread`),
  CONSTRAINT `t_users_update_threads_ibfk_2` FOREIGN KEY (`fk_user`) REFERENCES `t_users` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

LOCK TABLES `t_users_update_threads` WRITE;
/*!40000 ALTER TABLE `t_users_update_threads` DISABLE KEYS */;

INSERT INTO `t_users_update_threads` (`id_user_updates_thread`, `fk_user`, `fk_thread`, `update_date_user_updates_thread`)
VALUES
<<<<<<< HEAD
	(4,2,3,'2022-03-22 00:00:00');
=======
	(1,2,1,'2022-06-11 00:00:00'),
	(2,1,2,'2022-06-11 00:00:00'),
	(3,2,1,'2022-06-12 00:00:00'),
	(4,1,2,'2022-06-12 00:00:00');
>>>>>>> 5a0505c (BD changes)

/*!40000 ALTER TABLE `t_users_update_threads` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

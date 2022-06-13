-- Trouver toutes les infos dont on a besoin à partir d'une réponse (son ID)
SELECT title_section 'Section', title_cat 'Category', title_thread 'Thread', tu.nickname_user 'Thread\'s author',
	content_resp 'Response', 
	ru.nickname_user 'Response\'s author', CONCAT(last_name_char, ' ', first_name_char) as 'Response\'s author\'s characters', name_email 'Response\'s author\'s email', name_role 'Response\'s author\'s role', GROUP_CONCAT(name_perm) 'Role\'s permissions',
	title_thread 'Thread\'s update', content_resp 'Response\'s update',
	title_thread 'Thread\'s delete', 
	content_resp 'Response\'s
delete
'
FROM t_responses r
	INNER JOIN t_threads t ON r.fk_thread = id_thread
	INNER JOIN t_categories c ON t.fk_cat = id_cat
	INNER JOIN t_sections s ON c.fk_section = id_section
	INNER JOIN t_users_create_threads uct ON uct.fk_thread = id_thread
	INNER JOIN t_users tu ON uct.fk_user = tu.id_user
	INNER JOIN t_users_create_responses ucr ON ucr.fk_resp = id_resp
	INNER JOIN t_users ru ON ucr.fk_user = ru.id_user
	INNER JOIN t_users_have_characters uhc ON uhc.fk_user = ru.id_user
	INNER JOIN t_characters ch ON uhc.fk_char = id_char
	INNER JOIN t_users_have_emails uhe ON uhe.fk_user = ru.id_user
	INNER JOIN t_emails e ON uhe.fk_email = id_email
	INNER JOIN t_users_have_roles ucro ON ucro. fk_user = ru.id_user
	INNER JOIN t_roles ro ON ucro.fk_role = id_role
	INNER JOIN t_roles_have_permissions rhp ON rhp.fk_role = id_role
	INNER JOIN t_permissions p ON rhp.fk_perm = id_perm
	INNER JOIN t_users_update_threads uut ON uut.fk_thread = id_thread
	INNER JOIN t_users tuu ON uut.fk_user = tuu.id_user
	INNER JOIN t_users_update_responses uur ON uur.fk_resp = id_resp
	INNER JOIN t_users ruu ON uur.fk_user = ruu.id_user
	INNER JOIN t_users_delete_threads udt ON udt.fk_thread = id_thread
	INNER JOIN t_users tud ON udt.fk_user = tud.id_user
	INNER JOIN t_users_delete_responses udr ON udr.fk_resp = id_resp
	INNER JOIN t_users rud ON udr.fk_user = rud.id_user
WHERE id_resp = 2
GROUP BY title_cat, 
	title_thread, 
	tu.nickname_user, 
	content_resp, 
	ru.nickname_user,
	CONCAT(last_name_char, ' ', first_name_char),
	name_email, 
	name_role;

-- Trouver toutes les infos dont on a besoin à partir d'un thread (son ID)
SELECT title_section 'Section', title_cat 'Category', title_thread 'Thread', tu.nickname_user 'Thread\'s author',
	content_resp 'Response', 
	ru.nickname_user 'Response\'s author', CONCAT(last_name_char, ' ', first_name_char) as 'Response\'s author\'s characters', name_email 'Response\'s author\'s email', name_role 'Response\'s author\'s role', GROUP_CONCAT(name_perm) 'Role\'s permissions'
FROM t_responses r
	INNER JOIN t_threads t ON r.fk_thread = id_thread
	INNER JOIN t_categories c ON t.fk_cat = id_cat
	INNER JOIN t_sections s ON c.fk_section = id_section
	INNER JOIN t_users_create_threads uct ON uct.fk_thread = id_thread
	INNER JOIN t_users tu ON uct.fk_user = tu.id_user
	INNER JOIN t_users_create_responses ucr ON ucr.fk_resp = id_resp
	INNER JOIN t_users ru ON ucr.fk_user = ru.id_user
	INNER JOIN t_users_have_characters uhc ON uhc.fk_user = ru.id_user
	INNER JOIN t_characters ch ON uhc.fk_char = id_char
	INNER JOIN t_users_have_emails uhe ON uhe.fk_user = ru.id_user
	INNER JOIN t_emails e ON uhe.fk_email = id_email
	INNER JOIN t_users_have_roles ucro ON ucro.fk_user = ru.id_user
	INNER JOIN t_roles ro ON ucro.fk_role = id_role
	INNER JOIN t_roles_have_permissions rhp ON rhp.fk_role = id_role
	INNER JOIN t_permissions p ON rhp.fk_perm = id_perm
WHERE r.fk_thread = 1
GROUP BY title_cat, 
	title_thread, 
	tu.nickname_user, 
	content_resp, 
	ru.nickname_user,
	CONCAT(last_name_char, ' ', first_name_char),
	name_email, 
	name_role;

-- Trouver toutes les infos dont on a besoin à partir d'une catégorie (son ID)
SELECT title_section 'Section', title_cat 'Category', title_thread 'Thread', tu.nickname_user 'Thread\'s author'
FROM t_threads t
	INNER JOIN t_categories c ON t.fk_cat = id_cat
	INNER JOIN t_sections s ON c.fk_section = id_section
	INNER JOIN t_users_create_threads uct ON uct.fk_thread = id_thread
	INNER JOIN t_users tu ON uct.fk_user = tu.id_user
WHERE t.fk_cat = 1
GROUP BY title_cat, 
	title_thread, 
	tu.nickname_user;
	
-- Trouver toutes les infos dont on a besoin à partir d'une section (son ID)
SELECT title_section 'Section', title_cat 'Category'
FROM t_categories c
         INNER JOIN t_sections s ON c.fk_section = id_section
WHERE c.fk_section = 1
GROUP BY title_cat;
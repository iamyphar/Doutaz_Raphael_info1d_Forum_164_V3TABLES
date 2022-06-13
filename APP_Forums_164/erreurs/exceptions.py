"""
    File : exceptions.py
    Author : Raphaël Doutaz 09.05.22
"""
import sys

from flask import flash, render_template
from pymysql import IntegrityError

from APP_Forums_164 import app


class Base(Exception):
    def __init__(self, message):
        self.message = message


class ErreurFileSqlDump(Exception):
    pass


class ErreurFileEnvironnement(Exception):
    pass


class ExceptionInitApp(Exception):
    pass


class ErreurConnectionBD(Exception):
    pass


class ErreurExtractNameBD(Exception):
    pass


class MaBdErreurDoublon(IntegrityError):
    pass


class MonErreur(Exception):
    pass


class MaBdErreurConnexion(Exception):
    pass


class DatabaseException(Base):
    pass


class SqlException(DatabaseException):
    pass


class SqlSyntaxError(SqlException):
    pass


class DatabaseException(Base):
    pass


class ExceptionRolesDisplay(Base):
    pass


class ExceptionRoleDelete(Base):
    pass


class ExceptionRoleUpdate(Base):
    pass


class ExceptionUserAdd(Base):
    pass


class ExceptionCharsDisplay(Base):
    pass


class ExceptionCharUpdate(Base):
    pass


class ExceptionCharDelete(Base):
    pass


class ExceptionCharAdd(Base):
    pass


class ExceptionSectionsDisplay(Base):
    pass


class ExceptionSectionUpdate(Base):
    pass


class ExceptionSectionDelete(Base):
    pass


class ExceptionSectionAdd(Base):
    pass


class ExceptionCategoriesDisplay(Base):
    pass


class ExceptionCategoryUpdate(Base):
    pass


class ExceptionCategoryDelete(Base):
    pass


class ExceptionCategoryAdd(Base):
    pass

class ExceptionPermsDisplay(Base):
    pass


class ExceptionPermUpdate(Base):
    pass


class ExceptionPermDelete(Base):
    pass


class ExceptionPermAdd(Base):
    pass


class ExceptionUserDelete(Base):
    pass


class ExceptionUserUpdate(Base):
    pass


class ExceptionThreadAdd(Base):
    pass


class ExceptionThreadDelete(Base):
    pass


class ExceptionThreadUpdate(Base):
    pass


class ExceptionRoleAdd(Base):
    pass


class ExceptionUpdateThreadUserSelected(Base):
    pass


class ExceptionThreadsDisplay(Base):
    pass


class ExceptionUpdateUsersHaveThreadsSelected(Base):
    pass


class ExceptionUsersHaveThreadsDisplay(Base):
    pass


class ExceptionUpdateUsersHaveThreadsSelected(Base):
    pass


class ExceptionUpdateUsersHaveThreadsSelected(Base):
    pass

class ExceptionRolesUsersDisplayData(Base):
    pass

class ExceptionUpdatePermRoleSelected(Base):
    pass


class ExceptionPermsRolesDisplayData(Base):
    pass

class ExceptionRolesHavePermsDisplay(Base):
    pass


class ExceptionRolesPermsDisplayData(Base):
    pass

class ExceptionInitAppUsers164(Base):
    pass


class ExceptionUpdateRoleUserSelected(Base):
    pass


class ExceptionUpdateRoleUserSelected(Base):
    pass


class ExceptionUsersHaveCharsDisplay(Base):
    pass


class ExceptionUpdateCharUserSelected(Base):
    pass


class ExceptionUpdateCharUserSelected(Base):
    pass


class ExceptionCharsUsersDisplayData(Base):
    pass


@app.errorhandler(Exception)
def exception_handler(error):
    flash(f"Erreur : {error} {error.args[0]} {sys.exc_info()[0]}", "danger")
    a, b, c = sys.exc_info()
    flash(f"Erreur générale : {a} {b} {c}", "danger")

    return render_template("home.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

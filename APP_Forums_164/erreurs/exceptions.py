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


class ExceptionPass(Base):
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

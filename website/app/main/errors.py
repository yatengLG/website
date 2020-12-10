# -*- coding: utf-8 -*-
# @Author  : LG

from . import main_blueprint
from flask import render_template


@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('main/error.html', error_code=e), 404


@main_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return render_template('main/error.html', error_code=e), 500


@main_blueprint.app_errorhandler(502)
def internal_server_error(e):
    return render_template('main/error.html', error_code=e), 502

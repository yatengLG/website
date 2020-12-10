# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Blueprint

article_blueprint = Blueprint("article", __name__)

from . import views
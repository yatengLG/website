# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Blueprint

laboratory_blueprint = Blueprint("laboratory", __name__)

from .translate import views
from .index import views

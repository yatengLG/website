# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Blueprint

user_blueprint = Blueprint('user', __name__)

from . import forms, views


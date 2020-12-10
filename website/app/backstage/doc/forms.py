# -*- coding: utf-8 -*-
# @Author  : LG


from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class DocForm(FlaskForm):
    body = TextAreaField('内容', id = 'full-featured')
    submit = SubmitField('提交')

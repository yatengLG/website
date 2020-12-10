# -*- coding: utf-8 -*-
# @Author  : LG


from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField


class Experimentform(FlaskForm):
    title = TextField('标题', render_kw={'placeholder' : '标题',}, default=None)
    coverpic = TextField('封面图片链接', render_kw={'placeholder' : '封面图片链接'}, default=None)
    link = TextField('链接', render_kw={'placeholder' : '链接地址'}, default=None)
    forbid = SelectField('禁用', choices=[
        (1, '是'),
        (0, '否')
    ],default=0, render_kw={'style':'width: 200px'}, coerce=int)  # 这里传入的是int型， 但是后端接收是bool型。
    submit = SubmitField('提交')
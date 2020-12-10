# -*- coding: utf-8 -*-
# @Author  : LG


from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField


class Recommendationform(FlaskForm):
    article_id =TextField('文章id', render_kw={'placeholder' : '推荐文章id','style':'width: 383px'}, default=None)
    coverpic = TextField('封面图片链接', render_kw={'placeholder' : '封面图片链接','style':'width: 383px'}, default=None)
    link = TextField('链接', render_kw={'placeholder' : '链接地址','style':'width: 383px'}, default=None)
    forbid = SelectField('禁用', choices=[
        (1, '是'),
        (0, '否')
    ],default=0, render_kw={'style':'width: 200px'}, coerce=int)  # 这里传入的是int型， 但是后端接收是bool型。
    submit = SubmitField('提交')

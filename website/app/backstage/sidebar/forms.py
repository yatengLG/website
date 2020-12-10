# -*- coding: utf-8 -*-
# @Author  : LG


from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required, Length


class SidebarEditForm(FlaskForm):
    title =TextField('侧栏头', validators=[Required(message='标题为空'), Length(1, 40, message='1-40个字符')], render_kw={'placeholder' : '侧栏头','style':'width: 383px'})
    body = TextAreaField('内容(可编辑html源码的方式添加样式)', id = 'full-featured', render_kw={'style':'width: 383px'})
    forbid = SelectField('禁用', choices=[
        (1, '是'),
        (0, '否')
    ],default=0, render_kw={'style':'width: 200px'}, coerce=int)  # 这里传入的是int型， 但是后端接收是bool型。
    submit = SubmitField('提交')
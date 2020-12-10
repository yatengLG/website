# -*- coding: utf-8 -*-
# @Author  : LG


from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, SelectField
from wtforms.validators import Required


class CarouselEditform(FlaskForm):
    article_id =TextField('文章id', validators=[Required(message='文章id为空')], render_kw={'placeholder' : '轮播文章对应id','style':'width: 383px'})
    forbid = SelectField('禁用', choices=[
        (1, '是'),
        (0, '否')
    ],default=0, render_kw={'style':'width: 200px'}, coerce=int)  # 这里传入的是int型， 但是后端接收是bool型。
    submit = SubmitField('提交')
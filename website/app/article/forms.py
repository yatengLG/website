# -*- coding: utf-8 -*-
# @Author  : LG

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.fields import SubmitField, TextField, TextAreaField, SelectField, FileField, SelectMultipleField
from wtforms.validators import Required, Length
from wtforms import widgets, ValidationError
from ..models import Article

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()

class BuildForm(FlaskForm):
    title =TextField('标题', validators=[Required(message='标题为空'), Length(1, 40, message='1-40个字符')], render_kw={'placeholder' : '请输入文章标题'})
    coverpic = FileField('上传封面展示图(必须上传)', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], message='只允许上传图片，支持jpg、jpeg、png')])
    body = TextAreaField('内容', id = 'full-featured')
    original = SelectField('文章来源', choices=[
        ('原创', '原创'),
        ('转载', '转载'),
        ('翻译', '翻译')
    ], render_kw={'style':'width: 200px'}, default = '原创')
    classes = SelectField('文章类别', choices=[
        ('python基础', 'python基础'),
        ('Web开发', 'Web开发'),
        ('爬虫', '爬虫'),
        ('数据分析', '数据分析'),
        ('机器学习', '机器学习'),
        ('其他', '其他')
    ], render_kw={'style': 'width: 200px'}, default='python基础')
    # domain_ports = MultiCheckboxField('domain_ports', choices=[
    #     ('python基础', 'python基础'),
    #     ('pythonWeb', 'pythonWeb'),
    #     ('爬虫', '爬虫'),
    #     ('数据分析', '数据分析'),
    #     ('机器学习', '机器学习')
    # ], render_kw={'class': 'form-check-inline'})
    public = SelectField('发布形式', choices=[
        (1, '公开'),
        (0, '私有')
    ], render_kw={'style':'width: 200px'}, coerce=int)  # 这里传入的是int型， 但是后端接收是bool型。
    submit = SubmitField('提交')


class EditForm(FlaskForm):
    title =TextField('标题', validators=[Required(message='标题为空'), Length(1, 40, message='1-40个字符')], render_kw={'placeholder' : '请输入文章标题'})
    coverpic = FileField('修改封面展示图(不上传则使用原先的封面图)', validators=[FileAllowed(['jpg', 'jpeg', 'png'], message='只允许上传图片，支持jpg、jpeg、png')])
    body = TextAreaField('内容', id = 'full-featured')
    original = SelectField('文章来源', choices=[
        ('原创', '原创'),
        ('转载', '转载'),
        ('翻译', '翻译')
    ], render_kw={'style':'width: 200px'}, default = '原创')
    classes = SelectField('文章类别', choices=[
        ('python基础', 'python基础'),
        ('Web开发', 'Web开发'),
        ('爬虫', '爬虫'),
        ('数据分析', '数据分析'),
        ('机器学习', '机器学习'),
        ('其他', '其他')
    ], render_kw={'style': 'width: 200px'}, default='python基础')
    # domain_ports = MultiCheckboxField('domain_ports', choices=[
    #     ('python基础', 'python基础'),
    #     ('pythonWeb', 'pythonWeb'),
    #     ('爬虫', '爬虫'),
    #     ('数据分析', '数据分析'),
    #     ('机器学习', '机器学习')
    # ], render_kw={'class': 'form-check-inline'})
    public = SelectField('发布形式', choices=[
        (1, '公开'),
        (0, '私有')
    ], render_kw={'style':'width: 200px'}, coerce=int)  # 这里传入的是int型， 但是后端接收是bool型。
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = TextAreaField('',validators=[Required(), Length(1, 200, message='评论每条最多200字')], render_kw={'placeholder' : '欢迎写下您的评论，每条最多200字.'})
    submit = SubmitField('提交')

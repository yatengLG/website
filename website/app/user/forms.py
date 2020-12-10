# -*- coding: utf-8 -*-
# @Author  : LG

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User


# 登录表单
class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email(message='不是有效的邮箱地址')])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


# 注册表单
class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(3, 64), Email(message='不是有效的邮箱地址')], render_kw={'placeholder' : '请填写正确的邮箱'})
    username = StringField('用户名', validators=[Required(message='用户名不能为空'), Length(1, 16, message='最长为14个英文或7个汉字'),
                                                   Regexp("^[a-zA-Z0-9\u4e00-\u9fa5]+$", 0, '用户名必须由数字，字母以及中文组成.')], render_kw={'placeholder' : '支持中文，字母，数字'})
    password = PasswordField('密码', validators=[Required(message='密码不能为空'), Length(6, 20, message='密码长度应在6~20之间')], render_kw={'placeholder' : '密码长度6~20个字符'})
    password2 = PasswordField('确认密码', validators=[Required(message='确认密码不能为空'), EqualTo('password', message='输入的密码不一致.')], render_kw={'placeholder' : '请再次输入密码'})
    submit = SubmitField('注册')

    # 表单类中定义了以validate_ 开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用.
    # 本例分别为 email 和 username 字段定义了验证函数，确保填写的值在数据库中没出现过
    # 自定义的验证函数要想表示验证失败，可以抛出 ValidationError 异常，其参数就是错误消息
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册过了')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')


# 忘记密码表单
class ForgetPasswordForm(FlaskForm):
    email = StringField('请输入注册邮箱',validators=[Required()], render_kw={'placeholder' : '请填写正确的邮箱'})
    submit = SubmitField('提交')


# 重置密码表单
class ResetPasswordForm(FlaskForm):
    password = PasswordField('新密码', validators=[Required(message='密码不能为空'), Length(6, 20, message='密码长度应在6~20之间')],
                             render_kw={'placeholder': '密码长度6~20个字符'})
    password2 = PasswordField('确认密码',
                              validators=[Required(message='确认密码不能为空'), EqualTo('password', message='输入的密码不一致.')],
                              render_kw={'placeholder': '请再次输入密码'})
    submit = SubmitField('提交')
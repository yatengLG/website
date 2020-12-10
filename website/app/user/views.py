# -*- coding: utf-8 -*-
# @Author  : LG

from . import user_blueprint
from .forms import RegistrationForm, LoginForm, ResetPasswordForm, ForgetPasswordForm
from ..models import User, Article, Comment
from .. import db
from flask import flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from ..email import send_email
from datetime import datetime
from sqlalchemy import and_, or_

# 登录路由
@user_blueprint.route('/user/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('无效的账户或密码.')
    return render_template('user/login.html', form=form)


# 登出路由
@user_blueprint.route('/user/logout')
@login_required
def logout():
    logout_user()
    flash('账号已经登出.')
    return redirect(url_for('main.index'))


# 注册路由
@user_blueprint.route('/user/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit() # 这里先提交，因为后续验证需要用到id
        token = user.generate_confirmation_token()
        send_email(user.email, '账号注册验证',
                   'user/email/confirm', user=user, token=token)

        flash('一封认证邮件已经发送到您的邮箱,请注意查收.')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user_blueprint.route('/user/forgetpassword', methods = ['GET', 'POST'])
def forget_password():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_confirmation_token()
            send_email(form.email.data, '密码重置验证',
                       'user/email/resetpassword', user=user, token=token)
            flash('一封验证邮件已发送到您的邮箱，请注意查收。')
        else:
            flash('输入的注册邮箱不存在')
        return redirect(url_for('main.index'))
    return render_template('user/forgetpassword.html', form=form)


@user_blueprint.route('/user/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    dumps_dic = User.analysis_confirmation_token(token)
    user = User.query.filter_by(email=dumps_dic['email']).first()
    if user.id == dumps_dic['id']:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.password = form.password.data
            db.session.commit()
            logout_user()
            flash('账号密码已重置，请用新密码登录.')
            return redirect(url_for('user.login'))
        return render_template('user/resetpassword.html', form=form)
    else:
        flash('验证链接无效或已过期')
        return redirect(url_for('main.index'))


# 注销账号
@user_blueprint.route('/user/remove')
@login_required
def remove():
    user_id = current_user.id
    user = User.query.get(user_id)
    token = user.generate_confirmation_token()
    send_email(user.email, "账号注销验证",
               'user/email/remove', user=user, token=token)
    flash('一封验证邮件已经发送到您的邮箱，请注意查收.')
    return redirect(request.referrer or url_for('main.index'))


@user_blueprint.route('/user/remove/<token>')
@login_required
def remove_confirm(token):
    if current_user.confirm(token):
        user_id = current_user.id
        logout_user()
        print('验证成功')
        user = User.query.get(user_id)
        db.session.query(Article).filter(Article.author==user_id).delete()  # 删除文章
        db.session.query(Comment).filter(Comment.author_id == user_id).delete()  # 删除评论
        db.session.delete(user)         # 删除用户
        db.session.commit()
        flash('您的账号已经注销，发布的文章及评论等均已删除.')
    else:
        flash('确认链接无效或已过期.')
    return redirect(url_for('main.index'))


@user_blueprint.route('/user/confirm/<token>')
@login_required # 保护路由，如果未登录用户访问这个页面，flask-login会拦截用户并发往登录页面
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        # 验证通过，将用户验证标签置为True
        current_user.confirmed = True
        current_user.register_time = db.Column(db.DateTime, default=datetime.utcnow())  # 注册时间以邮箱验证时间为准.
        db.session.add(current_user)
        flash('您的账号已通过认证！')
    else:
        flash('确认链接无效或已过期。您可以直接登录，系统会自动发送一封新的认证邮件到您的邮箱！')
    return redirect(url_for('main.index'))


@user_blueprint.route('/user/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '账号注册验证',
               'user/email/confirm', user=current_user, token=token)
    flash('您的注册邮箱还未进行验证，一封新的验证邮件已发送到您的邮箱，请注意查收.')
    return redirect(request.referrer or url_for('main.index'))


# 用户主页
@user_blueprint.route('/user/home/<int:user_id>')
@login_required
def home(user_id):
    user = User.query.filter(User.id==user_id).first()
    if current_user == user:
        articles = Article.query.filter(Article.user == user).order_by(Article.timestamp.desc()).all()
        comments = Comment.query.filter(Comment.user == user).order_by(Comment.timestamp.desc()).all()
    else:
        articles = Article.query.filter(and_(Article.user == user, Article.forbid ==False, Article.public==True,Article.reviewed==True)).order_by(Article.timestamp.desc()).all()
        comments = Comment.query.filter(and_(Comment.user == user, Comment.forbid==False, Comment.reviewed==True)).order_by(Comment.timestamp.desc()).all()
    return render_template('user/home.html', current_user=current_user, user=user, articles=articles, comments=comments)

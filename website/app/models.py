# -*- coding: utf-8 -*-
# @Author  : LG

from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import loginmanager


# 文章数据库
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)                  # 标题
    coverpic = db.Column(db.Text)               # 封面图名
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))   # 作者id
    body = db.Column(db.Text)                   # 内容
    original = db.Column(db.Text)            # 0 原创， 1 转载， 2 翻译
    classes = db.Column(db.Text)            # 文章分类
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())   # 发表时间
    updatetimestamp = db.Column(db.DateTime)    # 文章最近一次更新时间
    clicks = db.Column(db.Integer, default=0)   # 文章点击数.
    # 权限设置
    public = db.Column(db.Boolean, default=True)    # 文章公开，默认为 公开
    forbid = db.Column(db.Boolean, default=False)   # 禁用，默认为不禁用
    reviewed = db.Column(db.Boolean, default=False)  # 审核，默认不通过审核， 审核后才会展示
    # 评论
    comments = db.relationship('Comment', backref='article', cascade='all, delete')
    carousel = db.relationship('Carousel', backref='article', uselist=False)    # 一对一，指向轮播
    recommendation = db.relationship('Recommendation', backref='article', uselist=False)    # 一对一指向推荐


# 文章相关记录,只记录登录的用户
class Content_record(db.Model):
    __tablename__ = 'content_records'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, default=None)            # 文章id
    comment_id = db.Column(db.Integer, default=None)            # 评论id
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 用户
    timestamp = db.Column(db.DateTime)              # 时间
    type = db.Column(db.String)                     # 操作


# 管理相关记录
class Manage_record(db.Model):
    __tablename__ = 'manage_records'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, default=None)
    comment_id = db.Column(db.Integer, default=None)
    user_id = db.Column(db.Integer, default=None)
    site_ops = db.Column(db.Text, default=None)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 管理员id
    timestamp = db.Column(db.DateTime)
    type = db.Column(db.String)
    result = db.Column(db.Text)


# 评论
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body = db.Column(db.Text)

    forbid = db.Column(db.Boolean, default=False)  # 禁用，默认为不禁用
    reviewed = db.Column(db.Boolean, default=False) # 审核
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)   # 评论时间


# 用户
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)    # 不允许重复
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)    # 邮箱验证
    forbid = db.Column(db.Boolean, default=False)   # 禁用，默认为不禁用
    level= db.Column(db.Integer, default=1) # 级别

    comments = db.relationship('Comment', backref='user', cascade='all')    # 评论
    articles = db.relationship('Article', backref='user')               # 文章

    manage_records = db.relationship('Manage_record', backref='user')   # 管理记录
    content_records = db.relationship('Content_record', backref='user') # 内容记录

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成一个令牌，有效期默认为五分钟
    def generate_confirmation_token(self, expiration=300, dumps_dic=None):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        if dumps_dic is None:
            dumps_dic={'email':self.email, 'id':self.id}
        return s.dumps(dumps_dic)

    # 解析token
    def analysis_confirmation_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            return data
        except:
            return False

    # 检验令牌，如果检验通过，则把新添加的 confirmed 属性设为 True
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('id') == self.id and data.get('email') == self.email:  # 检查id与存储在current_user中的已登录用户匹配
            return True
        return False


# 侧栏，这里将侧栏管理写入数据库，从后台进行侧栏修改
class Side_Bar(db.Model):
    __tablename__ = 'sidebars'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)                      # 侧栏头
    body = db.Column(db.Text)                       # 内容
    forbid = db.Column(db.Boolean, default=False)   # 禁用，默认为不禁用


# 轮播
class Carousel(db.Model):
    __tablename__ = 'carousels'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    forbid = db.Column(db.Boolean, default=False)   # 禁用，默认为不禁用


# 推荐
class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    # 如果是站内文章，则直接给文章id即可
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), default=None)
    # 如果是站外文章，需要给封面图片以及链接
    coverpic = db.Column(db.Text, default=None)               # 封面图名
    link = db.Column(db.Text, default=None)
    forbid = db.Column(db.Boolean, default=False)   # 禁用，默认为不禁用


# 实验
class Experiment(db.Model):
    __tablename__ = 'experiments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    coverpic = db.Column(db.Text)
    link = db.Column(db.Text, default=None)
    forbid = db.Column(db.Boolean, default=False)   # 禁用，默认为不禁用


# 加载用户的回调函数
@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

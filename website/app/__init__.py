# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_login import LoginManager
from flask_apscheduler import APScheduler

# bootstrap
bootstrap = Bootstrap()
# 数据库
db = SQLAlchemy()
# 日期管理
moment = Moment()
# 发送邮件
mail = Mail()
# 定时应用
scheduler = APScheduler()
# 用户登录管理
loginmanager = LoginManager()
loginmanager.session_protection = 'strong'  # 安全等级，strong时，会记录客户端ip地址和浏览器的用户代理信息，如有异动则登出用户
loginmanager.login_view = 'user.login'      # 登录页面的端点
loginmanager.login_message = '您好，请先登录'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    loginmanager.init_app(app)
    scheduler.init_app(app)

    scheduler.start()
    # 注册蓝图
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .article import article_blueprint
    app.register_blueprint(article_blueprint)

    from .user import user_blueprint
    app.register_blueprint(user_blueprint)

    from .backstage import backstage_blueprint
    app.register_blueprint(backstage_blueprint)

    from .laboratory import laboratory_blueprint
    app.register_blueprint(laboratory_blueprint)

    return app


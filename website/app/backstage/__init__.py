# -*- coding: utf-8 -*-
# @Author  : LG

from flask import Blueprint

backstage_blueprint = Blueprint('backstage', __name__)

from .main import views
from .article import views          # 文章
from .sidebar import views          # 侧栏
from .carousel import views         # 轮播
from .comment import views          # 评论
from .user import views             # 用户
from .experiment import views       # 实验
from .recommendation import views   # 推荐
from .record import views           # 日志
from .doc import views
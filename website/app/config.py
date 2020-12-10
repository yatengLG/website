# -*- coding: utf-8 -*-
# @Author  : LG

import os

DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))
# MAX_CONTENT_LENGTH = 3*1024*1024	# 上传文件大小限制
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hardstrings'  # 自己改个屌一点复杂一点的key，最好弄成环境变量
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# 数据库
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

# # 其他数据库
# SQLALCHEMY_BINDS = {
#     'laboratory': 'sqlite:///' + os.path.join(basedir, 'laboratory.sqlite')
# }


# 发送邮件服务器，用于给用户发送邮件，或者用户注册认证等，是自动邮箱
MAIL_SERVER = 'smtp.qq.com' # 这些根据你的自动邮箱更改

MAIL_PORT = 465      # 这些根据你的自动邮箱更改
MAIL_USE_SSL = True #  # 这些根据你的自动邮箱更改
# 邮箱
MAIL_USERNAME = '自动邮箱名'#os.environ.get('MAIL_USERNAME')     # 这个邮箱最好啥也别干了，重新申请一个最好了
MAIL_DEFAULT_SENDER = '自动邮箱地址'
# 授权码
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '你邮箱SMTP授权码'

FLASKY_MAIL_SUBJECT_PREFIX = '' # 这个是邮件发送人的 前部修饰部分

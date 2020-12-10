# -*- coding: utf-8 -*-
# @Author  : LG

from . import article_blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify
from .forms import EditForm, BuildForm, CommentForm
from flask_login import login_required, current_user
from ..models import Article, Comment, Content_record
from .. import db
from datetime import datetime
import os
from PIL import Image
from ..utils.upload import upload_file_qiniu, random_filename
import io

@article_blueprint.route('/article/build', methods=["GET", "POST"])
@login_required
def build():
    if current_user.forbid: # 如果用户被禁用，则无法发布文章
        return render_template('article/error.html', message='该账号已被禁用，请联系管理员了解详情.')
    if not current_user.confirmed:
        flash('验证注册邮箱后，才可以发布文章.')
        return redirect(url_for('user.home', user_id=current_user.id))
    form = BuildForm()
    if form.validate_on_submit():
        f = form.coverpic.data
        image = Image.open(f)
        image.thumbnail((1080, 960))

        filename = random_filename(f.filename)
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format=image.format)
        imgByteArr = imgByteArr.getvalue()
        try:
            upload_file_qiniu(data=imgByteArr, rename=filename)
        except Exception as e:
            return jsonify(errmsg='上传失败')

        article = Article(title=form.title.data,
                          coverpic = filename,
                          author_id=current_user.id,
                          original=form.original.data,
                          classes=form.classes.data,
                          body=form.body.data,
                          public=form.public.data
                          )

        db.session.add(article)
        db.session.commit() # 这里先进行提交，因为下面文章记录需要用到文章id
        record = Content_record(article_id=article.id,
                                admin_id=current_user.id,
                                timestamp=datetime.utcnow(),
                                type='创建')
        db.session.add(record)

        flash('文章已提交，待审核后显示，您可在个人中心提前查看.')
        return redirect(url_for('user.home', user_id=current_user.id))
    return render_template('article/build.html', form = form)


@article_blueprint.route('/article/edit/<article_id>', methods=["GET", "POST"])
@login_required
def edit(article_id):
    article = Article.query.get(article_id)
    if article is not None:
        if article.user == current_user:
            form = EditForm()
            if form.validate_on_submit():
                f = form.coverpic.data
                if f.filename != '' or article.title != form.title.data or article.body != form.body.data:
                    article.updatetimestamp = datetime.utcnow()
                    article.reviewed = False    # 封面图片、标题、内容 更改，需重新审核。
                    record = Content_record(article_id=article.id,
                                            timestamp=datetime.utcnow(),
                                            admin_id=current_user.id,
                                            type='编辑')
                    db.session.add(record)
                    flash('文章已修改，待审核。')
                if f.filename != '':
                    image = Image.open(f)
                    image.thumbnail((1080, 960))
                    filename = random_filename(f.filename)
                    imgByteArr = io.BytesIO()
                    image.save(imgByteArr, format=image.format)
                    imgByteArr = imgByteArr.getvalue()
                    try:
                        upload_file_qiniu(data=imgByteArr, rename=filename)
                    except Exception as e:
                        return jsonify(errmsg='上传失败')
                    article.coverpic = filename

                article.title = form.title.data
                article.body = form.body.data
                article.original = form.original.data
                article.public = form.public.data

                return redirect(url_for('article.article_show', article_id=article_id))

            form.title.data = article.title
            form.body.data = article.body
            form.original.data = str(article.original)
            form.public.data = article.public
            return render_template('article/edit.html', form=form)

        flash('您不是本文作者，无权进行编辑。')
        return redirect(url_for('article.article_show', article_id=article_id))
    flash('文章不存在。')
    return redirect(url_for('main.index'))


@article_blueprint.route('/article/delete/<article_id>', methods=["GET", "POST"])
@login_required
def delete(article_id):
    article = Article.query.get(article_id)
    if article is not None:
        if article.user == current_user:
            record = Content_record(article_id=article.id,
                                    timestamp=datetime.utcnow(),
                                    admin_id=current_user.id,
                                    type='删除')
            db.session.add(record)
            db.session.delete(article)
            flash('文章已删除。')
            return redirect(url_for('user.home',user_id=current_user.id))
        flash('您不是本文作者，无权进行删除。')
        return redirect(url_for('article.article_show', article_id=article_id))
    flash('文章不存在。')
    return redirect(url_for('main.index'))


@article_blueprint.route('/article/show/<article_id>', methods=["GET", "POST"])
def article_show(article_id):
    form = CommentForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('请先登录后再评论。')
            return redirect(url_for('article.article_show', article_id=article_id))
        if current_user.forbid: # 如果用户被禁用，则无法评论
            flash('您的账号已被限制，无法评论。')
            return redirect(url_for('article.article_show', article_id=article_id))
        if not current_user.confirmed:  # 用户账号必须先进行邮箱验证
            flash('验证邮箱后，才可以发布评论.请先前往个人中心进行邮箱验证.')
            return redirect(url_for('article.article_show', article_id=article_id))
        comment = form.body.data
        comment = Comment(body=comment, author_id=current_user.id, article_id=article_id, timestamp=datetime.utcnow())
        db.session.add(comment)
        db.session.commit()

        record = Content_record(comment_id=comment.id,
                                admin_id=current_user.id,
                                timestamp=datetime.utcnow(),
                                type='创建')
        db.session.add(record)

        flash('评论已提交,待审核后显示.')
        return redirect(url_for('article.article_show', article_id=article_id))
    article_id = int(article_id)
    article = Article.query.filter(Article.id==article_id).first()

    if article:
        comments = article.comments     # 加载文章评论
        comments = [comment for comment in comments if comment.reviewed and (not comment.forbid)]
        comments.reverse()  # 这里倒下序
        forbid = article.forbid         # 禁止
        reviewed = article.reviewed
        public = article.public

        if current_user.is_authenticated:   # 如果已登录
            if current_user==article.user: # 是作者，则直接跳转
                return render_template('/article/show.html', article=article, comments=comments, form=form)

            if current_user.level >= 2 and public:  # 是管理员，且文章公开，则跳转
                return render_template('/article/show.html', article=article, comments=comments, form=form)

        # 文章不公开，则提示
        if not public:
            flash('文章不存在。')
            return redirect(url_for('main.index'))

        # 禁用，则提示
        if forbid:
            flash('文章不存在。')
            return redirect(url_for('main.index'))

        # 是否通过审核
        if not reviewed:
            flash('文章不存在。')
            return redirect(url_for('main.index'))

        article.clicks += 1

        return render_template('/article/show.html', article=article, comments=comments, form=form)

    flash('文章不存在。')
    return redirect(url_for('main.index'))


@article_blueprint.route('/comment/delete/<comment_id>', methods=["GET"])
@login_required
def comment_delete(comment_id):
    comment = Comment.query.get(comment_id)
    if comment is not None:
        if comment.user == current_user:
            record = Content_record(comment_id=comment.id,
                                    admin_id=current_user.id,
                                    timestamp=datetime.utcnow(),
                                    type='删除')
            db.session.add(record)
            db.session.delete(comment)
            flash('评论已删除。')
        else:
            flash('您不是评论作者，无权进行删除。')
    else:
        flash('评论不存在。')
    return redirect(request.referrer or url_for('main.index'))
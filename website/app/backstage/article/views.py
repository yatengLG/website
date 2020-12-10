# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import Article, db, Manage_record
from datetime import datetime

# 文章管理页面
@backstage_blueprint.route('/backstage/article', defaults={'page': 1})
@backstage_blueprint.route('/backstage/article/page/<int:page>', methods=["GET", "POST"])
@login_required
def article_manage(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 2:
        per_page = 15                                    # 每页返回的数量
        pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        articles = pagination.items     # 返回查询到的数据
        return render_template('backstage/article/index.html', current_user=current_user, articles=articles, pagination=pagination)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 文章审核页面
@backstage_blueprint.route('/backstage/article/reviewed', defaults={'page': 1})
@backstage_blueprint.route('/backstage/article/reviewed/page/<int:page>', methods=["GET", "POST"])
@login_required
def article_reviewed(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level>=2:                       # 2级以上 可以进入 文章管理区域
        per_page = 15                                    # 每页返回的数量
        pagination = Article.query.filter(Article.reviewed==False).order_by(Article.timestamp.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        articles = pagination.items     # 返回查询到的数据
        return render_template('backstage/article/index.html', current_user=current_user, articles=articles, pagination=pagination)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 文章审核管理
@backstage_blueprint.route('/backstage/reviewed/article/<int:article_id>')
@login_required
def reviewed_article(article_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 2:         # 2级以上可以参与文章的审核
        article = Article.query.filter(Article.id==article_id).first()
        article.reviewed = not article.reviewed
        db.session.commit()
        record = Manage_record(article_id=article_id,
                               admin_id=current_user.id,
                               timestamp=datetime.utcnow(),
                               type='文章审核',
                               result='{}'.format(article.reviewed))
        db.session.add(record)
        if article.reviewed:
            flash('文章已审核。')
        else:
            flash('文章修改为未审核。')
    else:
        flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))


# 文章禁用管理
@backstage_blueprint.route('/backstage/forbid/article/<int:article_id>')
@login_required
def forbid_article(article_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 3:         # 3级以上可以管理内容的禁用
        article = Article.query.filter(Article.id==article_id).first()
        article.forbid = not article.forbid
        db.session.commit()
        record = Manage_record(article_id=article_id,
                               admin_id=current_user.id,
                               timestamp=datetime.utcnow(),
                               type='文章禁用',
                               result='{}'.format(article.forbid))
        db.session.add(record)
        if article.forbid:
            flash('文章已禁用。')
        else:
            flash('文章已解禁。')
    else:
        flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))

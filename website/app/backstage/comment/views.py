# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import Comment, db, Manage_record
from datetime import datetime


# 评论管理页面
@backstage_blueprint.route('/backstage/comment', defaults={'page': 1})
@backstage_blueprint.route('/backstage/comment/page/<int:page>', methods=["GET", "POST"])
@login_required
def comment_manage(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 2:
        per_page = 15                                    # 每页返回的数量
        pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        comments = pagination.items     # 返回查询到的数据
        return render_template('backstage/comment/index.html', current_user=current_user, comments=comments, pagination=pagination)
    flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))


# 评论审核页面
@backstage_blueprint.route('/backstage/comment/reviewed', defaults={'page': 1})
@backstage_blueprint.route('/backstage/comment/reviewed/page/<int:page>', methods=["GET", "POST"])
@login_required
def comment_reviewed(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 2:         # 2级以上 可以进入 文章管理区域
        per_page = 15                   # 每页返回的数量
        pagination = Comment.query.filter(Comment.reviewed==False).order_by(Comment.timestamp.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        comments = pagination.items     # 返回查询到的数据
        return render_template('backstage/comment/index.html', current_user=current_user, comments=comments, pagination=pagination)
    flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))


# 评论审核管理
@backstage_blueprint.route('/backstage/reviewed/comment/<int:comment_id>')
@login_required
def reviewed_comment(comment_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 2:             # 2级以上可以参与文章的审核
        comment = Comment.query.filter(Comment.id==comment_id).first()
        comment.reviewed = not comment.reviewed
        db.session.commit()
        record = Manage_record(admin_id=current_user.id,
                               comment_id=comment_id,
                               timestamp=datetime.utcnow(),
                               type='评论审核',
                               result='{}'.format(comment.reviewed))
        db.session.add(record)
        if comment.reviewed:
            flash('评论已审核。')
        else:
            flash('评论修改为未审核。')
    else:
        flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))


# 评论禁用管理
@backstage_blueprint.route('/backstage/forbid/comment/<int:comment_id>')
@login_required
def forbid_comment(comment_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 3:         # 3级以上可以管理内容的禁用
        comment = Comment.query.filter(Comment.id==comment_id).first()
        comment.forbid = not comment.forbid
        db.session.commit()
        record = Manage_record(comment_id=comment_id,
                               admin_id=current_user.id,
                               timestamp=datetime.utcnow(),
                               type='评论禁用',
                               result='{}'.format(comment.forbid))
        db.session.add(record)
        if comment.forbid:
            flash('评论已禁用。')
        else:
            flash('评论已解禁。')
    else:
        flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))
# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import Manage_record, Content_record


# 管理日志页面
@backstage_blueprint.route('/backstage/manage_record', defaults={'page': 1})
@backstage_blueprint.route('/backstage/manage_record/page/<int:page>', methods=["GET", "POST"])
@login_required
def record_manage(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:                         # 5级以上，可以查看管理日志
        per_page = 15                                   # 每页返回的数量
        pagination = Manage_record.query.order_by(Manage_record.id.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        records = pagination.items     # 返回查询到的数据
        return render_template('backstage/record/manage.html', current_user=current_user, records=records, pagination=pagination)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 内容日志页面
@backstage_blueprint.route('/backstage/content_record', defaults={'page': 1})
@backstage_blueprint.route('/backstage/content_record/page/<int:page>', methods=["GET", "POST"])
@login_required
def record_content(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:                         # 5级以上，可以查看管理日志
        per_page = 15                                   # 每页返回的数量
        pagination = Content_record.query.order_by(Content_record.id.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        records = pagination.items     # 返回查询到的数据
        return render_template('backstage/record/content.html', current_user=current_user, records=records, pagination=pagination)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))
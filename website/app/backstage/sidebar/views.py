# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import db, Manage_record, Side_Bar
from datetime import datetime
from .forms import SidebarEditForm


# 侧栏管理页面
@backstage_blueprint.route('/backstage/sidebar', defaults={'page': 1})
@backstage_blueprint.route('/backstage/sidebar/page/<int:page>', methods=["GET", "POST"])
@login_required
def sidebar_manage(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 4:                         # 4级以上可以管理用户， 这里是进入用户管理界面
        per_page = 15                                   # 每页返回的数量
        pagination = Side_Bar.query.order_by(Side_Bar.id.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        sidebars = pagination.items     # 返回查询到的数据
        return render_template('backstage/sidebar/index.html', current_user=current_user, sidebars=sidebars, pagination=pagination)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 侧栏编辑路由
@backstage_blueprint.route('/backstage/sidebar/edit/<int:sidebar_id>', methods=['GET', 'POST'])
@login_required
def edit_sidebar(sidebar_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = SidebarEditForm()
        sidebar = Side_Bar.query.get(sidebar_id)
        if sidebar:
            if form.validate_on_submit():
                if sidebar.title != form.title.data or sidebar.body != form.body.data or sidebar.forbid != form.forbid.data:
                    sidebar.title = form.title.data
                    sidebar.body = form.body.data
                    sidebar.forbid = form.forbid.data
                    flash('侧栏已编辑。')
                    record = Manage_record(admin_id=current_user.id,
                                           timestamp=datetime.utcnow(),
                                           site_ops='侧栏{}'.format(sidebar_id),
                                           type='编辑',
                                           result='成功')
                    db.session.add(record)
            form.title.data = sidebar.title
            form.body.data = sidebar.body
            form.forbid.data = sidebar.forbid
        return render_template('backstage/sidebar/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 侧栏新建页面
@backstage_blueprint.route('/backstage/sidebar/build', methods=['GET', 'POST'])
@login_required
def build_sidebar():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = SidebarEditForm()
        if form.validate_on_submit():
            sidebar = Side_Bar(title=form.title.data,
                               body=form.body.data,
                               forbid=form.forbid.data)
            db.session.add(sidebar)
            db.session.commit()         # 先提交，因为需要用到id
            record = Manage_record(admin_id=current_user.id,
                                   timestamp=datetime.utcnow(),
                                   site_ops='侧栏{}'.format(sidebar.id),
                                   type='新建',
                                   result='成功')
            db.session.add(record)

        return render_template('backstage/sidebar/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 侧栏删除路由
@backstage_blueprint.route('/backstage/sidebar/delete/<int:sidebar_id>')
@login_required
def delete_sidebar(sidebar_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        sidebar = Side_Bar.query.get(sidebar_id)
        record = Manage_record(admin_id=current_user.id,
                               timestamp=datetime.utcnow(),
                               site_ops='侧栏{}'.format(sidebar.id),
                               type='删除',
                               result='成功')
        db.session.add(record)
        db.session.delete(sidebar)
        return redirect(url_for('backstage.sidebar_manage'))
    return redirect(request.referrer or url_for('backstage.index'))

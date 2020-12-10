# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import User, db, Manage_record
from datetime import datetime


# 用户管理页面
@backstage_blueprint.route('/backstage/user', defaults={'page': 1})
@backstage_blueprint.route('/backstage/user/page/<int:page>', methods=["GET", "POST"])
@login_required
def user_manage(page):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 4:             # 4级以上可以管理用户， 这里是进入用户管理界面
        per_page = 15                       # 每页返回的数量
        pagination = User.query.order_by(User.id.desc()).paginate(page=page, per_page=per_page)    # 按页查询
        users = pagination.items            # 返回查询到的数据
        return render_template('backstage/user/index.html', current_user=current_user, users=users, pagination=pagination)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 用户禁用管理
@backstage_blueprint.route('/backstage/forbid/user/<int:user_id>')
@login_required
def forbid_user(user_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 4:             # 4级以上可以管理用户的禁用
        user = User.query.filter(User.id==user_id).first()
        if current_user.level > user.level:
            user.forbid = not user.forbid
            db.session.commit()
            record = Manage_record(user_id=user_id,
                                   admin_id=current_user.id,
                                   timestamp=datetime.utcnow(),
                                   type='用户禁用',
                                   result='{}'.format(user.forbid))
            db.session.add(record)
            if user.forbid:
                flash('用户{}已被禁用。'.format(user.username))
            else:
                flash('用户{}已被解禁。'.format(user.username))
        else:
            flash('权限不够。')
    else:
        flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))

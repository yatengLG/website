# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import db, Manage_record
from datetime import datetime
from .forms import DocForm


@backstage_blueprint.route('/backstage/doc/edit/<string:filename>', methods=["GET","POST"])
@login_required
def edit_doc(filename):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))

    if current_user.level >= 4:
        save_file = 'app/document/{}.txt'.format(filename)
        with open(save_file, 'r') as f1:
            body = f1.read()
        form = DocForm()
        if form.validate_on_submit():
            if form.body.data != body:
                body = form.body.data
                with open(save_file,'w')as f2:
                    f2.write(body)
                record = Manage_record(admin_id=current_user.id,
                                       timestamp=datetime.utcnow(),
                                       site_ops='文档{}'.format(filename),
                                       type='编辑',
                                       result='成功')
                db.session.add(record)
                flash('{}已修改'.format(filename))
            return redirect(url_for('main.doc', filename=filename))
        form.body.data = body
        return render_template('backstage/doc/edit.html', current_user=current_user, form=form)
    else:
        flash('权限不够。')
    return redirect(request.referrer or url_for('main.index'))
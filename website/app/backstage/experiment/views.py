# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import db, Manage_record, Experiment
from datetime import datetime
from .forms import Experimentform


# 实验管理页面
@backstage_blueprint.route('/backstage/experiment')
@login_required
def experiment_manage():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:                         # 5级以上，可以查看管理日志
        experiments = Experiment.query.all()
        return render_template('backstage/experiment/index.html', current_user=current_user, experiments=experiments)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 实验新建页面
@backstage_blueprint.route('/backstage/experiment/build', methods=['GET', 'POST'])
@login_required
def build_experiment():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = Experimentform()
        if form.validate_on_submit():
            experiment = Experiment(title=form.title.data,
                                    coverpic=form.coverpic.data,
                                    link=form.link.data,
                                    forbid=form.forbid.data)
            db.session.add(experiment)
            db.session.commit()         # 先提交，因为需要用到id
            record = Manage_record(admin_id=current_user.id,
                                   timestamp=datetime.utcnow(),
                                   site_ops='实验{}'.format(experiment.id),
                                   type='新建',
                                   result='成功')
            db.session.add(record)
            return redirect(url_for('backstage.experiment_manage'))
        return render_template('backstage/experiment/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 推荐编辑路由
@backstage_blueprint.route('/backstage/experiment/edit/<int:experiment_id>', methods=['GET', 'POST'])
@login_required
def edit_experiment(experiment_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = Experimentform()
        experiment = Experiment.query.get(experiment_id)
        if experiment:
            if form.validate_on_submit():
                if experiment.title != form.title.data \
                        or experiment.forbid != form.forbid.data \
                        or experiment.link != form.link.data \
                        or experiment.coverpic != form.coverpic.data:

                    experiment.title = form.title.data
                    experiment.coverpic = form.coverpic.data
                    experiment.link = form.link.data
                    experiment.forbid = form.forbid.data
                    flash('推荐已编辑。')
                    record = Manage_record(admin_id=current_user.id,
                                           timestamp=datetime.utcnow(),
                                           site_ops='实验{}'.format(experiment_id),
                                           type='编辑',
                                           result='成功')
                    db.session.add(record)
                else:
                    flash('侧栏未编辑。')
                return redirect(url_for('backstage.experiment_manage'))
            form.title.data = experiment.title
            form.coverpic.data = experiment.coverpic
            form.link.data = experiment.link
            form.forbid.data = experiment.forbid
        return render_template('backstage/experiment/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 推荐删除路由
@backstage_blueprint.route('/backstage/experiment/delete/<int:experiment_id>')
@login_required
def delete_experiment(experiment_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        experiment = Experiment.query.get(experiment_id)
        record = Manage_record(admin_id=current_user.id,
                               timestamp=datetime.utcnow(),
                               site_ops='实验{}'.format(experiment.id),
                               type='删除',
                               result='成功')
        db.session.add(record)
        db.session.delete(experiment)
        return redirect(url_for('backstage.experiment_manage'))
    return redirect(request.referrer or url_for('backstage.index'))
# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import db, Manage_record, Recommendation
from datetime import datetime
from .forms import Recommendationform


# 推荐管理页面
@backstage_blueprint.route('/backstage/recommendation')
@login_required
def recommendation_manage():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:                         # 5级以上，可以查看管理日志
        recommendations = Recommendation.query.all()
        return render_template('backstage/recommendation/index.html', current_user=current_user, recommendations=recommendations)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 推荐新建页面
@backstage_blueprint.route('/backstage/recommendation/build', methods=['GET', 'POST'])
@login_required
def build_recommendation():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = Recommendationform()
        if form.validate_on_submit():
            recommendation = Recommendation(article_id=form.article_id.data,
                                            coverpic=form.coverpic.data,
                                            link=form.link.data,
                                            forbid=form.forbid.data)
            db.session.add(recommendation)
            db.session.commit()         # 先提交，因为需要用到id
            record = Manage_record(admin_id=current_user.id,
                                   timestamp=datetime.utcnow(),
                                   site_ops='推荐{}'.format(recommendation.id),
                                   type='新建',
                                   result='成功')
            db.session.add(record)
            return redirect(url_for('backstage.recommendation_manage'))
        return render_template('backstage/recommendation/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 推荐编辑路由
@backstage_blueprint.route('/backstage/recommendation/edit/<int:recommendation_id>', methods=['GET', 'POST'])
@login_required
def edit_recommendation(recommendation_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = Recommendationform()
        recommendation = Recommendation.query.get(recommendation_id)
        if recommendation:
            if form.validate_on_submit():
                if recommendation.article_id != form.article_id.data or recommendation.forbid != form.forbid.data or recommendation.link != form.link.data or recommendation.coverpic != form.coverpic.data:
                    recommendation.article_id = form.article_id.data
                    recommendation.coverpic = form.coverpic.data
                    recommendation.link = form.link.data
                    recommendation.forbid = form.forbid.data
                    flash('推荐已编辑。')
                    record = Manage_record(admin_id=current_user.id,
                                           timestamp=datetime.utcnow(),
                                           site_ops='推荐{}'.format(recommendation_id),
                                           type='编辑',
                                           result='成功')
                    db.session.add(record)
                else:
                    flash('侧栏未编辑。')
                return redirect(url_for('backstage.recommendation_manage'))
            form.article_id.data = recommendation.article_id
            form.coverpic.data = recommendation.coverpic
            form.link.data = recommendation.link
            form.forbid.data = recommendation.forbid
        return render_template('backstage/recommendation/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 推荐删除路由
@backstage_blueprint.route('/backstage/recommendation/delete/<int:recommendation_id>')
@login_required
def delete_recommendation(recommendation_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        recommendation = Recommendation.query.get(recommendation_id)
        record = Manage_record(admin_id=current_user.id,
                               timestamp=datetime.utcnow(),
                               site_ops='推荐{}'.format(recommendation.id),
                               type='删除',
                               result='成功')
        db.session.add(record)
        db.session.delete(recommendation)
        return redirect(url_for('backstage.recommendation_manage'))
    return redirect(request.referrer or url_for('backstage.index'))

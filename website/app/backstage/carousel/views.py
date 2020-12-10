# -*- coding: utf-8 -*-
# @Author  : LG


from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import db, Manage_record, Carousel
from datetime import datetime
from .forms import CarouselEditform


# 轮播管理页面
@backstage_blueprint.route('/backstage/carousel')
@login_required
def carousel_manage():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:                         # 5级以上，可以查看管理日志
        carousels = Carousel.query.all()
        return render_template('backstage/carousel/index.html', current_user=current_user, carousels=carousels)
    flash('权限不够')
    return redirect(request.referrer or url_for('main.index'))


# 轮播新建页面
@backstage_blueprint.route('/backstage/carousel/build', methods=['GET', 'POST'])
@login_required
def build_carousel():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = CarouselEditform()
        if form.validate_on_submit():
            carousel = Carousel(article_id=form.article_id.data,
                                forbid=form.forbid.data)
            db.session.add(carousel)
            db.session.commit()         # 先提交，因为需要用到id
            record = Manage_record(admin_id=current_user.id,
                                   timestamp=datetime.utcnow(),
                                   site_ops='轮播{}'.format(carousel.id),
                                   type='新建',
                                   result='成功')
            db.session.add(record)
            return redirect(url_for('backstage.carousel_manage'))
        return render_template('backstage/carousel/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 轮播编辑路由
@backstage_blueprint.route('/backstage/carousel/edit/<int:carousel_id>', methods=['GET', 'POST'])
@login_required
def edit_carousel(carousel_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        form = CarouselEditform()
        carousel = Carousel.query.get(carousel_id)
        if carousel:
            if form.validate_on_submit():
                if carousel.article_id != form.article_id.data or carousel.forbid != form.forbid.data:
                    carousel.article_id = form.article_id.data
                    carousel.forbid = form.forbid.data
                    flash('侧栏已编辑。')
                    record = Manage_record(admin_id=current_user.id,
                                           timestamp=datetime.utcnow(),
                                           site_ops='轮播{}'.format(carousel_id),
                                           type='编辑',
                                           result='成功')
                    db.session.add(record)
                else:
                    flash('侧栏未编辑。')
                return redirect(url_for('backstage.carousel_manage'))
            form.article_id.data = carousel.article_id
            form.forbid.data = carousel.forbid
        return render_template('backstage/carousel/edit.html', current_user=current_user, form=form)
    return redirect(request.referrer or url_for('backstage.index'))


# 轮播删除路由
@backstage_blueprint.route('/backstage/carousel/delete/<int:carousel_id>')
@login_required
def delete_carousel(carousel_id):
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 4:
        carousel = Carousel.query.get(carousel_id)
        record = Manage_record(admin_id=current_user.id,
                               timestamp=datetime.utcnow(),
                               site_ops='轮播{}'.format(carousel.id),
                               type='删除',
                               result='成功')
        db.session.add(record)
        db.session.delete(carousel)
        return redirect(url_for('backstage.carousel_manage'))
    return redirect(request.referrer or url_for('backstage.index'))

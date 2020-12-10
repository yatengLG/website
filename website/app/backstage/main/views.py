# -*- coding: utf-8 -*-
# @Author  : LG

from .. import backstage_blueprint
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user


# 后台主页
@backstage_blueprint.route('/backstage')
@login_required
def index():
    if current_user.forbid:
        return redirect(request.referrer or url_for('main.index'))
    if current_user.level >= 2:
        return render_template('backstage/index.html', current_user=current_user)
    else:
        return redirect(url_for('main.index'))
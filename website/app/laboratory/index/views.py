# -*- coding: utf-8 -*-
# @Author  : LG

from .. import laboratory_blueprint
from flask_login import login_required
from flask import render_template, request
from ...models import Experiment


@laboratory_blueprint.route('/laboratory')
def index():
    experiments = Experiment.query.filter(Experiment.forbid==False).all()
    return render_template('laboratory/index.html', experiments=experiments)

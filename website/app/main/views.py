# -*- coding: utf-8 -*-
# @Author  : LG

from . import main_blueprint
from flask import render_template, request, jsonify
from flask_login import current_user, login_required
from ..models import Article, Side_Bar, Carousel, Recommendation
from sqlalchemy import and_
from PIL import Image
from ..utils.upload import upload_file_qiniu, random_filename
import io


@main_blueprint.route('/', defaults={'page': 1})
@main_blueprint.route('/page/<int:page>')
def index(page):
    per_page = 10                                    # 每页返回的数量
    pagination = Article.query.filter(and_(Article.reviewed==True, Article.forbid==False, Article.public==True)).order_by(Article.timestamp.desc()).paginate(page=page, per_page=per_page)    # 按页查询
    articles = pagination.items     # 返回查询到的数据

    # 侧栏
    sidebars = Side_Bar.query.all()
    # 轮播
    carousels = Carousel.query.all()
    carousels = [carousel for carousel in carousels
                 if carousel.article
                 if carousel.article.reviewed==True and carousel.article.forbid==False and carousel.article.public==True]
    # 推荐
    recommendations = Recommendation.query.filter(Recommendation.forbid==False).all()
    return render_template('main/index.html', current_user=current_user, articles=articles, pagination=pagination, carousels=carousels, recommendations=recommendations, sidebars=sidebars)


@main_blueprint.route('/doc/<string:filename>')
def doc(filename):
    print(filename)
    aboutus_file = 'app/document/{}.txt'.format(filename)
    with open(aboutus_file,'r')as f:
        body = f.read()
    return render_template('main/doc.html', body=body)


@main_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    print(request.cookies)
    file = request.files.get('file')
    image = Image.open(file)
    image.thumbnail((1080, 960))
    filename = random_filename(file.filename)
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    try:
        upload_file_qiniu(data=imgByteArr, rename=filename)
    except Exception as e:
        return jsonify(errmsg='上传失败')
    return { "location": filename }

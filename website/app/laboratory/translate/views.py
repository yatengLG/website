# -*- coding: utf-8 -*-
# @Author  : LG

from .. import laboratory_blueprint
from flask_login import login_required
from flask import render_template, request
import http.client
import hashlib
import urllib
import random
import json


@laboratory_blueprint.route('/laboratory/translation', methods=["GET"])
@login_required
def translation():
    return render_template('laboratory/translation.html')


@laboratory_blueprint.route('/laboratory/translate', methods=["GET", "POST"])
def translate():
    content = request.form.get('from_content')
    fromLang = request.form.get('from_lang')
    toLang = request.form.get('to_lang')

    results = translate_fn(content, fromLang, toLang)
    results = results['trans_result']
    results = [str(result['dst']) for result in results]
    results = '<br>'.join(results)
    return results


def translate_fn(content, fromLang, toLang):
    appid = '百度翻译key'  # 填写你的appid
    secretKey = '百度翻译key'  # 填写你的密钥
    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    if fromLang is None:
        fromLang='auto'
    if toLang is None:
        toLang='zh'
    sign = appid + str(content) + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()

    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(content) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        return result

    except Exception as e:
        return e

    finally:
        if httpClient:
            httpClient.close()



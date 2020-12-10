# -*- coding: utf-8 -*-
# @Author  : LG

from qiniu import Auth, put_data, etag
import os
import uuid

access_key = '七牛云access_key' or os.environ.get('QINIU_ACCESS_KEY')
secret_key = '七牛云secret_key' or os.environ.get('QINIU_SECRET_KEY')


def upload_file_qiniu(data, bucket_name='pic-data', rename=None):
    """
    七牛云上传文件
    :param data:    byte型数据
    :bucket_name:   存储的空间名
    :rename:        重命名
    :return:
    """
    # 构建鉴权对象
    q = Auth(access_key=access_key, secret_key=secret_key)
    # 生成上传token
    token = q.upload_token(bucket_name)
    # key 为上传数据的重命名
    ret1, ret2 = put_data(up_token=token, key=rename, data=data)
    print('ret1:',ret1)
    print('ret2:',ret2)

    if ret2.status_code!=200:
        raise Exception('文件上传失败')
    # 这里返回七牛云存储的数据名
    return ret1.get('key')


# 用于生成随机文件名
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename
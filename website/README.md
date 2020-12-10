# website
之前想自己写一个类似内容分享网站，于是，就有了这个项目

项目基于flask编写。

现分享出来供大家学习交流，由于是第一次写网站，很多东西不完善，但是可以作为一个学习项目。

## 结构
```text
├── app
│   ├── article                             // 文章蓝图
│   │   ├──__init__.py
│   │   ├──forms.py
│   │   └──views.py
│   ├── main                                // 主蓝图
│   │   ├──__init__.py
│   │   ├──errors.py
│   │   └──views.py
│   ├── static                              // 静态文件
│   │   ├──css
│   │   ├──js
│   │   ├──imgs
│   │   ├──tinymce
│   │   └──bootstrap-4.3.1-dist.zip
│   ├── templates                           // 模板
│   │   ├──article
│   │   ├──main
│   │   ├──user
│   │   └──base.html
│   ├── user                                // 用户蓝图
│   │   ├──__init__.py
│   │   ├──forms.py
│   │   └──views.py
│   ├── __init__.py
│   ├── config.py                           // 设置
│   ├── data-dev.splite                     // 数据库
│   ├── email.py                            // 发送邮件
│   └── models.py                           // 数据库模型
├── migrations                              // 数据库管理文件，勿动
├── manage.py                               // 主文件夹
├── README.md                          
```

## 使用

#### 运行
```text
python manage.py runserver
```

#### 新建数据库
```text
python manage.py shell

db.create_all()
```

#### 数据库迁移、升级
如果数据库新添加了表/列，或删除了某表/列时使用。
```text
# 首先创建迁移仓库， 也就是文件结构中对应的migrations文件夹
python manage.py db init

# 创建迁移脚本
python manage.py db migrate -m 'initial migration'

# 更新数据库
python manage.py db upgrade
```

# 服务器端部署
```text
##uwsgi 停止
uwsgi --stop uwsgi.pid

## uwsgi 从配置启动
uwsgi --ini uwsgi.ini
```

```text
## nginx 停止
nginx -s quit

## nginx 从配置启动
nginx -c nginx.conf # 配置文件需为绝对路况
```

|蓝图|路由|地址|模板|相关文件|说明|
|:----:|:----:|:----:|:----:|:----:|:----:|
|main|index|'/', '/page/<int:page'|main/index.html| -- |主页
| |doc|'/doc/<string:filename'|main/doc.html| -- |文档页面，本站以及免责声明|
| |upload|'/upload'| -- | -- |上传图片|
|user|home|'/user/home/<int:user_id' |user/home.html|--|用户主页|
| |login|'/user/login'|user/login.html| -- |登录|
| |logout|'/user/logout'| -- | -- | 登出|
| |register|'/user/register'|user/register.html| user/email/confirm |注册|
| |confirm|'/user/confirm/<token'| -- | -- |验证|
| |resend_confirmation|'/user/confirm'| -- | user/email/confirm.txt |重新验证|
| |forget_password|'/user/forgetpassword'|user/forgetpassword.html| user/email/resetpassword.txt |忘记密码页面|
| |reset_password|'/user/resetpassword/<token'|user/resetpassword.html| -- |重置密码页面|
| |remove|'/user/remove'| -- | user/email/remove.txt |注销账号申请|
| |remove_confirm|'/user/remove/<token'| -- | -- | 注销账号验证
|article|build|'/article/build'|article/build.html|--|新建文章页面|
| |edit|'/article/edit/<article_id>'|article/edit.html|--|编辑文章页面|
| |delete|'/article/delete/<article_id>'|--|--|删除文章|
| |article_show|'/article/show/<article_id>'|/article/show.html|--|文章展示页面|
| |delete|'/article/delete/<article_id>'|--|--|删除文章|
| |comment_delete|'/comment/delete/<comment_id>'|--|--|删除评论|
|backstage|index|'/backstage/home'|backstage/index.html|--|后台主页|
| |article_manage|'/backstage/article', '/backstage/article/page/<int:page>'|backstage/article.html|--|文章管理页面|
| |comment_manage|'/backstage/comment', '/backstage/comment/page/<int:page>'|backstage/comment.html|--| 评论管理页面|
| |user_manage|'/backstage/user', '/backstage/user/page/<int:page>'|backstage/user.html|--|用户管理页面|
| |article_reviewed|'/backstage/article/reviewed', '/backstage/article/reviewed/page/<int:page>'| backstage/article.html|--|文章审核页面|
| |comment_reviewed|'/backstage/comment/reviewed', '/backstage/comment/reviewed/page/<int:page>'|backstage/comment.html|--|评论审核页面|
| |reviewed_article|'/backstage/reviewed/article/<int:article_id>'|--|--|文章审核|
| |reviewed_comment|'/backstage/reviewed/comment/<int:comment_id>'|--|--|评论审核|
| |forbid_article|'/backstage/forbid/article/<int:article_id>'|--|--|文章禁用|
| |forbid_comment|'/backstage/forbid/comment/<int:comment_id>'|--|--|评论禁用|
| |forbid_user|'/backstage/forbid/user/<int:user_id>'|--|--|用户禁用|
| |edit_doc|'/backstage/doc/edit/<string:filename>'|backstage/edit_doc.html|--|文档编辑页面|
| |edit_sidebar|'backstage/sidebar/edit/<int:sidebar_id>'|backstage/sidebar.html|--|侧栏编辑页面|
| |build_sidebar|'/backstage/sidebar/build'|backstage/sidebar.html|--|侧栏新建页面|
| |carousel_manage|'/backstage/carousel'|backstage/carousel.html|--|轮播管理页面|
| |build_carousel|'/backstage/carousel/build'|backstage/carousel_edit.html|--|轮播创建页面|
| |edit_carousel|'/backstage/carousel/edit/<int:carousel_id>'|backstage/carousel_edit.html|--|轮播编辑页面|
| |delete_carousel|'/backstage/carousel/delete/<int:carousel_id>'|--|--|轮播删除|
| |record_manage|'/backstage/manage_record/page/<int:page>'|backstage/manage_record.html|--|管理日志页面
| |record_content|'/backstage/content_record/page/<int:page>'|backstage/content_record.html|--|管理日志页面

## 环境变量配置
|环境变量名|说明|备注|
|:----:|:----:|:----:|
|QINIU_ACCESS_KEY|七牛云access_key| 必填 |
|QINIU_SECRET_KEY|七牛云sceret_key| 必填 |
|MAIL_PASSWORD|邮件系统授权码| 必填 |

## 管理员权限等级
|等级|权限|
|:----:|:----:|
|2|文章、评论审核|
|3|文章、评论禁用|
|4|网站管理：轮播、侧栏、用户、管理日志、文档|

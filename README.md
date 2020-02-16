Pirate
===

一个通过简单API手动抓取微信公众号文章的Extractor。

通过CDN清洗微信图片。

用法：假设部署后的域名为 www.myhost.com

    POST http://www.myhost.com/api/v1/extrack/wx/

    params:

        * raw_url: 类型string, 微信公众号文章的路由

用到的技术
---

* original - 本项目使用的Django脚手架 (original)[https://github.com/duoduo369/original]
* virtualenv + pip - 项目依赖管理
* nginx + supervisor - 项目部署相关
* cdn - 七牛免费可以有一些额度
* 域名和ssl证书


部署相关文件
---

创建 config/settings/private_production.py

    import os

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'dbname', # 改成你的数据库名字
            'HOST': os.environ.get('ORIGINAL_MYSQL_HOST', 'localhost'), # 数据库host
            'USER': os.environ.get('ORIGINAL_MYSQL_USER', 'db_username'), # 改成你的数据库user
            'PASSWORD': os.environ.get('ORIGINAL_MYSQL_PASSWORD', 'db_password'), # 改成你的数据库password
            'PORT': os.environ.get('ORIGINAL_MYSQL_PORT', 3306),
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }

    FILE_UPLOAD_BACKEND = 'qiniu'
    FILE_UPLOAD_KEY = 'i6fdSECQjLfF' # 改成你的qiniu key，现在这里是假的
    FILE_UPLOAD_SECRET = 'adfiuerqp' # 改成你的qiniu secret
    FILE_UPLOAD_BUCKET = 'reworkdev' # 改成你的qiniu bucket
    FILE_CALLBACK_POLICY = {}
    FILE_DOWNLOAD_PREFIX = '' # 改成你的host, 例如 http://cdn.myhost.com/

    FILEUPLOAD_CALLBACK_URL = # 改成你自己host的对应地址, 例如 https://www.myhost.com/api/v1/file/upload/callback/

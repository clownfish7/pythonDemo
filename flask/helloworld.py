#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : helloworld.py
  @Desc     : 
  @Time     : 2020/12/23 14:06
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""

# 导入Flask类
from flask import Flask

# Flask类接收一个参数__name__
app = Flask(__name__)

# 装饰器的作用是将路由映射到视图函数index
@app.route('/')
def index():
    return 'Hello World!'


# Flask应用程序实例的run方法启动WEB服务器
if __name__ == '__main__':
    app.run()

"""
Flask 程序实例在创建的时候，需要默认传入当前 Flask 程序所指定的包(模块)，接下来就来详细查看一下 Flask 应用程序在创建的时候一些需要我们关注的参数：

import_name
    Flask程序所在的包(模块)，传 __name__ 就可以
    其可以决定 Flask 在访问静态文件时查找的路径
static_url_path
    静态文件访问路径，可以不传，默认为：/ + static_folder
static_folder
    静态文件存储的文件夹，可以不传，默认为 static
template_folder
    模板文件存储的文件夹，可以不传，默认为 templates
    
默认参数情况下
app = Flask(__name__)
文件目录

----
  |---static
  |     |--- 1.png
  |---helloworld.py
访问 127.0.0.1:5000/static/1.png 就可以访问到图片

修改参数的情况下
app = Flask(__name__, static_url_path='/url_path_param', static_folder='folder_param')
文件目录

----
  |---folder_param     # 此处目录名变化
  |     |--- 1.png
  |---helloworld.py
访问127.0.0.1:5000/url_path_param/1.png才可以访问到图片
"""

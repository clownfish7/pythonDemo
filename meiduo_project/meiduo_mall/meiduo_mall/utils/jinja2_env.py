#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : jinja2_env.py
  @Desc     : 
  @Time     : 2020/12/23 15:44
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment


def jinja2_environment(**options):
    """jinja2环境"""
    # 创建环境对象
    env = Environment(**options)
    # 自定义语法：{{ static('静态文件相对路径') }} {{ url('路由的m命名空间') }}
    env.globals.update({
        # 获取静态文件的前缀
        'static': static,
        # 反向解析
        'url': reverse,
    })
    return env


"""
确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句 
"""

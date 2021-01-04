#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : urls.py
  @Desc     : 
  @Time     : 2021/1/4 19:22
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from django.urls import re_path
from . import views

app_name = 'areas'
urlpatterns = [
    re_path(r'^areas/$', views.AreaView.as_view())
]

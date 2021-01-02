#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : urls.py
  @Desc     : 
  @Time     : 2021/1/3 0:23
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from django.urls import path, re_path
from . import views

app_name = 'oauth'
urlpatterns = [
    # QQ 登录扫码页面
    re_path(r'^qq/login/', views.QQLoginURLView.as_view()),
    # QQ 回调
    re_path(r'^oauth_callback/$', views.QQAuthUserView.as_view())
]

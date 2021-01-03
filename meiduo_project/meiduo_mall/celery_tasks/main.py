#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : main.py
  @Desc     : Celery 入口 celery -A celery_tasks.main worker -l info
  @Time     : 2021/1/2 3:05
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from celery import Celery
import os

# 为celery使用django配置文件进行设置
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'
# 创建实例
celery_app = Celery('meiduo')
# 加载 celery 配置
celery_app.config_from_object('celery_tasks.config')
# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])

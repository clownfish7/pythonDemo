#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : tasks.py
  @Desc     : 定义任务
  @Time     : 2021/1/2 3:14
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from celery_tasks.sms.yuntongxun.ccp_sms import CCP
from celery_tasks.main import celery_app
from . import constants


# 使用 celery 装饰器装饰异步任务，保证任务识别
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                            constants.SEND_SMS_TEMPLATE_ID)

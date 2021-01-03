#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : views.py
  @Desc     : 
  @Time     : 2021/1/3 20:44
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django import http

from meiduo_mall.utils.response_code import RETCODE, err_msg


class LoginRequiredJSONMixin(LoginRequiredMixin):
    """自定义判断用户是否登录扩展类，返回JSON"""

    def handle_no_permission(self):
        return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': err_msg[RETCODE.SESSIONERR]})

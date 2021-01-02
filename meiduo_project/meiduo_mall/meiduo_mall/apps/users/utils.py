#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : utils.py
  @Desc     : 
  @Time     : 2021/1/2 20:52
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from django.contrib.auth.backends import ModelBackend
import re

from users.models import User


def get_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(mobile=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileBacked(ModelBackend):
    """自定义用户认证后端"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法
        @param request:
        @param username: mobile or username
        @param password:
        @param kwargs:
        @return: user
        """
        user = get_user_by_account(username)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        else:
            return None

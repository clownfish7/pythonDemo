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
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadData
import re

from users.models import User
from . import constants


def get_user_by_account(account):
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
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


def generate_verify_email_url(user):
    """邮箱激活url"""
    serializer = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id, 'email': user.email}
    token = serializer.dumps(data)
    return settings.EMAIL_VERIFY_URL + '?token=' + token.decode()


def check_verify_email_token(token):
    """校验邮箱激活token"""
    serializer = Serializer(settings.SECRET_KEY, constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = serializer.loads(token)
    except BadData as e:
        return None
    else:
        user_id = data.get('user_id')
        email = data.get('email')
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user

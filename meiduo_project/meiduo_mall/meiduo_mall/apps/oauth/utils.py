#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : utils.py
  @Desc     : 
  @Time     : 2021/1/3 19:22
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from itsdangerous import BadData
from itsdangerous.jws import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

from . import constants_oauth


def generate_access_token(openid):
    """
    签名、序列化  openid
    @param openid:
    @return:
    """
    serializer = Serializer(settings.SECRET_KEY, constants_oauth.ACCESS_TOKEN_EXPIRES)
    token = serializer.dumps({'openid': openid})
    return token.decode()


def check_access_token(access_token_openid):
    """
    反序列化 access_token_openid
    @param access_token_openid:
    @return:
    """
    serializer = Serializer(settings.SECRET_KEY, constants_oauth.ACCESS_TOKEN_EXPIRES)
    try:
        data = serializer.loads(access_token_openid)
    except BadData:
        return None
    else:
        return data.get('openid')

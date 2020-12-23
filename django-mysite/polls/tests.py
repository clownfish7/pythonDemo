#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : DjangoDemo
  @File     : tests.py
  @Desc     : 单元测试  python manage.py test
  @Time     : 2020/12/21 19:01
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""
from django.test import TestCase


class SomeTests(TestCase):

    def testa(self):
        a = 1
        print('fuck')
        self.assertEqual(a, 1, 'err')

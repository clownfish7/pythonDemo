#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : log.py
  @Desc     : 
  @Time     : 2020/12/23 16:34
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""

import logging

# 创建日志记录器
logger = logging.getLogger('django')
# 输出日志
logger.debug('测试logging模块debug')
logger.info('测试logging模块info')
logger.error('测试logging模块error')
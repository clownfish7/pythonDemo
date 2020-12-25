#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @Project  : pythonDemo
  @File     : demo_jsonpath.py
  @Desc     : 
  @Time     : 2020/12/25 15:06
  @Author   : clownfish7 yuzhiyou999@outlook.com
  @Software : PyCharm
  @Version  : 1.0
"""

from jsonpath import jsonpath
import requests
import json

# 获取拉勾网城市json字符串
url = 'https://www.lagou.com/lbs/getAllCitySearchLabels.json'
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 "
                  "Safari/537.36 Edg/87.0.664.66 "
}
response = requests.get(url, headers=headers)
json_str = response.content.decode()

# 把json格式字符串转换成python对象
json_obj = json.loads(json_str)

# 从根节点开始，获取所有key为name的值
city_list = jsonpath(json_obj, '$..name')

# 写入文件,指定文件编码为 utf-8
with open('city_name', 'w', encoding='utf-8') as f:
    content = json.dumps(city_list, ensure_ascii=False)
    f.write(content)

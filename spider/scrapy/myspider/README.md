# 爬取传智播客小demo
tree
scrapy startproject myspider

tree
└─myspider
    │  scrapy.cfg
    │
    └─myspider
        │  items.py             -> 自己预计需要爬取的内容
        │  middlewares.py       -> 定义中间件的地方
        │  pipelines.py         -> 管道，保存数据
        │  settings.py          -> 设置文件，UA，启动管道
        │  __init__.py
        │
        └─spiders               -> 自己定义的 spider 文件夹
                __init__.py 
                itcast.py       -> 定义 spider 的文件
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """自定义用户模型类"""
    # db_column 默认为 key 一样
    mobile = models.CharField(db_column='mobile', max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        # 自定义表名
        # db_table 默认为 app名 + 类名
        db_table = 'tb_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

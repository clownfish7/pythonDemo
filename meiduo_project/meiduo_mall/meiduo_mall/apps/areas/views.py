from django.shortcuts import render
from django.views import View
from areas.models import Area
from django import http
from django.http import *
from django.core.cache import cache
import logging

from meiduo_mall.utils.response_code import RETCODE, err_msg

log = logging.getLogger('django')


# Create your views here.
class AreaView(View):
    """省市区数据"""

    def get(self, request):
        """提供省市区数据"""
        area_id = request.GET.get('area_id')

        if not area_id:
            # 读取省份缓存数据
            province_list = cache.get('province_list')
            if not province_list:
                # 提供省份数据
                try:
                    # 查询省份数据
                    province_model_list = Area.objects.filter(parent__isnull=True)
                    # 序列化省级数据
                    province_list = []
                    for province_model in province_model_list:
                        province_list.append({'id': province_model.id, 'name': province_model.name})
                except Exception as e:
                    log.error(e)
                    return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})
                # 默认存储到别名为·default·的配置中
                cache.set('province_list', province_list, 3600)
            # 响应省份数据
            return JsonResponse({'code': RETCODE.OK, 'errmsg': err_msg[RETCODE.OK], 'province_list': province_list})
        else:
            # 读取市或区缓存数据
            sub_data = cache.get('sub_area_' + area_id)
            if not sub_data:
                # 提供市或区数据
                try:
                    # 查询市或区的父级
                    parent_model = Area.objects.get(id=area_id)
                    sub_model_list = parent_model.subs.all()

                    # 序列化市或区数据
                    sub_list = []
                    for sub_model in sub_model_list:
                        sub_list.append({'id': sub_model.id, 'name': sub_model.name})
                    else:
                        sub_data = {
                            'id': parent_model.id,  # 父级pk
                            'name': parent_model.name,  # 父级name
                            'subs': sub_list  # 父级的子集
                        }
                except Exception as e:
                    log.error(e)
                    return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '城市或区数据错误'})
                # 储存市或区缓存数据
                cache.set('sub_area_' + area_id, sub_data, 3600)
            # 响应市或区数据
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data})

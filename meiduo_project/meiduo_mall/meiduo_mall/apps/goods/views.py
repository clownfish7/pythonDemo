from django import http
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View

from contents.utils import get_categories
from goods import models
from goods.models import SKU
from goods.utils import get_breadcrumb
from meiduo_mall.utils.response_code import RETCODE


# Create your views here.


class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """提供商品列表页"""
        # 判断category_id是否正确
        try:
            category = models.GoodsCategory.objects.get(id=category_id)
        except models.GoodsCategory.DoesNotExist:
            return http.HttpResponseNotFound('GoodsCategory does not exist')
        # 接收sort参数：如果用户不传，就是默认的排序规则
        sort = request.GET.get('sort', 'default')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        # 获取sort(排序规则): 如果sort没有值，取'default'
        sort = request.GET.get('sort', 'default')
        # 根据sort选择排序字段，排序字段必须是模型类的属性
        if sort == 'price':
            sort_field = 'price'  # 按照价格由低到高排序
        elif sort == 'hot':
            sort_field = '-sales'  # 按照销量由高到低排序
        else:  # 只要不是'price'和'-sales'其他的所有情况都归为'default'
            sort = 'default'  # 当出现?sort=itcast 也把sort设置我'default'
            sort_field = 'create_time'

        # 分页和排序查询：category查询sku,一查多,一方的模型对象.多方关联字段.all/filter
        # skus = SKU.objects.filter(category=category, is_launched=True) # 无经验查询
        # skus = SKU.objects.filter(category_id=category_id, is_launched=True)  # 无经验查询
        # skus = category.sku_set.filter(is_launched=True).order_by('排序字段：create_time,price,-sales') # 有经验查询
        skus = category.sku_set.filter(is_launched=True).order_by(sort_field)  # 有经验查询

        # 创建分页器
        # Paginator('要分页的记录', '每页记录的条数')
        paginator = Paginator(skus, 5)  # 把skus进行分页，每页5条记录
        # 获取到用户当前要看的那一页（核心数据）
        try:
            page_skus = paginator.page(page_num)  # 获取到page_num页中的五条记录
        except EmptyPage:
            return http.HttpResponseNotFound('Empty Page')
        # 获取总页数：前端的分页插件需要使用
        total_page = paginator.num_pages

        # 渲染页面
        context = {
            'categories': categories,  # 频道分类
            'breadcrumb': breadcrumb,  # 面包屑导航
            'sort': sort,  # 排序字段
            'category_id': category.id,  # 第三级分类
            'page_skus': page_skus,  # 分页后数据
            'total_page': total_page,  # 总页数
            'page_num': page_num,  # 当前页码
        }
        return render(request, 'list.html', context)


class HotGoodsView(View):
    """热销排行"""

    def get(self, request, category_id):
        # 查询指定分类的SKU信息，而且必须是上架的状态，然后按照销量由高到低排序，最后切片取出前两位
        skus = SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 将模型列表转字典列表，构造JSON数据
        hot_skus = []
        for sku in skus:
            sku_dict = {
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url  # 记得要取出全路径
            }
            hot_skus.append(sku_dict)

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'hot_skus': hot_skus})

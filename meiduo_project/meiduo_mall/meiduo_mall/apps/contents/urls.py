from django.urls import path, re_path
from . import views

app_name = 'contents'
urlpatterns = [
    # 首页广告
    re_path(r'^$', views.IndexView.as_view(), name='index'),
]

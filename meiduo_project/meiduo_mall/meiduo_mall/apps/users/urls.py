from django.urls import path, re_path
from . import views

app_name = 'users'
urlpatterns = [
    # path('register/', views.get, name='register'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # 判断用户名是否重复
    re_path(r'^users/(?P<username>[a-zA-Z0-9_-]{5,20})/count/', views.UsernameCountView.as_view()),
    # 用户登录
    re_path(r'^login/', views.LoginView.as_view(), name='login'),
    # 退出登录
    re_path(r'^logout/', views.LogoutView.as_view(), name='logout'),
    # 用户中心
    re_path(r'^info/', views.UserInfoView.as_view(), name='info'),
    # 添加邮箱
    re_path(r'^emails/$', views.EmailView.as_view()),
    # 邮箱验证
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    # 用户收货地址
    re_path(r'^addresses/$', views.AddressView.as_view(), name='address'),
    # 新建用户收货地址
    re_path(r'^addresses/create/$', views.CreateAddressView.as_view()),
    # 修改用户收货地址 & 删除
    re_path(r'^addresses/(?P<address_id>\d+)/$', views.UpdateDestroyAddressView.as_view()),
    # 设置用户默认地址
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', views.DefaultAddressView.as_view()),
    # 修改地址标题
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', views.UpdateTitleAddressView.as_view()),
    # 修改密码
    re_path(r'^pass/$', views.ChangePasswordView.as_view(), name='pass'),
    # 用户商品浏览记录
    re_path(r'^browse_histories/$', views.UserBrowseHistory.as_view()),
]

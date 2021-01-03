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
]

from django.urls import path, re_path
from . import views

app_name = 'verifications'
urlpatterns = [
    re_path(r'verifications/image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    re_path(r'verifications/sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view()),
]

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django import http
from django.db import DatabaseError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection
import re, json, logging

# Create your views here.
from users.models import User
from meiduo_mall.utils.response_code import RETCODE, err_msg
from meiduo_mall.utils.views import LoginRequiredJSONMixin
from celery_tasks.email.tasks import send_verify_email
from users.utils import generate_verify_email_url, check_verify_email_token

log = logging.getLogger('django')


class UsernameCountView(View):
    """用户名检测"""

    def get(self, request, username):
        """
        :param username: 用户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return http.JsonResponse({
            'code': RETCODE.OK,
            'message': err_msg[RETCODE.OK],
            'data': {'count': count},
        })


class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """提供用户注册页面"""
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        sms_code_client = request.POST.get('sms_code')

        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('请勾选用户协议')
        # 短信验证码校验
        redis_conn = get_redis_connection('verifications')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None or sms_code_server.decode() != sms_code_client:
            return render(request, 'register.html', {'sms_code_message': '验证码错误'})

        # 保存注册数据
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        login(request, user)
        # 响应注册结果
        # return http.HttpResponse('注册成功')
        response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response

    def delete(self):
        pass


class LoginView(View):
    """用户登录"""

    def get(self, request):
        """获取用户登录视图"""
        return render(request, 'login.html')

    def post(self, requeust):
        """登录逻辑"""
        username = requeust.POST.get('username')
        password = requeust.POST.get('password')
        remembered = requeust.POST.get('remembered')

        if not all([username, password]):
            return http.HttpResponseForbidden('缺失参数')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.HttpResponseForbidden('username not allow')
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('password not allow')

        # 认证用户
        user = authenticate(username=username, password=password)
        if user is None:
            return render(requeust, 'login.html', {'account_errmsg': "账户或密码错误"})

        # 保持状态
        login(requeust, user)

        # 使用 remembered 确定状态保持周期
        if remembered != 'on':
            # 浏览器结束销毁，单位是 second
            requeust.session.set_expiry(0)
        else:
            # 状态保持 2 week 默认两周
            requeust.session.set_expiry(None)

        # 响应结果重定向到首页
        if requeust.GET.get('next'):
            response = redirect(requeust.GET.get('next'))
        else:
            response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response


class LogoutView(View):
    """用户退出登录"""

    def get(self, request):
        """清除session"""
        logout(request)
        # clear cookie
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response


class UserInfoView(LoginRequiredMixin, View):
    """用户中心"""

    def get(self, request):
        # if request.user.is_authenticated:
        #     return render(request, 'user_center_info.html')
        # return redirect('users:login')
        # LoginRequiredMixin 判断用户已登录 request.user 就是登录用户对象
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }
        return render(request, 'user_center_info.html', context)


class EmailView(LoginRequiredJSONMixin, View):
    """添加邮箱"""

    def put(self, request):
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('email error')
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            log.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': err_msg[RETCODE.DBERR]})

        # send email
        email_verify_url = generate_verify_email_url(request.user)
        send_verify_email.delay(request.user.email, email_verify_url)

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': err_msg[RETCODE.OK]})


class VerifyEmailView(View):
    """验证邮箱"""

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return http.HttpResponseForbidden('no token')
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseBadRequest('unuseful token')
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            log.error(e)
            return http.HttpResponseServerError('email active error')
        return redirect(reverse('users:info'))


class AddressView(View):
    """用户收货地址"""

    def get(self, request):
        """提供收货地址页面"""
        return render(request, 'user_center_site.html')

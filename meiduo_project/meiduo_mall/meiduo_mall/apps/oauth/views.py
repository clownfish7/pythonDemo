from django.shortcuts import render, redirect, reverse
from django.views import View
from django.conf import settings
from django.contrib.auth import login
from django import http
from QQLoginTool.QQtool import OAuthQQ
from django_redis import get_redis_connection
import logging, re

from meiduo_mall.utils.response_code import RETCODE, err_msg
from oauth.models import OauthQQUser
from oauth.utils import generate_access_token, check_access_token
from users.models import User

# Create your views here.
log = logging.getLogger('django')


class QQLoginURLView(View):
    """QQ登录扫码页面"""

    def get(self, request):
        next = request.GET.get('next')

        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next)

        login_url = oauth.get_qq_url()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': err_msg[RETCODE.OK], 'login_url': login_url})


class QQAuthUserView(View):
    """处理QQ回调"""

    def get(self, request):
        code = request.GET.get('CODE')
        if not code:
            return http.HttpResponseServerError('get code error')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            token = oauth.get_access_token(code)
            open_id = oauth.get_open_id(token)
        except Exception as e:
            log.error(e)
            return http.HttpResponseServerError('OAuth2 failed')

        try:
            oauth_user = OauthQQUser.objects.get(open_id=open_id)
        except OauthQQUser.DoesNotExist:
            content = {'access_token_openid': generate_access_token(open_id)}
            return render(request, 'oauth_callback.html', content)
        else:
            login(request, oauth_user.user)
            next = request.POST.get('state')
            response = redirect(next)
            response.set_cookie('username', oauth_user.user.username, max_age=3600 * 24 * 15)
            return response

    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token_openid = request.POST.get('access_token_openid')

        # 判断参数是否齐全
        if not all([password, mobile, sms_code_client, access_token_openid]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20位的密码')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        # 短信验证码校验
        redis_conn = get_redis_connection('verifications')
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if sms_code_server is None or sms_code_server.decode() != sms_code_client:
            return render(request, 'oauth_callback.html', {'sms_code_message': '验证码错误'})

        # openid
        openid = check_access_token(access_token_openid)
        if not openid:
            return render(request, 'oauth_callback.html', {'openid_errmsg': 'openid error'})

        # 手机号用户查询
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 不存在创建用户
            user = User.objects.create_user(username=mobile, password=password, mobile=mobile)
        else:
            # 存在校验密码
            if not user.check_password(password):
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户密码错误'})

        # 绑定 openid
        try:
            oauth_qq_user = OauthQQUser.objects.create(user=user, openid=openid)
        except Exception as e:
            log.error(e)
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': '用户密码错误'})
        # 登陆状态保持
        login(request, user)
        next = request.POST.get('state')
        response = redirect(next)
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        return response

from django.shortcuts import render
from django.views import View
from django.conf import settings
from django import http
from QQLoginTool.QQtool import OAuthQQ
import logging

from meiduo_mall.utils.response_code import RETCODE, err_msg

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
        pass

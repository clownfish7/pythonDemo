import random

from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from django import http
from django_redis import get_redis_connection

from verifications.libs.captcha.captcha import captcha
from meiduo_mall.utils.response_code import RETCODE, err_msg
from verifications.libs.yuntongxun.ccp_sms import CCP
from . import constants


# Create your views here.
class SmsCodeView(View):
    """短信验证码"""

    def get(self, request, mobile):
        """
        @param mobile: 手机号
        @return: JSON
        """
        image_code_client = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        if not all([mobile, image_code_client, uuid]):
            return http.HttpResponseForbidden('缺失参数')

        redis_conn = get_redis_connection('verifications')
        image_code_server = redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({
                'code': RETCODE.IMAGECODEERR,
                'message': err_msg[RETCODE.IMAGECODEERR],
            })
        redis_conn.delete('img_%s' % uuid)
        image_code_server = image_code_server.decode()
        if image_code_server.lower() != image_code_client.lower():
            return http.JsonResponse({
                'code': RETCODE.IMAGECODEERR,
                'message': err_msg[RETCODE.IMAGECODEERR],
            })
        # 短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
                                constants.SEND_SMS_TEMPLATE_ID)
        return http.JsonResponse({
            'code': RETCODE.OK,
            'message': err_msg[RETCODE.OK],
        })


class ImageCodeView(View):
    """图形验证码"""

    def get(self, request, uuid):
        """
        @param uuid: 唯一标识该验证码属于哪个用户
        @return: image/jpg
        """
        code, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('verifications')
        # redis_conn.setex('key','expir','value')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, code)
        return http.HttpResponse(image, content_type='image/jpg')

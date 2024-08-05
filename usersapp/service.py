import random
import re
from django.core.mail import send_mail
from django.http import HttpResponse
from django_redis import get_redis_connection

from mysite.settings import EMAIL_HOST_USER



# 验证邮箱格式
def verify_email(email):
    re_mail = r'(\w+)@(\w+)\.(\w+)'
    if re.match(re_mail, email):
        return True
    return False


# class EmailVerificationView(View):


def post_email(email):
    DURATION = 3  # 有效时长，单位为分钟
    EMAIL_KEY_TEMPL = 'email:verification:%s'

    verification_code = random.randint(100000, 999999)  # 六位随机验证码

    # 将验证码保存到redis数据库
    cache = get_redis_connection(alias='verify_codes')  # 获取redis连接对象 from django_redis import get_redis_connection
    cache.set(EMAIL_KEY_TEMPL % email, verification_code, 60 * DURATION)  # redis缓存验证码

    send_mail_task(email, verification_code, DURATION)
    print(f'收件人：{email}')
    return HttpResponse('发送邮件成功')


def send_mail_task(email, verification_code, duration):
    """
        发送邮箱验证码
        :param email: 收件人邮箱
        :param verification_code: 随机验证码
        :param duration: 有效时长
        :return:发送状态
        """

    email_param = {
        'subject': '网站邮箱验证码',
        'message': '',
        'html_message':  # f-string: 格式化字符串常量，也就是格式化 {} 内容。Python3.6及以后的版本可用
            f"""   
                    <h2>欢迎注册,祝你生活愉快！</h2>
                    <p>您的验证码为：<span style='color:#ff5722'>{verification_code}</span></p>
                    <p>注意：验证码的有效时长为{duration}分钟</p>
                """,
        'from_email': EMAIL_HOST_USER,  # from FFmall.settings import EMAIL_HOST_USER
        'recipient_list': [email],  # 接收者
    }
    res_email = send_mail(**email_param)  # from django.core.mail import send_mail
    return res_email


def register(request):
    # 校验验证码
    EMAIL_KEY_TEMPL = 'email:verification:%s'
    vecode = request.POST.get('email_code')
    email = request.POST.get('email')
    cache = get_redis_connection(alias='verify_codes')
    cache_vecode = cache.get(EMAIL_KEY_TEMPL % email)
    if vecode != cache_vecode:
        return "邮箱验证错误"
    return ""

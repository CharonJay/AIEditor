from alipay import AliPay
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.models import CustomUser
from datetime import timedelta
from django.utils import timezone

from django.http import JsonResponse

alipay = AliPay(
    appid=settings.ALIPAY_APPID,
    app_notify_url=None,
    app_private_key_string=settings.ALIPAY_PRIVATE_KEY,
    alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY,
    sign_type="RSA2",
    debug=settings.ALIPAY_DEBUG
)

@api_view(['POST', 'GET'])
def create_alipay_payment(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    print('开始支付了')
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=f"order_{user_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}",  # 订单号，需要唯一
        total_amount=0.01,  # 订单金额
        subject="Membership Purchase",
        return_url=settings.ALIPAY_RETURN_URL,
        notify_url=settings.ALIPAY_NOTIFY_URL
    )
    print(0)

    alipay_url = "https://openapi-sandbox.dl.alipaydev.com/gateway.do?" + order_string if settings.ALIPAY_DEBUG else "https://openapi.alipay.com/gateway.do?" + order_string
    print('1 '+alipay_url)
    return Response({'url': alipay_url}, status=status.HTTP_303_SEE_OTHER)

def pad_base64(b64_string):
    return b64_string + '=' * (-len(b64_string) % 4)

@api_view(['POST'])
def alipay_notify(request):
    data = request.POST.dict()
    signature = data.pop("sign")

    #print("Received Data:", data)
    #print("Received Signature:", signature)

    #signature = pad_base64(signature)

    success = alipay.verify(data, signature)
    if success:
        out_trade_no = data.get('out_trade_no')
        user_id = out_trade_no.split('_')[1]  # 假设订单号中包含用户ID

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.now()
        current_expiration = user.membership_expiration

        if current_expiration and current_expiration > current_time:
            new_expiration_date = current_expiration + timedelta(days=30)
        else:
            new_expiration_date = current_time + timedelta(days=30)

        user.is_member = True
        user.membership_expiration = new_expiration_date
        user.save()
        return Response({"message": "Payment successful, membership activated."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import os

# 大模型
from erniebot_agent.chat_models import ERNIEBot


os.environ["EB_AGENT_ACCESS_TOKEN"] = "667595ca971e8228418f477dd45e78444b88c14e"

@csrf_exempt
@api_view(['GET'])
def alipay_return(request):
    data = request.GET.dict()
    signature = data.pop("sign")

    success = alipay.verify(data, signature)
    if success:
        out_trade_no = data.get('out_trade_no')
        user_id = out_trade_no.split('_')[1]  # 假设订单号中包含用户ID

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        current_time = timezone.now()
        current_expiration = user.membership_expiration

        if current_expiration and current_expiration > current_time:
            new_expiration_date = current_expiration + timedelta(days=30)
        else:
            new_expiration_date = current_time + timedelta(days=30)

        user.is_member = True
        user.membership_expiration = new_expiration_date
        user.save()
        cache.delete(f'user_model_{user_id}')
        user_model=None
        if user.is_member:
            user_model = ERNIEBot(model='ernie-4.0')
            print(1)
        else:
            user_model = ERNIEBot(model='ernie-3.5')

        # 加入记忆
        DEFAULT_TIMEOUT = 86400  # 24 hours in seconds
        timeout = DEFAULT_TIMEOUT

        cache.set(f'user_model_{user_id}', user_model, timeout)

        return HttpResponseRedirect(f'39.105.111.211/personalcenter?status=success')
    else:
        return HttpResponseRedirect(f'39.105.111.211/personalcenter?status=failure')

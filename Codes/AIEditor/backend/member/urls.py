from django.urls import path
from .views import create_alipay_payment, alipay_notify, alipay_return

urlpatterns = [
    path('create-alipay-payment/<int:user_id>/', create_alipay_payment, name='create_alipay_payment'),
    path('alipay-notify/', alipay_notify, name='alipay_notify'),
    path('alipay-return/', alipay_return, name='alipay_return'),
]

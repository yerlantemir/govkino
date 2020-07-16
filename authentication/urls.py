from django.urls import path
from rest_framework.authtoken import views as authview

from .views import SMSSignInView, SMSSignInVerificationView, SignUpView, SignUpVerificationView, \
    PasswordSignInView

urlpatterns = [
    path('api-token-auth/', authview.obtain_auth_token),
    path('sms-sign-in/', SMSSignInView.as_view(), name='sms-sign-in'),
    path('sms-sign-in/verify/', SMSSignInVerificationView.as_view(), name='sms-sign-in-verify'),
    path('password-sign-in/', PasswordSignInView.as_view(), name='password-sign-in'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-up/verify/', SignUpVerificationView.as_view(), name='sign-up-verify')
]

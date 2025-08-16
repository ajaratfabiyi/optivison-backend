# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, 
    ProfileView,
    LoginView, 
    TwoFAVerifyView,  # ✅ matches your views.py
    RequestPinTokenView,
    SetPinView,
    VerifyPinView
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/2fa/', TwoFAVerifyView.as_view(), name='login_2fa'),  # ✅ no mismatch now
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile
    path('me/', ProfileView.as_view(), name='profile'),

    # PIN management
    path('pin/request-token/', RequestPinTokenView.as_view(), name='request_pin_token'),
    path('pin/set/', SetPinView.as_view(), name='set_pin'),
    path('pin/verify/', VerifyPinView.as_view(), name='verify_pin'),
]

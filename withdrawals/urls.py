from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WithdrawalRequestViewSet,
    AdminApproveWithdrawalView,
    ServiceConfirmWithdrawalView
)

router = DefaultRouter()
router.register(r'', WithdrawalRequestViewSet, basename='withdrawal')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/approve/<int:pk>/', AdminApproveWithdrawalView.as_view(), name='approve_withdrawal'),
    path('service/confirm/<int:pk>/', ServiceConfirmWithdrawalView.as_view(), name='confirm_withdrawal'),
]

from django.urls import path
from .views import (
    AdminUserListView, AdminUserToggleActiveView,
    AdminKYCListView, AdminKYCApproveView, AdminKYCRejectView,
    AdminTransactionListView
)

urlpatterns = [
    # Users (UUID support)
    path('users/', AdminUserListView.as_view(), name='admin-users'),
    path('users/<uuid:pk>/toggle/', AdminUserToggleActiveView.as_view(), name='admin-user-toggle'),

    # KYC
    path('kyc/', AdminKYCListView.as_view(), name='admin-kyc'),
    path('kyc/<int:pk>/approve/', AdminKYCApproveView.as_view(), name='admin-kyc-approve'),
    path('kyc/<int:pk>/reject/', AdminKYCRejectView.as_view(), name='admin-kyc-reject'),

    # Transactions
    path('transactions/', AdminTransactionListView.as_view(), name='admin-transactions'),
]

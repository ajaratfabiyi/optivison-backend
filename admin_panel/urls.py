from django.urls import path
from .views import (
    AdminUserListView, AdminUserUpdateView,
    AdminKYCListView, AdminKYCApproveView, AdminKYCRejectView,
    AdminWithdrawalListView, AdminWithdrawalApproveView, AdminWithdrawalRejectView,
    AdminTransactionListView
)

urlpatterns = [
    # Users (UUID support)
    path('users/', AdminUserListView.as_view(), name='admin-users'),
    path('users/<uuid:pk>/', AdminUserUpdateView.as_view(), name='admin-user-update'),

    # KYC
    path('kyc/', AdminKYCListView.as_view(), name='admin-kyc'),
    path('kyc/<int:pk>/approve/', AdminKYCApproveView.as_view(), name='admin-kyc-approve'),
    path('kyc/<int:pk>/reject/', AdminKYCRejectView.as_view(), name='admin-kyc-reject'),

    # Withdrawals
    path('withdrawals/', AdminWithdrawalListView.as_view(), name='admin-withdrawals'),
    path('withdrawals/<int:pk>/approve/', AdminWithdrawalApproveView.as_view(), name='admin-withdrawal-approve'),
    path('withdrawals/<int:pk>/reject/', AdminWithdrawalRejectView.as_view(), name='admin-withdrawal-reject'),

    # Transactions
    path('transactions/', AdminTransactionListView.as_view(), name='admin-transactions'),
]

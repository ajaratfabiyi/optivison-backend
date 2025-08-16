# dashboard/urls.py
from django.urls import path
from .views import (
    UserStatsView,
    DownlineStatsView,
    EarningsStatsView,
    ReferralTreeView,
    DashboardOverviewView
)

urlpatterns = [
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('downline/', DownlineStatsView.as_view(), name='downline-stats'),
    path('earnings/', EarningsStatsView.as_view(), name='earnings-stats'),
    path('referrals/tree/', ReferralTreeView.as_view(), name='referral-tree'),
    path('overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
]

from django.urls import path
from .views import SubmitKYCView, KYCStatusView, AdminKYCUpdateView

urlpatterns = [
    path('submit/', SubmitKYCView.as_view(), name='submit_kyc'),
    path('status/', KYCStatusView.as_view(), name='kyc_status'),
    path('admin/update/<int:pk>/', AdminKYCUpdateView.as_view(), name='admin_update_kyc'),
]

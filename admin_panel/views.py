# admin_panel/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from users.models import User
from kyc.models import KYCSubmission
from transactions.models import Transaction
from withdrawals.models import WithdrawalRequest
from .serializers import (
    UserAdminSerializer,
    KYCAdminSerializer,
    TransactionAdminSerializer
)


# -------- USER MANAGEMENT --------
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]


class AdminUserUpdateView(generics.UpdateAPIView):
    """
    Allows admin to update multiple user fields (balance, status, withdrawal status).
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'updated', 'user': serializer.data})


# -------- KYC MANAGEMENT --------
class AdminKYCListView(generics.ListAPIView):
    queryset = KYCSubmission.objects.all().order_by('-submitted_at')
    serializer_class = KYCAdminSerializer
    permission_classes = [IsAdminUser]


class AdminKYCApproveView(generics.UpdateAPIView):
    queryset = KYCSubmission.objects.all()
    serializer_class = KYCAdminSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        kyc = self.get_object()
        kyc.status = 'approved'
        kyc.reviewed_at = timezone.now()
        kyc.save()
        kyc.user.is_kyc_verified = True
        kyc.user.save()
        return Response({'status': 'approved', 'user_verified': True})


class AdminKYCRejectView(generics.UpdateAPIView):
    queryset = KYCSubmission.objects.all()
    serializer_class = KYCAdminSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        reason = request.data.get('reason', '')
        kyc = self.get_object()
        kyc.status = 'rejected'
        kyc.rejection_reason = reason
        kyc.reviewed_at = timezone.now()
        kyc.save()
        kyc.user.is_kyc_verified = False
        kyc.user.save()
        return Response({'status': 'rejected', 'reason': reason})


# -------- WITHDRAWAL MANAGEMENT --------
class AdminWithdrawalListView(generics.ListAPIView):
    queryset = WithdrawalRequest.objects.all().order_by('-requested_at')
    serializer_class = TransactionAdminSerializer  # or create a specific WithdrawalAdminSerializer
    permission_classes = [IsAdminUser]


class AdminWithdrawalApproveView(generics.UpdateAPIView):
    queryset = WithdrawalRequest.objects.all()
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        withdrawal = self.get_object()
        withdrawal.status = 'approved'
        withdrawal.save()
        return Response({'status': 'approved'})


class AdminWithdrawalRejectView(generics.UpdateAPIView):
    queryset = WithdrawalRequest.objects.all()
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        reason = request.data.get('reason', '')
        withdrawal = self.get_object()
        withdrawal.status = 'rejected'
        withdrawal.notes = reason
        withdrawal.save()
        return Response({'status': 'rejected', 'reason': reason})


# -------- TRANSACTIONS MONITORING --------
class AdminTransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionAdminSerializer
    permission_classes = [IsAdminUser]

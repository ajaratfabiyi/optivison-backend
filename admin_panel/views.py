from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from users.models import User
from kyc.models import KYCSubmission
from transactions.models import Transaction
from .serializers import UserAdminSerializer, KYCAdminSerializer, TransactionAdminSerializer


# -------- USER MANAGEMENT --------
class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]


class AdminUserToggleActiveView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({'status': 'updated', 'is_active': user.is_active})


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

        # Also mark user as verified
        kyc.user.is_kyc_verified = True
        kyc.user.save()

        return Response({'status': 'approved', 'user_verified': True})


class AdminKYCRejectView(generics.UpdateAPIView):
    queryset = KYCSubmission.objects.all()
    serializer_class = KYCAdminSerializer
    permission_classes = [IsAdminUser]

    def patch(self, request, *args, **kwargs):
        kyc = self.get_object()
        kyc.status = 'rejected'
        kyc.reviewed_at = timezone.now()
        kyc.save()

        # Keep user unverified
        kyc.user.is_kyc_verified = False
        kyc.user.save()

        return Response({'status': 'rejected', 'user_verified': False})


# -------- TRANSACTIONS MONITORING --------
class AdminTransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionAdminSerializer
    permission_classes = [IsAdminUser]

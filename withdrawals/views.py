import uuid
from django.db import transaction as db_transaction
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WithdrawalRequest
from .serializers import WithdrawalRequestSerializer
from transactions.models import Transaction

class WithdrawalRequestViewSet(viewsets.ModelViewSet):
    serializer_class = WithdrawalRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WithdrawalRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with db_transaction.atomic():
            withdrawal = serializer.save(user=self.request.user, status='pending')

            transaction_obj = Transaction.objects.create(
                user=self.request.user,
                tx_type='withdrawal',
                amount=withdrawal.amount,
                reference=f"WDR-{uuid.uuid4().hex[:10].upper()}",
                status='pending'
            )

            withdrawal.transaction = transaction_obj
            withdrawal.save()


class AdminApproveWithdrawalView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            withdrawal = WithdrawalRequest.objects.get(pk=pk)
        except WithdrawalRequest.DoesNotExist:
            return Response({"error": "Withdrawal not found"}, status=status.HTTP_404_NOT_FOUND)

        if withdrawal.status != 'pending':
            return Response({"error": "Only pending withdrawals can be approved"}, status=status.HTTP_400_BAD_REQUEST)

        withdrawal.status = 'approved'
        withdrawal.save()
        return Response({"message": "Withdrawal approved", "status": withdrawal.status})


class ServiceConfirmWithdrawalView(APIView):
    permission_classes = [permissions.IsAdminUser]  # or a special API key check for provider

    def post(self, request, pk):
        try:
            withdrawal = WithdrawalRequest.objects.get(pk=pk)
        except WithdrawalRequest.DoesNotExist:
            return Response({"error": "Withdrawal not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            withdrawal.mark_as_paid()
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Update linked transaction
        if withdrawal.transaction:
            withdrawal.transaction.status = 'completed'
            withdrawal.transaction.save()

        return Response({"message": "Withdrawal marked as paid", "status": withdrawal.status})

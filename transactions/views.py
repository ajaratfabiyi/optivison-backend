# transactions/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    Handles listing and retrieving transactions for the logged-in user.
    Admins can view all transactions.
    """
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # Admins see all transactions
            return Transaction.objects.all().order_by('-created_at')
        # Regular users only see their own
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        # Prevent users from directly creating transactions
        return Response(
            {"detail": "Transactions cannot be created manually."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

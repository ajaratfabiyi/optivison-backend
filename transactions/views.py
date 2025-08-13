from rest_framework import viewsets, permissions
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their transactions
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Ensure all new transactions start as pending
        serializer.save(user=self.request.user, status='pending')

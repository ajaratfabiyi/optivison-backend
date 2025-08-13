from rest_framework import serializers
from users.models import User
from kyc.models import KYCSubmission
from transactions.models import Transaction

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'date_joined'
        ]


class KYCAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = KYCSubmission
        fields = [
            'id', 'user_email', 'status',
            'submitted_at', 'reviewed_at', 'document_type'
        ]


class TransactionAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'user_email', 'tx_type', 'amount',
            'status', 'created_at'
        ]

from rest_framework import serializers
from users.models import User
from kyc.models import KYCSubmission
from transactions.models import Transaction
from withdrawals.models import WithdrawalRequest


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_kyc_verified',
            'two_factor_enabled', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

    def update(self, instance, validated_data):
        """
        Allows partial admin updates to user fields such as is_active,
        is_staff, is_kyc_verified, and two_factor_enabled.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class KYCAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = KYCSubmission
        fields = [
            'id', 'user_email', 'status',
            'submitted_at', 'reviewed_at', 'document_type',
            'rejection_reason'
        ]
        read_only_fields = ['id', 'user_email', 'submitted_at', 'reviewed_at']


class TransactionAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'user_email', 'tx_type', 'amount',
            'status', 'created_at', 'reference'
        ]
        read_only_fields = ['id', 'user_email', 'created_at', 'reference']


class WithdrawalAdminSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = WithdrawalRequest
        fields = [
            'id', 'user_email', 'amount', 'bank_name',
            'account_number', 'account_name', 'status',
            'requested_at', 'updated_at', 'notes'
        ]
        read_only_fields = ['id', 'user_email', 'requested_at', 'updated_at']

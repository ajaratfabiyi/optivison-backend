from rest_framework import serializers
from .models import WithdrawalRequest

class WithdrawalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalRequest
        fields = '__all__'
        read_only_fields = [
            'id', 'status', 'requested_at', 'updated_at', 'transaction', 'user'
        ]

    def validate_account_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Account number must contain only digits.")
        return value

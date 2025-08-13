from rest_framework import serializers

class UserStatsSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_earnings = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_withdrawn = serializers.DecimalField(max_digits=12, decimal_places=2)
    referrals_count = serializers.IntegerField()
